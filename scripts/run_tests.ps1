param(
    [string]$pytest = 'pytest'
)
try {
    Write-Host "Running tests with $pytest"
    & $pytest
} catch {
    Write-Host "pytest not available, falling back to python script runner"
    python .\scripts\run_tests.py
}
