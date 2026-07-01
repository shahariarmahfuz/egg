from flask import Blueprint, render_template
from flask_login import login_required

account_reports_bp = Blueprint('account_reports', __name__, url_prefix='/account_reports')

@login_required
@account_reports_bp.route('/expense_report')
def expense_report():
    return render_template('placeholder.html', title="Expense Report")
@login_required
@account_reports_bp.route('/income_report')
def income_report():
    return render_template('placeholder.html', title="Income Report")
@login_required
@account_reports_bp.route('/bank_report')
def bank_report():
    return render_template('placeholder.html', title="Bank Report")
@login_required
@account_reports_bp.route('/bank_statement')
def bank_statement():
    return render_template('placeholder.html', title="Bank Statement")
@login_required
@account_reports_bp.route('/cash_book')
def cash_book():
    return render_template('placeholder.html', title="Cash Book")

