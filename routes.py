from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from models import db, ExpenseEntry, CashOut, Purchase, PurchaseReturn, Sale, SaleItem

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    return redirect(url_for('routes.dashboard'))

@routes_bp.route('/dashboard')
@login_required
def dashboard():
    total_expense = db.session.query(db.func.sum(ExpenseEntry.amount)).scalar() or 0.00
    total_cash_out = db.session.query(db.func.sum(CashOut.amount)).scalar() or 0.00
    
    cash_purchase_base = db.session.query(db.func.sum(Purchase.cash_paid)).scalar() or 0.00
    purchase_due_base = db.session.query(db.func.sum(Purchase.due_amount)).scalar() or 0.00

    cash_refund = db.session.query(db.func.sum(PurchaseReturn.cash_refund)).scalar() or 0.00
    due_adjustment = db.session.query(db.func.sum(PurchaseReturn.due_adjustment)).scalar() or 0.00
    
    cash_purchase = cash_purchase_base - cash_refund
    purchase_due = purchase_due_base - due_adjustment
    
    cash_sale = db.session.query(db.func.sum(Sale.cash_paid)).scalar() or 0.00
    sale_due = db.session.query(db.func.sum(Sale.due_amount)).scalar() or 0.00
    sale_income = db.session.query(db.func.sum(SaleItem.profit)).scalar() or 0.00

    summary_data = {
        'cash_sale': cash_sale,
        'cash_purchase': cash_purchase,
        'sale_due': sale_due,
        'purchase_due': purchase_due,
        'sale_return': 0.00,
        'sale_income': sale_income,
        'return_due': 0.00,
        'expense': total_expense,
        'cash_out': total_cash_out
    }
    return render_template('dashboard.html', data=summary_data)
