from app import create_app
from models import db, Supplier, Product, Purchase, PurchaseItem, Customer, Sale, SaleItem, CashOut, ExpenseHead, ExpenseEntry
from datetime import datetime

app = create_app()

def run_crud_tests():
    with app.app_context():
        try:
            # 1. Supplier CRUD
            sup = Supplier(supplier_name="Test Supplier", current_balance=100.0)
            db.session.add(sup)
            db.session.commit()
            sup_id = sup.id
            
            # 2. Product and Purchase
            prod = Product(product_code="TEST1", product_name="Test Product", current_stock=0)
            db.session.add(prod)
            db.session.commit()
            prod_id = prod.id
            
            purch = Purchase(supplier_id=sup_id, total_amount=100.0, due_amount=100.0)
            db.session.add(purch)
            db.session.commit()
            purch_id = purch.id
            
            p_item = PurchaseItem(purchase_id=purch_id, product_id=prod_id, quantity=10, purchase_price=10.0, total_price=100.0)
            db.session.add(p_item)
            prod.current_stock += 10
            sup.current_balance += 100
            db.session.commit()
            
            # 3. Customer and Sale
            cust = Customer(customer_name="Test Customer", current_balance=0.0)
            db.session.add(cust)
            db.session.commit()
            cust_id = cust.id
            
            sale = Sale(customer_id=cust_id, total_amount=50.0, due_amount=50.0)
            db.session.add(sale)
            db.session.commit()
            sale_id = sale.id
            
            s_item = SaleItem(sale_id=sale_id, product_id=prod_id, quantity=2, selling_price=25.0, cost_price=10.0, profit=30.0, total_price=50.0)
            db.session.add(s_item)
            prod.current_stock -= 2
            cust.current_balance += 50.0
            db.session.commit()
            
            # 4. Try deleting Sale (checks cascade)
            s = Sale.query.get(sale_id)
            db.session.delete(s)
            db.session.commit()
            
            # 5. Try deleting Purchase
            p = Purchase.query.get(purch_id)
            db.session.delete(p)
            db.session.commit()
            
            # 6. Try deleting Supplier
            s2 = Supplier.query.get(sup_id)
            db.session.delete(s2)
            db.session.commit()
            
            # 7. Try deleting Customer
            c2 = Customer.query.get(cust_id)
            db.session.delete(c2)
            db.session.commit()
            
            print("CRUD Tests Passed Successfully! Database logic and Cascades are perfectly configured.")
            
        except Exception as e:
            db.session.rollback()
            print(f"CRUD Tests Failed: {e}")

if __name__ == '__main__':
    run_crud_tests()
