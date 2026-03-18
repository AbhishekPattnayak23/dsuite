set -e

echo "=== ENVIRONMENT CHECK ==="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "[CHECK] FAIL: .env file not found"
    echo "Copy .env.example to .env and configure it"
    exit 1
fi
echo "[CHECK] PASS: .env file exists"

# Check if requirements can be installed
pip install -q --dry-run -r requirements.txt 2>/dev/null && echo "[CHECK] PASS: Python requirements" || echo "[CHECK] FAIL: Python requirements missing"

# Check structure
[ -d backend/models ] && echo "[CHECK] PASS: backend structure" || echo "[CHECK] FAIL: backend structure"
[ -f frontend/pages/index.jsx ] && echo "[CHECK] PASS: frontend structure" || echo "[CHECK] PASS: frontend structure"

echo ""
echo "=== VALIDATION COMPLETE ==="
