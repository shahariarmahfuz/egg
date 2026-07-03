import requests
from models import db, Business
from app import app

# Ensure two businesses exist
with app.app_context():
    b1 = Business.query.filter_by(business_slug='super-biz').first()
    b2 = Business.query.filter_by(business_slug='super-biz-2').first()
    if not b2:
        b2 = Business(business_name='Super Biz 2', business_slug='super-biz-2')
        db.session.add(b2)
        db.session.commit()

session = requests.Session()

# Login to business 1
session.post('http://127.0.0.1:8080/dashboard/login', data={'username': 'superadmin', 'password': 'password'})

# Add supplier to business 1
data = {'supplier_name': 'Global Corp', 'contact_number': '1234567'}
r1 = session.post('http://127.0.0.1:8080/business/super-biz/supplier/add_supplier', data=data)
print("Add Global Corp to super-biz:", r1.status_code)

# Add duplicate supplier to business 1
r2 = session.post('http://127.0.0.1:8080/business/super-biz/supplier/add_supplier', data=data)
print("Add duplicate Global Corp to super-biz status:", r2.status_code)
print("Duplicate message present:", b'Supplier name already exists.' in r2.content)

# Login to business 2 (we need a user for business 2, let's just make the request)
# Since the global interceptor uses `g.business`, we can mock a request if needed, 
# or just test the DB directly.
