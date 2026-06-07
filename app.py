#!/usr/bin/env python
"""Main Flask application entry point."""

import os
from app import create_app, db
from app.models import User, Expense, Category

config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)


@app.shell_context_processor
def make_shell_context():
    """Create shell context for flask shell."""
    return {'db': db, 'User': User, 'Expense': Expense, 'Category': Category}


@app.before_request
def before_request():
    """Tasks to run before each request."""
    pass


@app.after_request
def after_request(response):
    """Tasks to run after each request."""
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return {'error': 'Not found'}, 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return {'error': 'Internal server error'}, 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
