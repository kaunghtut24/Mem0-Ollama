<#
Windows PowerShell setup helper.
Run as: Open PowerShell (not admin required) and execute:
  powershell -ExecutionPolicy Bypass -File .\scripts\setup_windows.ps1
#>
Write-Host "Windows setup helper"

# Check python
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
  Write-Host "Python not found. Please install Python 3.10+ from https://www.python.org/downloads/"
} else {
  Write-Host "Python found: $($py.Version)"
}

# Check node
$nd = Get-Command node -ErrorAction SilentlyContinue
if (-not $nd) {
  Write-Host "Node.js not found. Please install Node.js 18+ from https://nodejs.org/"
} else {
  Write-Host "Node found: $((node --version))"
}

Write-Host ""
Write-Host "Follow steps in README.md. Use .env to configure your environment."
