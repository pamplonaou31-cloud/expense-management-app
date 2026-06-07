"""Utility functions."""

from datetime import datetime, timedelta
from functools import wraps
from flask import redirect, url_for
from flask_login import current_user


def login_required_custom(f):
    """Custom login required decorator."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def format_currency(amount):
    """Format amount as currency."""
    return f'${amount:,.2f}'


def format_date(date_obj):
    """Format date object to string."""
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime('%Y-%m-%d') if date_obj else ''


def get_month_name(month_num):
    """Get month name from month number."""
    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    if 1 <= month_num <= 12:
        return months[month_num - 1]
    return ''


def get_date_range(range_type='month'):
    """Get date range based on type."""
    today = datetime.now().date()
    
    if range_type == 'month':
        month_start = datetime(today.year, today.month, 1).date()
        if today.month == 12:
            month_end = datetime(today.year + 1, 1, 1).date() - timedelta(days=1)
        else:
            month_end = datetime(today.year, today.month + 1, 1).date() - timedelta(days=1)
        return month_start, month_end
    
    elif range_type == 'year':
        year_start = datetime(today.year, 1, 1).date()
        year_end = datetime(today.year, 12, 31).date()
        return year_start, year_end
    
    elif range_type == 'week':
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        return week_start, week_end
    
    elif range_type == 'all':
        return None, None
    
    return today, today


def parse_date_str(date_str):
    """Parse date string to date object."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None


def get_percentage(part, total):
    """Calculate percentage."""
    if total == 0:
        return 0
    return round((part / total) * 100, 2)
