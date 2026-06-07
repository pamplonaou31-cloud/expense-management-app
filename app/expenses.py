"""Expense management routes."""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Expense, Category
from datetime import datetime, timedelta
import json

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')


def get_user_categories():
    """Get list of categories for dropdown."""
    categories = Category.query.all()
    return [cat.name for cat in categories]


@expenses_bp.route('/')
@login_required
def view_expenses():
    """View all expenses."""
    page = request.args.get('page', 1, type=int)
    category_filter = request.args.get('category', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    query = Expense.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if category_filter:
        query = query.filter_by(category=category_filter)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Expense.date >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Expense.date <= date_to_obj)
        except ValueError:
            pass
    
    # Paginate results
    expenses = query.order_by(Expense.date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    categories = get_user_categories()
    total = sum(e.amount for e in query)
    
    return render_template('expenses.html',
                           expenses=expenses,
                           categories=categories,
                           category_filter=category_filter,
                           date_from=date_from,
                           date_to=date_to,
                           total=total)


@expenses_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Add a new expense."""
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
            category = request.form.get('category', '').strip()
            description = request.form.get('description', '').strip()
            date_str = request.form.get('date', '')
            
            # Validate input
            if amount <= 0:
                flash('Amount must be greater than 0.', 'error')
                return redirect(url_for('expenses.add_expense'))
            
            if not category:
                flash('Please select a category.', 'error')
                return redirect(url_for('expenses.add_expense'))
            
            if not date_str:
                flash('Please select a date.', 'error')
                return redirect(url_for('expenses.add_expense'))
            
            try:
                expense_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'error')
                return redirect(url_for('expenses.add_expense'))
            
            # Create expense
            expense = Expense(
                user_id=current_user.id,
                amount=amount,
                category=category,
                description=description,
                date=expense_date
            )
            
            db.session.add(expense)
            db.session.commit()
            
            flash('Expense added successfully!', 'success')
            return redirect(url_for('expenses.view_expenses'))
        
        except ValueError:
            flash('Please enter a valid amount.', 'error')
            return redirect(url_for('expenses.add_expense'))
    
    categories = get_user_categories()
    today = datetime.now().date().isoformat()
    
    return render_template('add_expense.html',
                           categories=categories,
                           today=today,
                           mode='add')


@expenses_bp.route('/<int:expense_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    """Edit an expense."""
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
            category = request.form.get('category', '').strip()
            description = request.form.get('description', '').strip()
            date_str = request.form.get('date', '')
            
            # Validate input
            if amount <= 0:
                flash('Amount must be greater than 0.', 'error')
                return redirect(url_for('expenses.edit_expense', expense_id=expense_id))
            
            if not category:
                flash('Please select a category.', 'error')
                return redirect(url_for('expenses.edit_expense', expense_id=expense_id))
            
            if not date_str:
                flash('Please select a date.', 'error')
                return redirect(url_for('expenses.edit_expense', expense_id=expense_id))
            
            try:
                expense_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'error')
                return redirect(url_for('expenses.edit_expense', expense_id=expense_id))
            
            # Update expense
            expense.amount = amount
            expense.category = category
            expense.description = description
            expense.date = expense_date
            
            db.session.commit()
            
            flash('Expense updated successfully!', 'success')
            return redirect(url_for('expenses.view_expenses'))
        
        except ValueError:
            flash('Please enter a valid amount.', 'error')
            return redirect(url_for('expenses.edit_expense', expense_id=expense_id))
    
    categories = get_user_categories()
    expense_date = expense.date.isoformat()
    
    return render_template('add_expense.html',
                           expense=expense,
                           categories=categories,
                           mode='edit')


@expenses_bp.route('/<int:expense_id>/delete', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Delete an expense."""
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
    
    db.session.delete(expense)
    db.session.commit()
    
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('expenses.view_expenses'))


@expenses_bp.route('/api/chart-data')
@login_required
def get_chart_data():
    """Get chart data for dashboard."""
    # Category breakdown
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    
    category_data = {}
    for expense in expenses:
        category_data[expense.category] = category_data.get(expense.category, 0) + expense.amount
    
    # Monthly trend (last 12 months)
    now = datetime.now()
    monthly_data = {}
    
    for i in range(12):
        month_date = now - timedelta(days=30*i)
        month_key = month_date.strftime('%Y-%m')
        monthly_data[month_key] = 0
    
    for expense in expenses:
        month_key = expense.date.strftime('%Y-%m')
        if month_key in monthly_data:
            monthly_data[month_key] += expense.amount
    
    return jsonify({
        'categories': list(category_data.keys()),
        'category_amounts': list(category_data.values()),
        'months': list(reversed(list(monthly_data.keys()))),
        'monthly_amounts': list(reversed(list(monthly_data.values())))
    })
