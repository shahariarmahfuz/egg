import requests

session = requests.Session()

# 1. Login to business as superadmin
session.post('http://127.0.0.1:8080/dashboard/login', data={'username': 'superadmin', 'password': 'password'})

# 2. Add Sale using the product we created
sale_data = {
    'customer_id': '',
    'bill_number': 'BILL123',
    'sale_date': '2026-07-03',
    'payment_method': 'Cash',
    'transport_cost': '0',
    'labour_cost': '0',
    'vat': '0',
    'discount': '0',
    'cash_paid': '15',
    'note': 'Test sale',
    'product_id[]': '4',
    'quantity[]': '1',
    'price[]': '15'
}
r = session.post('http://127.0.0.1:8080/business/super-biz/sale/add_sale', data=sale_data)
print("Add sale status:", r.status_code)

# 3. Check if stock was reduced
r = session.get('http://127.0.0.1:8080/business/super-biz/product/api/list')
products = r.json()['data']
for p in products:
    if p['product_name'] == 'Test Sale Product':
        print("Stock after sale:", p['current_stock'])

