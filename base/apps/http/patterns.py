import re

GITHUB_REPO_JSON_PATTERN = re.compile("https://api.github.com/repositories/[a-z0-9]+\?")
GITHUB_REPO_HTML_PATTERN = re.compile("https://github.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+\?")
GITHUB_REPO_SPARKLINE_PATTERN = re.compile("https://github.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+/graphs/participation\?")
GITHUB_REPO_DEPENDENTS_HTML_PATTERN = re.compile("https://github.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9._-]+/network/dependents\?")
GITHUB_USER_JSON_PATTERN = re.compile("https://api.github.com/user/[0-9]+\?")
GITHUB_USER_FOLLOWERS_JSON_PATTERN = re.compile("https://api.github.com/user/[0-9]+/followers")
GITHUB_USER_FOLLOWING_JSON_PATTERN = re.compile("https://api.github.com/user/[0-9]+/following")
GITHUB_USER_REPOS_JSON_PATTERN = re.compile("https://api.github.com/user/repos")
GITHUB_USER_PUBLIC_REPOS_JSON_PATTERN = re.compile("https://api.github.com/user/[0-9]+/repos")
GITHUB_USER_STARRED_REPOS_JSON_PATTERN = re.compile("https://api.github.com/user/[0-9]+/starred")
