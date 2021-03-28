set -e
set -x

bash scripts/test.sh --cov-report=html --html=htmlcov/pytest-report.html --self-contained-html "${@}"