import re

with open('models.py', 'r') as f:
    content = f.read()

# Add Business model
business_model = """
class Business(db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(150), nullable=False)
    business_slug = db.Column(db.String(150), unique=True, nullable=False)
    status = db.Column(db.String(50), default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
"""

if "class Business" not in content:
    content = content.replace("class Admin", business_model + "\nclass Admin")

# Add business_id to all models
models = [
    "Admin", "ExpenseHead", "ExpenseEntry", "CashOut", "Supplier", "Product",
    "Purchase", "PurchaseItem", "PurchaseReturn", "PurchaseReturnItem",
    "Customer", "Sale", "SaleItem", "CustomerLedger", "SaleReturn",
    "SaleReturnItem", "CustomerCollection", "CashLedger", "Bank",
    "BankTransaction", "SupplierPayment", "SupplierLedger"
]

for model in models:
    if f"class {model}(" in content:
        # Find where the class ends and add business_id
        pattern = r"(class " + model + r"\(.*?\):\n(?:\s+__tablename__ = .*?\n)?(?:\s+id = .*?\n))"
        replacement = r"\1    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=True)\n"
        content = re.sub(pattern, replacement, content, count=1)

events_code = """
from sqlalchemy import event
from sqlalchemy.orm import Query
from flask import g, has_request_context

@event.listens_for(Query, "before_compile", retval=True)
def before_compile(query):
    if has_request_context() and getattr(g, 'business', None):
        for column_description in query.column_descriptions:
            entity = column_description['entity']
            if entity is None:
                continue
            if hasattr(entity, 'business_id') and getattr(entity, '__name__', '') != 'Business':
                query = query.filter(entity.business_id == g.business.id)
    return query

@event.listens_for(db.Model, 'before_insert', propagate=True)
def receive_before_insert(mapper, connection, target):
    if hasattr(target, 'business_id') and getattr(target, '__class__', None) and target.__class__.__name__ != 'Business':
        if not target.business_id and has_request_context() and getattr(g, 'business', None):
            target.business_id = g.business.id
"""

if "def before_compile" not in content:
    content = content + "\n" + events_code

with open('models.py', 'w') as f:
    f.write(content)

print("models.py updated successfully.")
