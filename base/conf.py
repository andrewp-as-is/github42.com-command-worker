import os

ROOT_DIRNAME = os.path.join(os.path.expanduser("~"),'.github42.com','files')
if os.path.exists('/.dockerenv'):
    ROOT_DIRNAME = os.path.join('/files') # use docker volumes

PROXY_HTTP_URL = "https://raw.githubusercontent.com/andrewp-as-is/proxy-list/master/http.txt"
PROXY_SOCKS4_URL = "https://raw.githubusercontent.com/andrewp-as-is/proxy-list/master/socks4.txt"
