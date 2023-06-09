import os
from urllib.parse import parse_qs, urlparse

from ...conf import ROOT_DIRNAME,PROXY_HTTP_URL, PROXY_SOCKS4_URL
from . import patterns

def get_full_path(*args):
    return os.path.join(ROOT_DIRNAME,'tmp',*list(map(str,args)))

def get_repo_id(url):
    parsed_url = urlparse(url)
    return int(parse_qs(parsed_url.query)['repo_id'][0])

def get_path(url):
    parsed_url = urlparse(url)
    if patterns.GITHUB_REPO_JSON_PATTERN.match(url):
        repo_id = parse_qs(parsed_url.query)['repo_id'][0]
        return get_full_path('github-repo-json','%s.json' % repo_id)
    if patterns.GITHUB_REPO_HTML_PATTERN.match(url):
        repo_id = parse_qs(parsed_url.query)['repo_id'][0]
        return get_full_path('github-repo-html','%s.html' % repo_id)
    if patterns.GITHUB_REPO_DEPENDENTS_HTML_PATTERN.match(url):
        repo_id = parse_qs(parsed_url.query)['repo_id'][0]
        return get_full_path('github-repo-dependents-html','%s.html' % repo_id)
    if patterns.GITHUB_REPO_SPARKLINE_PATTERN.match(url):
        repo_id = parse_qs(parsed_url.query)['repo_id'][0]
        return get_full_path('github-repo-sparkline','%s.svg' % repo_id)
    if patterns.GITHUB_USER_JSON_PATTERN.match(url):
        user_id = parse_qs(parsed_url.query)['user_id'][0]
        return get_full_path('github-user-json','%s.json' % user_id)
    if patterns.GITHUB_USER_FOLLOWERS_JSON_PATTERN.match(url):
        page = parse_qs(parsed_url.query)['page'][0]
        user_id = parse_qs(parsed_url.query)['user_id'][0]
        return get_full_path('github-user-followers-json',user_id,'%s.json' % page)
    if patterns.GITHUB_USER_FOLLOWING_JSON_PATTERN.match(url):
        page = parse_qs(parsed_url.query)['page'][0]
        user_id = parse_qs(parsed_url.query)['user_id'][0]
        return get_full_path('github-user-following-json',user_id,'%s.json' % page)
    # https://api.github.com/user/repos
    if patterns.GITHUB_USER_REPOS_JSON_PATTERN.match(url):
        page = parse_qs(parsed_url.query)['page'][0]
        user_id = parse_qs(parsed_url.query)['user_id'][0]
        return get_full_path('github-user-repos-json',user_id,'%s.json' % page)
    if patterns.GITHUB_USER_PUBLIC_REPOS_JSON_PATTERN.match(url):
        page = parse_qs(parsed_url.query)['page'][0]
        user_id = parse_qs(parsed_url.query)['user_id'][0]
        return get_full_path('github-user-public-repos-json',user_id,'%s.json' % page)
    if patterns.GITHUB_USER_STARRED_REPOS_JSON_PATTERN.match(url):
        page = parse_qs(parsed_url.query)['page'][0]
        user_id = parse_qs(parsed_url.query)['user_id'][0]
        return get_full_path('github-user-starred-repos-json',user_id,'%s.json' % page)
    if PROXY_HTTP_URL in url:
        return get_full_path('proxy','http.txt')
    if PROXY_SOCKS4_URL in url:
        return get_full_path('proxy','socks4.txt')
