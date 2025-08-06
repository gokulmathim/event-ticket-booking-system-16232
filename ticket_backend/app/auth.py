import hashlib

# PUBLIC_INTERFACE
def hash_password(password: str) -> str:
    """
    Hash a password for storage (very basic, not recommended for production!).
    """
    return hashlib.sha256(password.encode()).hexdigest()

# PUBLIC_INTERFACE
def verify_password(password: str, hash_value: str) -> bool:
    """
    Verify a plain password against its hash.
    """
    return hash_password(password) == hash_value
