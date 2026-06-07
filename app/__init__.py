"""Flask application factory."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name='development'):
    """Create and configure Flask application."""
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Create instance folder if it doesn't exist
    try:
        import os
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Register blueprints
    from app.auth import auth_bp
    from app.expenses import expenses_bp
    from app.reports import reports_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(reports_bp)
    
    # Main routes
    @app.route('/')
    def index():
        from flask import redirect
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect('/dashboard')
        return redirect('/login')
    
    @app.route('/dashboard')
    def dashboard():
        from flask_login import login_required
        from flask import render_template
        from app.models import Expense
        from datetime import datetime, timedelta
        from sqlalchemy import func
        
        @login_required
        def view():
            user_id = current_user.id
            
            # Get current month expenses
            now = datetime.now()
            month_start = datetime(now.year, now.month, 1)
            if now.month == 12:
                month_end = datetime(now.year + 1, 1, 1) - timedelta(days=1)
            else:
                month_end = datetime(now.year, now.month + 1, 1) - timedelta(days=1)
            
            month_expenses = Expense.query.filter(
                Expense.user_id == user_id,
                Expense.date >= month_start,
                Expense.date <= month_end
            ).all()
            
            total_month = sum(e.amount for e in month_expenses)
            
            # Get all expenses for statistics
            all_expenses = Expense.query.filter_by(user_id=user_id).all()
            total_all = sum(e.amount for e in all_expenses)
            avg_all = total_all / len(all_expenses) if all_expenses else 0
            max_all = max((e.amount for e in all_expenses), default=0)
            
            # Get recent expenses
            recent_expenses = Expense.query.filter_by(user_id=user_id).order_by(
                Expense.date.desc()
            ).limit(5).all()
            
            # Category breakdown
            category_breakdown = {}
            for expense in all_expenses:
                category_breakdown[expense.category] = category_breakdown.get(
                    expense.category, 0
                ) + expense.amount
            
            return render_template('dashboard.html',
                                   total_month=total_month,
                                   total_all=total_all,
                                   avg_all=round(avg_all, 2),
                                   max_all=max_all,
                                   recent_expenses=recent_expenses,
                                   category_breakdown=category_breakdown)
        
        return view()
    
    # Load user for login manager
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
