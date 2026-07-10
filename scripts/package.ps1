param(
  [ValidateSet("android", "web")]
  [string]$Target = "android",

  [ValidateSet("preview", "production")]
  [string]$Profile = "preview",

  [ValidateSet("", "mock", "real")]
  [string]$ApiMode = "",

  [switch]$SkipInstall,
  [switch]$Clean,
  [switch]$NonInteractive,
  [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"

function Write-Step {
  param([string]$Message)
  Write-Host ""
  Write-Host "==> $Message" -ForegroundColor Cyan
}

function Require-Command {
  param([string]$Name)
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
    throw "Required command '$Name' was not found. Please install it or add it to PATH."
  }
}

function Test-CommandVersion {
  param([string]$Name)
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
    return $false
  }

  try {
    & $Name --version | Out-Null
    return $LASTEXITCODE -eq 0
  } catch {
    return $false
  }
}

function Enable-LocalNode {
  $VersionRoot = Join-Path $env:USERPROFILE ".nvmd\versions"
  $Candidates = @()
  $PreferredRoot = Join-Path $VersionRoot "24.3.0"

  if (Test-Path $PreferredRoot) {
    $Candidates += $PreferredRoot
  }

  if (Test-Path $VersionRoot) {
    $InstalledRoots = Get-ChildItem -LiteralPath $VersionRoot -Directory |
      Sort-Object { [version]$_.Name } -Descending |
      ForEach-Object { $_.FullName }
    $Candidates += $InstalledRoots
  }

  foreach ($Candidate in ($Candidates | Select-Object -Unique)) {
    $NodePath = Join-Path $Candidate "node.exe"
    $NpmPath = Join-Path $Candidate "npm.cmd"
    if ((Test-Path $NodePath) -and (Test-Path $NpmPath)) {
      $env:Path = "$Candidate;$env:Path"
      if ((Test-CommandVersion "node") -and (Test-CommandVersion "npm")) {
        return $Candidate
      }
    }
  }

  return $null
}

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

if (-not (Test-Path "package.json")) {
  throw "package.json was not found. Run this script from the project repository."
}

Write-Step "Checking local toolchain"
if ((-not (Test-CommandVersion "node")) -or (-not (Test-CommandVersion "npm"))) {
  $EnabledNode = Enable-LocalNode
  if ($EnabledNode) {
    Write-Step "Using Node from $EnabledNode"
  }
}

if ((-not (Test-CommandVersion "node")) -or (-not (Test-CommandVersion "npm"))) {
  if (Get-Command "nvmd" -ErrorAction SilentlyContinue) {
    Write-Step "Activating Node 24.3.0 with nvmd"
    nvmd use 24.3.0
  }
}

Require-Command "node"
Require-Command "npm"

if ((-not (Test-CommandVersion "node")) -or (-not (Test-CommandVersion "npm"))) {
  throw "Node/npm is not available. Try running package.bat directly, or run 'nvmd use 24.3.0' in a new terminal."
}

node --version
npm --version

if ($ApiMode -ne "") {
  Write-Step "Using EXPO_PUBLIC_API_MODE=$ApiMode"
  $env:EXPO_PUBLIC_API_MODE = $ApiMode
}

if (-not (Test-Path "node_modules")) {
  if ($SkipInstall) {
    throw "node_modules is missing, and -SkipInstall was provided."
  }

  Write-Step "Installing npm dependencies"
  npm install
}

if ($CheckOnly) {
  Write-Step "Package script check completed"
  exit 0
}

$DistRoot = Join-Path $RepoRoot "dist"
$PackageDir = Join-Path $DistRoot "packages"
$WebDir = Join-Path $DistRoot "web"
New-Item -ItemType Directory -Force -Path $PackageDir | Out-Null

if ($Clean) {
  Write-Step "Cleaning previous package output"
  $ResolvedDist = Resolve-Path $DistRoot
  if (-not $ResolvedDist.Path.StartsWith($RepoRoot.Path)) {
    throw "Refusing to clean outside repository: $($ResolvedDist.Path)"
  }

  if ($Target -eq "web" -and (Test-Path $WebDir)) {
    Remove-Item -LiteralPath $WebDir -Recurse -Force
  }

  if ($Target -eq "android") {
    Get-ChildItem -LiteralPath $PackageDir -File -Filter "dujia-tonghua-android-$Profile-*" |
      Remove-Item -Force
  }
}

if ($Target -eq "web") {
  Write-Step "Exporting Expo web build"
  npx expo export --platform web --output-dir $WebDir
  Write-Step "Web package created at $WebDir"
  exit 0
}

$Extension = if ($Profile -eq "production") { "aab" } else { "apk" }
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$OutputFile = Join-Path $PackageDir "dujia-tonghua-android-$Profile-$Timestamp.$Extension"

$EasArgs = @(
  "eas-cli@latest",
  "build",
  "--platform", "android",
  "--profile", $Profile,
  "--local",
  "--output", $OutputFile
)

if ($NonInteractive) {
  $EasArgs += "--non-interactive"
}

Write-Step "Building Android package with EAS local build"
npx --yes @EasArgs

Write-Step "Android package created at $OutputFile"
