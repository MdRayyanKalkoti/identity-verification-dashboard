from flask import session
from functools import wraps
from flask import jsonify

def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({'error': 'Unauthorized', 'locked': True}), 401
        return f(*args, **kwargs)
    return decorated_function

def verify_password(provided_password, correct_password):
    """Verify password with timing-safe comparison"""
    import hmac
    return hmac.compare_digest(
        provided_password.encode('utf-8'),
        correct_password.encode('utf-8')
    )