import requests

session = requests.Session()

# 1. Login to site admin
login_data = {
    'username': 'siteadmin',
    'password': 'admin'
}
r = session.post('http://127.0.0.1:8080/site-admin/login', data=login_data)
print("Login status:", r.status_code)
print("Current URL:", r.url)

# 2. Create Business
biz_data = {
    'business_name': 'My Super Business',
    'business_slug': 'super-biz'
}
r = session.post('http://127.0.0.1:8080/site-admin/business/create', data=biz_data)
print("Create Biz status:", r.status_code)

# 3. Check Dashboard for the biz
r = session.get('http://127.0.0.1:8080/site-admin/dashboard')
print("Business in dashboard:", "super-biz" in r.text)

