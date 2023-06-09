from datetime import datetime, timedelta
import json
import os

import requests

from base.utils import headers2str

from ..pages.models import Page, Pagination, PaginationPage
from ..http.models import RequestBase
from .models import Token, User, UserSync, UserSyncBase


def get_headers(page=None,token=None):
    headers = {}
    if token:
        headers['Authorization'] = 'Bearer %s' % token.token
    if page and page.etag:
        headers['If-None-Match'] =  page.etag
    return headers

def get_url(relpath,token):
    return 'https://api.github.com%s?per_page=100&page=1&token_user_id=%s&token_id=%s' % (relpath,token.user_id,token.id)

def sync_user(login,token):
    try:
        user = User.objects.get(login=login)
        created = False
    except User.DoesNotExist:
        user = None
    is_owner = user and user.id==token.user_id
    sync, created = UserSyncBase.objects.get_or_create(login=login)
    if sync.is_disabled:
        return
    kwargs = dict(token_id=token.id,started_at=datetime.now(),finished_at=None)
    for f in filter(lambda f:'is_' in f.name,UserSync._meta.fields):
        kwargs[f.name] = False
    kwargs['is_repos_requests_created'] = True
    urls = []
    if user:
        urls.append('https://api.github.com/user/%s' % user.id)
        kwargs['is_user_updated'] = False
    else:
        url = 'https://api.github.com/users/%s' % login
        r = requests.get(url,headers={"Authorization": "Bearer %s" % token.token})
        token.update(r.headers)
        if r.status_code in [200,304]:
            defaults = {
                'status':r.status_code,
                'etag':r.headers['etag'],
                'checked_at':datetime.now()
                # 'updated_at':datetime.now()
            }
            Page.objects.update_or_create(defaults,url=url)
            data = r.json()
            defaults = dict(
                login = data['login'],
                type = data['type'],
                name = data['name'],
                company = data['company'],
                blog = data['blog'],
                location = data['location'],
                bio = data['bio'],

                public_repos_count = data['public_repos'],

                followers_count = data['followers'],
                following_count = data['following'],

                created_at = datetime.strptime(data['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
                updated_at = datetime.strptime(data['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
            )
            user, created = User.objects.get_or_create(defaults,id = data['id'])
            is_owner = user.id==token.user_id
            kwargs.update(user_id=data['id'],is_user_updated=True)
        if r.status_code in [403]: # ?
            pass
        if r.status_code in [404]:
            kwargs = dict(token_id=None,started_at=datetime.now(),finished_at=datetime.now())
            for f in filter(lambda f:'is_' in f.name,UserSync._meta.fields):
                kwargs[f.name] = True
            UserSync.objects.filter(id=sync.id).update(**kwargs)
            return
    if 'org' not in str(user.type).lower():
        url = get_url('/user/%s/repos' % user.id,token)
        if is_owner:
            url = get_url('/user/repos',token)
        urls.append(url)
        if created and user.followers_count:
            url = get_url('/user/%s/followers' % user.id,token)
            urls.append(url)
        else:
            kwargs.update({'is_followers_list_updated':True})
        if created and user.following_count:
            url = get_url('/user/%s/following' % user.id,token)
            urls.append(url)
        else:
            kwargs.update({'is_following_list_updated':True})
        url = get_url('/user/%s/starred' % user.id,token)
        if is_owner:
            url = url+'&owner=1'
        urls.append(url)
    UserSync.objects.filter(id=sync.id).update(**kwargs)
    http_requests = []
    page_list = list(Page.objects.filter(url__in=urls).only('id','url','etag'))
    page_ids = list(map(lambda p:p.id,page_list))
    request_list = list(RequestBase.objects.filter(page_id__in=page_ids).only('id','url'))
    pagination_list = list(Pagination.objects.filter(page_id__in=page_ids))
    pagination_ids = list(map(lambda p:p.id,pagination_list))
    if pagination_ids:
        PaginationPage.objects.filter(pagination_id__in=pagination_ids).delete()
        Pagination.objects.filter(id__in=pagination_ids).delete()
    for url in urls:
        page = next(filter(lambda p:p.url==url,page_list),None)
        request = next(filter(lambda r:r.url==url,request_list),None)
        if not page:
            page, created = Page.objects.get_or_create(url=url)
        headers = get_headers(page,token)
        if '/starred' in url:
            headers['Accept'] = 'application/vnd.github.v3.star+json'
        if not request:
            http_requests.append(RequestBase(url=url,page_id=page.id,headers=headers2str(headers)))
    RequestBase.objects.bulk_create(http_requests)
