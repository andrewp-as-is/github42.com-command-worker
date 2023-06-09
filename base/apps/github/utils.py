from datetime import datetime, timedelta
import json
import os

import requests

from base.utils import headers2str

from ..pages.models import Page, PageBase, Pagination, PaginationPage
from ..http.models import RequestBase
from .models import Token, User, UserSync, UserSyncBase


def get_headers(page=None,token=None):
    headers = {}
    if token:
        headers['Authorization'] = 'Bearer %s' % token.token
    if page and page.etag:
        headers['If-None-Match'] =  page.etag
    return headers

def get_url(relpath):
    return 'https://api.github.com%s?per_page=100&page=1' % relpath

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
    kwargs['is_requests_created'] = True
    canonical_urls = []
    if user:
        canonical_urls.append('https://api.github.com/user/%s' % user.id)
        kwargs['is_user_updated'] = False
        kwargs['user_id'] = user.id
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
    url = get_url('/user/%s/repos' % user.id)
    if is_owner:
        url = get_url('/user/repos')
    canonical_urls.append(url)
    if 'org' not in str(user.type).lower():
        if created and user.followers_count and user.followers_count<=100:
            url = get_url('/user/%s/followers' % user.id)
            canonical_urls.append(url)
        else:
            kwargs.update({'is_followers_list_updated':True})
        if created and user.following_count and user.following_count<=100:
            url = get_url('/user/%s/following' % user.id)
            canonical_urls.append(url)
        else:
            kwargs.update({'is_following_list_updated':True})
        url = get_url('/user/%s/starred' % user.id)
        if is_owner:
            url = url+'&owner=1'
        canonical_urls.append(url)
    UserSync.objects.filter(id=sync.id).update(**kwargs)
    http_requests = []
    page_list = list(Page.objects.filter(url__in=canonical_urls).only('id','url','etag'))
    missing_urls = list(set(canonical_urls)-set(map(lambda p:p.url,page_list)))
    missing_pages = list(map(lambda url:PageBase(url=url),missing_urls))
    PageBase.objects.bulk_create(missing_pages)
    page_list+=list(Page.objects.filter(url__in=missing_urls).only('id','url','etag'))
    page_ids = list(map(lambda p:p.id,page_list))
    request_list = list(RequestBase.objects.filter(page_id__in=page_ids).only('id','url'))
    pagination_list = list(Pagination.objects.filter(page_id__in=page_ids))
    pagination_ids = list(map(lambda p:p.id,pagination_list))
    if pagination_ids:
        PaginationPage.objects.filter(pagination_id__in=pagination_ids).delete()
        Pagination.objects.filter(id__in=pagination_ids).delete()
    for canonical_url in canonical_urls:
        page = next(filter(lambda p:p.url==canonical_url,page_list),None)
        request = next(filter(lambda r:r.page_id==page.id,request_list),None)
        headers = get_headers(page,token)
        sep = '&' if '?' in canonical_url else '?'
        url = '%s%spage_id=%s&token_id=%s&user_id=%s' % (canonical_url,sep,page.id,token.id,user.id)
        if '/starred' in canonical_url:
            headers['Accept'] = 'application/vnd.github.v3.star+json'
        if not request:
            http_requests.append(RequestBase(page_id=page.id,url=url,headers=headers2str(headers),priority=100))
    RequestBase.objects.bulk_create(http_requests)
