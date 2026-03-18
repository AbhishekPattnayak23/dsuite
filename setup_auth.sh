set -e

echo "Setting up authentication system..."

# Install dependencies
pip install -r auth/requirements.txt

# Create database tables
python -c "
from db.session import engine
from auth.models.user import Base
Base.metadata.create_all(bind=engine)
print('Database tables created')
"

# Run validation
python validate_auth.py

echo "Authentication system setup complete!"
