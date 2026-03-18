"""
Validation script for authentication system
"""
import sys
import os
import importlib.util

def check_dependencies():
    """Check if all required dependencies are available"""
    required_packages = [
        'fastapi',
        'jose',
        'argon2',
        'pydantic',
        'sqlalchemy'
    ]

    for package in required_packages:
        try:
            __import__(package)
            print(f" {package} available")
        except ImportError:
            print(f" {package} missing")
            return False
    return True

def check_models():
    """Check if user models are properly defined"""
    try:
        from auth.models.user import User, PasswordResetToken
        print(" User models defined")
        return True
    except Exception as e:
        print(f" User models error: {e}")
        return False

def check_utils():
    """Check if utilities are properly defined"""
    try:
        from auth.utils.password import PasswordUtil
        from auth.utils.jwt import JWTUtil

        # Test password hashing
        hashed = PasswordUtil.hash_password("test123")
        assert hashed != "test123"
        print(" Password hashing works")

        # Test JWT token creation
        token = JWTUtil.create_access_token({"sub": "test"})
        assert token is not None
        print(" JWT token creation works")

        return True
    except Exception as e:
        print(f" Utility error: {e}")
        return False

if __name__ == "__main__":
    print("Validating authentication system...")

    checks = [
        check_dependencies,
        check_models,
        check_utils
    ]

    passed = 0
    for check in checks:
        if check():
            passed += 1

    print(f"\nPassed {passed}/{len(checks)} checks")
    if passed == len(checks):
        print("Authentication system validated successfully!")
        sys.exit(0)
    else:
        print("Some checks failed. Please review above.")
        sys.exit(1)
