# ============================================
# COMPLETE utils/security.py FILE
# ============================================
# Replace your entire utils/security.py with this

def validate_password(provided_password, expected_password):
    """
    Validate provided password against expected password
    
    Args:
        provided_password (str): Password provided by user
        expected_password (str): Expected password from config
    
    Returns:
        bool: True if passwords match, False otherwise
    """
    if not provided_password or not expected_password:
        return False
    
    # Simple string comparison
    # In production, you might want to use password hashing
    return provided_password == expected_password


def sanitize_input(text):
    """
    Sanitize user input to prevent XSS and injection attacks
    
    Args:
        text (str): Input text to sanitize
    
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Remove potential HTML tags
    import re
    text = re.sub(r'<[^>]*>', '', str(text))
    
    # Remove potential script tags
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    return text.strip()


def generate_secure_token(length=32):
    """
    Generate a secure random token
    
    Args:
        length (int): Length of token to generate
    
    Returns:
        str: Secure random token
    """
    import secrets
    import string
    
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))