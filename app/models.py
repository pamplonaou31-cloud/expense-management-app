"""Database models."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """User model."""
    
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    expenses = db.relationship('Expense', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def get_total_expenses(self):
        """Get total expenses for user."""
        return sum(e.amount for e in self.expenses)
    
    def get_monthly_expenses(self, year, month):
        """Get monthly expenses for user."""
        from datetime import datetime as dt
        expenses = Expense.query.filter(
            Expense.user_id == self.id,
            db.func.strftime('%Y-%m', Expense.date) == f'{year:04d}-{month:02d}'
        ).all()
        return expenses
    
    def get_yearly_expenses(self, year):
        """Get yearly expenses for user."""
        expenses = Expense.query.filter(
            Expense.user_id == self.id,
            db.func.strftime('%Y', Expense.date) == f'{year:04d}'
        ).all()
        return expenses
    
    def __repr__(self):
        return f'<User {self.username}>'


class Expense(db.Model):
    """Expense model."""
    
    __tablename__ = 'expense'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False, index=True, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Expense {self.category}: ${self.amount}>'
    
    def to_dict(self):
        """Convert expense to dictionary."""
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date.isoformat(),
            'created_at': self.created_at.isoformat()
        }


class Category(db.Model):
    """Category model."""
    
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    icon = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Category {self.name}>'


# Default categories
DEFAULT_CATEGORIES = [
    {'name': 'Food & Dining', 'icon': '🍽️'},
    {'name': 'Transportation', 'icon': '🚗'},
    {'name': 'Shopping', 'icon': '🛍️'},
    {'name': 'Entertainment', 'icon': '🎬'},
    {'name': 'Utilities', 'icon': '💡'},
    {'name': 'Healthcare', 'icon': '⚕️'},
    {'name': 'Education', 'icon': '📚'},
    {'name': 'Other', 'icon': '📋'},
]
