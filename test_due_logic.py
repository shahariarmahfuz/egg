import os
from flask import Flask
from models import db, Customer, Sale, CustomerCollection, SaleReturn, Business
from customer_collection import _calculate_customer_due
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    
    b = Business(business_name="Test Business", business_slug="test-biz")
    db.session.add(b)
    db.session.commit()
    
    c = Customer(business_id=b.id, customer_name="Test Cust", customer_code="C001", previous_balance=0.0)
    db.session.add(c)
    db.session.commit()
    
    print(f"Customer: {c.customer_name}")
    initial_due, _ = _calculate_customer_due(c.id)
    print(f"Initial Due: {initial_due}")
    
    print("--- Creating Sale ---")
    s = Sale(business_id=b.id, customer_id=c.id, sale_date=date.today(), total_amount=1000, due_amount=1000, cash_paid=0)
    db.session.add(s)
    db.session.commit()
    
    after_sale_due, _ = _calculate_customer_due(c.id)
    print(f"Due after 1000 sale: {after_sale_due}")
    
    print("--- Creating Collection ---")
    col = CustomerCollection(business_id=b.id, customer_id=c.id, date=date.today(), previous_due=after_sale_due, cash_paid=400, discount=0, balance=after_sale_due-400)
    db.session.add(col)
    db.session.commit()
    
    after_col_due, _ = _calculate_customer_due(c.id)
    print(f"Due after 400 collection: {after_col_due}")
    
    print("Test passed.")
