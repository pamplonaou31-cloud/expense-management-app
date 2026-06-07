"""Authentication routes."""

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Category, DEFAULT_CATEGORIES
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__)


def init_categories():
    """Initialize default categories if they don't exist."""
    for cat_data in DEFAULT_CATEGORIES:
        existing = Category.query.filter_by(name=cat_data['name']).first()
        if not existing:
            category = Category(name=cat_data['name'], icon=cat_data['icon'])
            db.session.add(category)
    db.session.commit()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # Validate input
        if not username or len(username) < 3:
            flash('Username must be at least 3 characters long.', 'error')
            return redirect(url_for('auth.register'))
        
        if not email or '@' not in email:
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('auth.register'))
        
        if not password or len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return redirect(url_for('auth.register'))
        
        if password != password_confirm:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.register'))
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            if existing_user.username == username:
                flash('Username already taken.', 'error')
            else:
                flash('Email already registered.', 'error')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            
            # Initialize categories
            init_categories()
            
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login a user."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember_me') is not None
        
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Invalid username or password.', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember_me)
        
        # Initialize categories
        init_categories()
        
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
@login_required
def profile():
    """View user profile."""
    from app.models import Expense
    from datetime import datetime
    
    total_expenses = sum(e.amount for e in current_user.expenses)
    expense_count = current_user.expenses.count()
    avg_expense = total_expenses / expense_count if expense_count > 0 else 0
    
    return render_template('profile.html',
                           user=current_user,
                           total_expenses=total_expenses,
                           expense_count=expense_count,
                           avg_expense=round(avg_expense, 2))


@auth_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile."""
    new_email = request.form.get('email', '').strip()
    new_password = request.form.get('new_password', '')
    current_password = request.form.get('current_password', '')
    
    # Verify current password
    if not current_user.check_password(current_password):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('auth.profile'))
    
    # Update email if provided
    if new_email and new_email != current_user.email:
        if User.query.filter_by(email=new_email).first():
            flash('Email already in use.', 'error')
            return redirect(url_for('auth.profile'))
        current_user.email = new_email
    
    # Update password if provided
    if new_password:
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return redirect(url_for('auth.profile'))
        current_user.set_password(new_password)
    
    try:
        db.session.commit()
        flash('Profile updated successfully.', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('An error occurred while updating profile.', 'error')
    
    return redirect(url_for('auth.profile'))
