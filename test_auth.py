import requests
from bs4 import BeautifulSoup

# 1. Login to business as superadmin, try to access site admin
session1 = requests.Session()
r = session1.post('http://127.0.0.1:8080/dashboard/login', data={'username': 'superadmin', 'password': 'password'})
print("superadmin login status:", r.status_code)
r = session1.get('http://127.0.0.1:8080/site-admin/dashboard')
print("superadmin trying to access site-admin dashboard status:", r.status_code)

# 2. Login to site admin as superadmin
r = session1.post('http://127.0.0.1:8080/site-admin/login', data={'username': 'superadmin', 'password': 'password'})
print("superadmin trying site-admin login status:", r.status_code)
print("superadmin site-admin login text contains 'Access Denied':", "Access Denied" in r.text)

# 3. Login to site admin as siteadmin, try to access business
session2 = requests.Session()
r = session2.post('http://127.0.0.1:8080/site-admin/login', data={'username': 'siteadmin', 'password': 'admin'})
print("siteadmin login status:", r.status_code)
r = session2.get('http://127.0.0.1:8080/business/super-biz/dashboard')
print("siteadmin trying to access business dashboard status:", r.status_code)
print("siteadmin business access text contains 'Access Denied':", "Access Denied" in r.text)

