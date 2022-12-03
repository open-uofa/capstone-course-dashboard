#!/bin/bash

# This script can be used to format the backend code.
cd $(dirname "$0")

echo "Checking backend code..."
echo "====================isort===================="
isort --profile black server/ tests/
echo "====================black===================="
black server/ tests/
echo "====================pylint(server)==========="
pylint server/
echo "====================pylint(tests)============"
pylint --rcfile=tests/.pylintrc tests/
echo "Complete."
