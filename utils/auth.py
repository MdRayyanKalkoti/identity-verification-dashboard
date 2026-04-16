# ============================================
# COMPLETE utils/auth.py FILE
# ============================================
# Replace your entire utils/auth.py with this

from functools import wraps
from flask import session, jsonify

def login_required(f):
    """
    Decorator to require authentication for routes
    
    Usage:
        @app.route('/protected')
        @login_required
        def protected_route():
            return 'Protected content'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function