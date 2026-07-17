$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $repoRoot

$preferredNodeRoot = Join-Path $env:USERPROFILE ".nvmd\versions\24.3.0"
if ((Test-Path (Join-Path $preferredNodeRoot "node.exe")) -and (Test-Path (Join-Path $preferredNodeRoot "npx.cmd"))) {
  $env:Path = "$preferredNodeRoot;$env:Path"
}

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
  throw "Node.js is unavailable. Run package.bat -CheckOnly to diagnose the local toolchain."
}

$env:EXPO_PUBLIC_DEV_UI = "1"
$env:EXPO_PUBLIC_API_MODE = "mock"

Write-Host "Starting Expo Web with the development UI enabled..." -ForegroundColor Cyan
$npxCommand = Join-Path $preferredNodeRoot "npx.cmd"
if (-not (Test-Path $npxCommand)) {
  $npxCommand = "npx.cmd"
}

& $npxCommand expo start --web
exit $LASTEXITCODE
