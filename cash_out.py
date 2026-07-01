from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, CashOut
from datetime import datetime

cash_out_bp = Blueprint('cash_out', __name__, url_prefix='/cash_out')

@login_required
@cash_out_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        date_str = request.form.get('date')
        co_type = request.form.get('type')
        comment = request.form.get('comment')
        amount = request.form.get('amount')
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            amount_val = float(amount)
            if amount_val <= 0:
                flash("Amount must be greater than 0.", "danger")
            else:
                new_entry = CashOut(
                    date=date_obj,
                    type=co_type,
                    comment=comment,
                    amount=amount_val
                )
                db.session.add(new_entry)
                db.session.commit()
                flash("Cash Out record saved successfully.", "success")
                return redirect(url_for('cash_out.manage'))
        except Exception as e:
            flash(f"Error saving record: {e}", "danger")
            
    return render_template('cash_out_form.html', action="Add")

@login_required
@cash_out_bp.route('/manage')
def manage():
    records = CashOut.query.order_by(CashOut.date.desc(), CashOut.id.desc()).all()
    return render_template('manage_cash_out.html', records=records)

@login_required
@cash_out_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    record = CashOut.query.get_or_404(id)
    if request.method == 'POST':
        date_str = request.form.get('date')
        co_type = request.form.get('type')
        comment = request.form.get('comment')
        amount = request.form.get('amount')
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            amount_val = float(amount)
            if amount_val <= 0:
                flash("Amount must be greater than 0.", "danger")
            else:
                record.date = date_obj
                record.type = co_type
                record.comment = comment
                record.amount = amount_val
                db.session.commit()
                flash("Cash Out record updated successfully.", "success")
                return redirect(url_for('cash_out.manage'))
        except Exception as e:
            flash(f"Error updating record: {e}", "danger")
            
    return render_template('cash_out_form.html', action="Edit", record=record)

@login_required
@cash_out_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    record = CashOut.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash("Cash Out record deleted successfully.", "success")
    return redirect(url_for('cash_out.manage'))
