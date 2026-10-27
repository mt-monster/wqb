# install.ps1 - wire this directory as git core.hooksPath (Windows twin of install.sh).
#
# Why: core.hooksPath is a LOCAL git config and is NOT stored in the repo, so a fresh
# clone has NO hooks active - pre-commit (audit_structure / doc_path_refs /
# destructive_default / pytest) and commit-msg silently never run. That is the root
# cause behind the 27 violations found by the 2026-10-24 repo audit.
#
# Usage (from repo root):
#   powershell -ExecutionPolicy Bypass -File tools\git-hooks\install.ps1
#   powershell -ExecutionPolicy Bypass -File tools\git-hooks\install.ps1 -Check
#   powershell -ExecutionPolicy Bypass -File tools\git-hooks\install.ps1 -Unset
#
# NOTE: this file is intentionally ASCII-only. Windows PowerShell 5.1 reads .ps1 as
# ANSI unless a UTF-8 BOM is present; non-ASCII text silently garbles and breaks parsing.

param(
    [switch]$Check,
    [switch]$Unset
)

$ErrorActionPreference = 'Stop'

$HooksDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent (Split-Path -Parent $HooksDir)
$RelHooks = 'tools/git-hooks'

if (-not (Test-Path (Join-Path $RepoRoot '.git'))) {
    Write-Error "Not a git repository: $RepoRoot"
}

$current = ''
try {
    $out = & git -C $RepoRoot config core.hooksPath 2>$null
    if ($LASTEXITCODE -eq 0 -and $out) { $current = [string]$out }
} catch {
    $current = ''
}

if ($Check) {
    if ($current -eq $RelHooks) {
        Write-Host "[install-hooks] OK: core.hooksPath=$RelHooks"
        exit 0
    }
    $shown = if ($current) { $current } else { '<unset>' }
    Write-Host "[install-hooks] MISSING: core.hooksPath=[$shown], expected [$RelHooks]" -ForegroundColor Yellow
    exit 1
}

if ($Unset) {
    & git -C $RepoRoot config --unset core.hooksPath 2>$null | Out-Null
    Write-Host "[install-hooks] core.hooksPath unset (back to .git/hooks)"
    exit 0
}

& git -C $RepoRoot config core.hooksPath $RelHooks
Write-Host "[install-hooks] wired: core.hooksPath=$RelHooks"

$active = @(Get-ChildItem -Path $HooksDir -File |
    Where-Object { $_.Name -notin @('install.sh', 'install.ps1', 'README.md') } |
    ForEach-Object { $_.Name })
Write-Host "[install-hooks] active hooks: $($active -join ' ')"
