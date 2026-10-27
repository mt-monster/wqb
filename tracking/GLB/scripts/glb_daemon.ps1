# GLB campaign daemon — launched by Windows Task Scheduler (outside agent Job Object)
$ErrorActionPreference = 'Continue'
$repo   = 'D:\coding\traeCN_project\wqb'
$log    = Join-Path $repo 'logs\glb_daemon.log'
$stop   = Join-Path $repo 'cache\glb_daemon.stop'
$py     = Join-Path $repo 'world-quant-brain-mcp\.venv\Scripts\python.exe'
$runner = Join-Path $env:USERPROFILE '.workbuddy\skills\wq-brain-ra-glb\scripts\glb_runner.py'
$datasets = 'other455,pv30,pv37,techindi_model,predictive_starmine'

$env:WQB_REPO_ROOT = $repo
$env:WQB_CAMPAIGN_REGION = 'GLB'
Set-Location $repo

function Write-Log([string]$msg) {
  "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $msg" | Out-File -Append -Encoding utf8 $log
}

Write-Log "[daemon] boot pid=$PID"
if (Test-Path $stop) { Write-Log "[daemon] stop flag present at boot, exit"; exit 0 }

$attempt = 0
while (-not (Test-Path $stop)) {
  $attempt++
  Remove-Item (Join-Path $repo 'cache\lane_GLB_supervisor.lock') -Force -ErrorAction SilentlyContinue
  Remove-Item (Join-Path $repo 'cache\lane_GLB_campaign.lock') -Force -ErrorAction SilentlyContinue
  Write-Log "[daemon] run #$attempt starting (datasets=$datasets)"
  & $py -u -X utf8 $runner --datasets $datasets --min-cov 0.85 --require-ten-years --max-inflight 1 --stall-sec 1800 --check-sec 60 --zero-alpha-stop 3 *>> $log
  $code = $LASTEXITCODE
  Write-Log "[daemon] run #$attempt exited code=$code"
  if ($code -eq 0) { Write-Log "[daemon] clean exit -> stop"; break }
  Start-Sleep -Seconds 30
}
Write-Log "[daemon] terminated"
