echo "Setting up appointment booking system..."

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (for development)
npm init -y 2>/dev/null || true
npm install concurrently 2>/dev/null || true

echo "Setup complete!"
echo ""
echo "To start the system:"
echo "1. Make sure PostgreSQL is running and update .env.example to .env with your database details"
echo "2. Copy .env.example to .env and configure your email settings"
echo "3. Run: npm run dev"
echo ""
echo "API will be at http://localhost:8000"
echo "Frontend will be at http://localhost:3000"
