from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
import secrets

ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,
    parallelism=1,
    hash_len=32,
    salt_len=16
)

class PasswordUtil:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using Argon2"""
        return ph.hash(password)

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            ph.verify(hashed, password)
            if ph.check_needs_rehash(hashed):
                return True, True  # Valid but needs rehash
            return True, False  # Valid and up to date
        except (VerifyMismatchError, VerificationError):
            return False, False

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generate cryptographically secure random token"""
        return secrets.token_urlsafe(length)
