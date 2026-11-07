# RESILIENCE SL: Pipeline Execution & Verification Script (PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  RESILIENCE SL: Research Workbench Pipeline Execution" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Resolve Python executable
$PYTHON = "python"
if (Test-Path ".venv\Scripts\python.exe") {
    $PYTHON = ".venv\Scripts\python.exe"
}

Write-Host "`n[Step 1/3] Generating verified V3 research tables..." -ForegroundColor Yellow
& $PYTHON scripts/generate_tables.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "Table generation failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host "`n[Step 2/3] Running automated pytest test suite (35+ tests)..." -ForegroundColor Yellow
$PYTEST = "pytest"
if (Test-Path ".venv\Scripts\pytest.exe") {
    $PYTEST = ".venv\Scripts\pytest.exe"
}
& $PYTEST -v --tb=short
if ($LASTEXITCODE -ne 0) {
    Write-Error "Test suite failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host "`n[Step 3/3] Verifying data integrity..." -ForegroundColor Yellow
& $PYTHON -c "from rsl.checksums import sha256_file; from pathlib import Path; p = Path('data/processed/panel_a_stratum_metrics.csv'); print(f'Verified panel_a_stratum_metrics.csv SHA-256: {sha256_file(p)}')"

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  SUCCESS: All pipeline steps and test verifications passed!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
