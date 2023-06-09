#!/usr/bin/env python
import requests


url = 'https://api.github.com/user'
headers = {"Authorization": "Bearer %s" % token}
r = requests.get(url,headers = headers)
data = r.json()
print(data)
