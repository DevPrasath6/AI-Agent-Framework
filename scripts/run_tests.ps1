param(
    [string]$reporter = '.\scripts\run_tests_report.py'
)

try {
    # Ensure the repository root and `django_app` are on PYTHONPATH so pytest/pytest-django
    # can import the local Django apps (which are in the django_app/ directory)
    $repoRoot = (Get-Location).Path
    $djangoAppPath = Join-Path $repoRoot 'django_app'
    Write-Host "Setting PYTHONPATH=$djangoAppPath;$repoRoot"
    $env:PYTHONPATH = "$djangoAppPath;$repoRoot"
    Write-Host "Running advanced test reporter ($reporter)"
    python $reporter
} catch {
    Write-Host "Failed to run advanced reporter, falling back to pytest"
    & pytest
}
