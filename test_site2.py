import requests
from bs4 import BeautifulSoup

session = requests.Session()

# 1. Login to site admin
login_data = {
    'username': 'siteadmin',
    'password': 'admin'
}
r = session.post('http://127.0.0.1:8080/site-admin/login', data=login_data)

# 2. Get the business ID for super-biz
r = session.get('http://127.0.0.1:8080/site-admin/dashboard')
soup = BeautifulSoup(r.text, 'html.parser')
# Find the business super-biz in the table and its ID
super_biz_row = None
for row in soup.find_all('tr'):
    if 'super-biz' in row.text:
        super_biz_row = row
        break
biz_id = int(super_biz_row.find_all('td')[0].text.strip())
print("Business ID:", biz_id)

# 3. Create a user for super-biz
user_data = {
    'username': 'superadmin',
    'password': 'password',
    'name': 'Super Admin',
    'role': 'Admin'
}
r = session.post(f'http://127.0.0.1:8080/site-admin/users/{biz_id}/add', data=user_data)
print("Create User status:", r.status_code)

# 4. Login to the business as superadmin
biz_session = requests.Session()
biz_login_data = {
    'username': 'superadmin',
    'password': 'password'
}
r = biz_session.post('http://127.0.0.1:8080/business/super-biz/login', data=biz_login_data)
print("Biz Login URL:", r.url)
print("Biz Login Status:", r.status_code)

# 5. Access business dashboard
r = biz_session.get('http://127.0.0.1:8080/business/super-biz/dashboard')
print("Dashboard status:", r.status_code)
print("Dashboard HTML len:", len(r.text))
print("Dashboard title:", BeautifulSoup(r.text, 'html.parser').title.text)

