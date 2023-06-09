from collections import defaultdict
from datetime import datetime
import logging
import os
import random
import sys

import aiofiles
import asyncio
import aiohttp
from asgiref.sync import sync_to_async
from aiohttp_proxy import ProxyConnector
from django.conf import settings

from base.apps.http.models import Error, Request, Response
from base.apps.http.utils import get_path
from base.apps.proxy.models import Proxy

SEMA = asyncio.Semaphore(10)
PUSH_LIMIT = 100

async def write(path,text):
    # todo: .tmp?
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    async with SEMA:
        async with aiofiles.open(path, "w") as f:
            await f.write(text)
            await f.flush()
            await f.close()

async def get_pushed_count():
    qs = Request.objects.filter(is_pushed=True)
    return await sync_to_async(qs.count)()

async def get_push_count():
    return PUSH_LIMIT - await get_pushed_count()

async def push_tasks(q):
    push_count = await get_push_count()
    if push_count>0:
        request_list = await sync_to_async(list)(Request.objects.filter(is_pushed=False).order_by('-priority')[0:push_count])
        github_api_urls = list(filter(lambda r:'api.github.com' in r.url,request_list))
        proxy_count = len(request_list)-len(github_api_urls)
        proxy_list = await sync_to_async(list)(Proxy.objects.filter(is_active=True).only('id','addr')[0:proxy_count])
        proxy_data = defaultdict(int)
        for request in request_list:
            request.proxy_id = None
            if 'api.github.com' not in request.url and not settings.DEBUG:
                proxy = random.choice(proxy_list)
                if proxy:
                    request.proxy_id = proxy.id
                    request.proxy_url = proxy.get_proxy_url()
                    proxy_data[error.proxy_id]=proxy_data[error.proxy_id]+1
            q.put_nowait(request)
        ids = list(map(lambda t:t.id,request_list))
        await sync_to_async(Request.objects.filter(id__in=ids).update)(is_pushed=True)
        proxy_objs = []
        for proxy_id, calls_count in proxy_data.items():
            proxy_objs.append(Proxy(id=proxy_id,calls_count=F('calls_count')+calls_count))
        Proxy.objects.bulk_update(proxy_objs,fields=['calls_count'])

def get_headers_text(data):
    lines = []
    for k,v in data.items():
        if k == 'etag' or (k == 'Link' and 'prev' not in v) or 'x-ratelimit-' in k.lower():
            lines.append('%s: %s' % (k.lower(),v))
    return "\n".join(lines)

async def run_task(request):
    if settings.DEBUG:
        print('GET %s' % request.url)
        if request.headers:
            print(request.headers)
    try:
        connector = aiohttp.TCPConnector(enable_cleanup_closed=True)
        # todo: proxy
        #if request.proxy_url:
        #    connector = ProxyConnector.from_url(request.proxy_url)
        timeout = aiohttp.ClientTimeout(total=5)
        headers = request.get_headers()
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            async with session.get(request.url,headers=headers,allow_redirects=True) as r:
                if settings.DEBUG:
                    print('GET %s status %s' % (request.url,r.status))
                    #if request.headers:
                    #    print(request.headers)
                if r.status not in [304,404]:
                    try:
                        path = get_path(request.url)
                        if not path:
                            print('UNKNOWN: %s' % request.url)
                            sys.exit(0)
                    except Exception as e:
                        print('%s\n%s: %s' % (request.url,type(e),str(e)))
                        sys.exit(0)
                    content = await r.text()
                    await write(path,content)
                kwargs = dict(
                    url=request.url,
                    page_id=request.page_id,
                    status = r.status,
                    headers = get_headers_text(r.headers)
                )
                if request.page_id:
                    kwargs['page_id'] = request.page_id
                if request.proxy_id:
                    kwargs['proxy_id'] = request.proxy_id
                await sync_to_async(Response(**kwargs).save)()
    except Exception as e:
        print('settings.DEBUG = %s' % settings.DEBUG)
        if settings.DEBUG:
            logging.error(e)
        if 'server closed the connection unexpectedly' in str(e).lower():
            sys.exit(0) # restart docker. use docker `restart: always`
        exc_type='.'.join(filter(None,[type(e).__module__,type(e).__name__]))
        exc_value=str(e)
        # no need traceback :)
        # exc_traceback=''.join(format_exception(etype=type(e), value=e, tb=e.__traceback__))
        await sync_to_async(Error(
            url=request.url,
            page_id=request.page_id,
            proxy_id=request.proxy_id,
            exc_type=exc_type,
            exc_value=exc_value
        ).save)()
    finally:
        await sync_to_async(Request.objects.filter(id=request.id).delete)()
