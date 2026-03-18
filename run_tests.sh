set -e
echo "Starting BULLETPROOF test execution..."
python -m pytest test_appointment.py test_integration.py -v --tb=short
exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo " ALL TESTS PASSED! BULLETPROOF FIX SUCCESSFUL"
else
    echo " Test execution failed with exit code: $exit_code"
    exit $exit_code
fi
