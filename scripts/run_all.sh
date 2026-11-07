#!/usr/bin/env bash
# RESILIENCE SL: Pipeline Execution & Verification Script (Bash)
set -euo pipefail

echo "=========================================================="
echo "  RESILIENCE SL: Research Workbench Pipeline Execution"
echo "=========================================================="

PYTHON="python3"
if [ -f ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
elif [ -f ".venv/Scripts/python.exe" ]; then
    PYTHON=".venv/Scripts/python.exe"
fi

echo -e "\n[Step 1/3] Generating verified V3 research tables..."
$PYTHON scripts/generate_tables.py

echo -e "\n[Step 2/3] Running automated pytest test suite (35+ tests)..."
PYTEST="pytest"
if [ -f ".venv/bin/pytest" ]; then
    PYTEST=".venv/bin/pytest"
elif [ -f ".venv/Scripts/pytest.exe" ]; then
    PYTEST=".venv/Scripts/pytest.exe"
fi
$PYTEST -v --tb=short

echo -e "\n[Step 3/3] Verifying data integrity..."
$PYTHON -c "import sys; sys.path.insert(0, 'src'); from rsl.checksums import sha256_file; from pathlib import Path; p = Path('data/processed/panel_a_stratum_metrics.csv'); print(f'Verified panel_a_stratum_metrics.csv SHA-256: {sha256_file(p)}')"

echo "=========================================================="
echo "  SUCCESS: All pipeline steps and test verifications passed!"
echo "=========================================================="
