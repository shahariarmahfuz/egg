import requests

session = requests.Session()

# 1. Login to business as superadmin
r = session.post('http://127.0.0.1:8080/dashboard/login', data={'username': 'superadmin', 'password': 'password'})
print("Login status:", r.status_code)

# 2. Add a new product with stock > 0
product_data = {
    'product_name': 'Test Sale Product',
    'category': 'Test Category',
    'brand': 'Test Brand',
    'unit': 'Pcs',
    'cost_price': '10',
    'selling_price': '15',
    'opening_stock': '100',
    'min_stock_alert': '5',
    'barcode': 'BARCODE123',
    'description': 'Test description',
    'status': 'Active'
}
r = session.post('http://127.0.0.1:8080/business/super-biz/product/add_product', data=product_data)
print("Add product status:", r.status_code)

# 3. Search for the product using barcode
r = session.get('http://127.0.0.1:8080/business/super-biz/sale/api/search_product?q=BARCODE123')
print("Search product status:", r.status_code)
search_results = r.json()
print("Search results:", search_results)

if len(search_results) > 0:
    print("SUCCESS: Product found in search results!")
else:
    print("ERROR: Product NOT found in search results.")
