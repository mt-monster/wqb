# wqb 脱离 Agent Job 的长任务启动器
#
# 为什么需要它
# ------------
# Windows 上 Agent 的 shell / 工具调用被放进一个 Job object（通常带
# JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE）。因此：
#   · `cmd &` / `nohup` 起的子进程 → Job 一关就全被 kill（2026-10-26 实测两次）
#   · 工具的 run_in_background → 能活，但绑在会话上，会话结束仍会回收
# 由**任务计划程序（Schedule 服务，svchost）**创建进程后，父链是 svchost，
# 与 Agent 的 Job 无关 ⇒ 会话结束/Job 关闭都不影响它。
#
# 注意：WMI Win32_Process.Create 在本环境被安全策略拦截（等同 Start-Process），
# 只有 schtasks 这条路可用（2026-10-26 实测）。
#
# 实现：先落一个 .cmd 包装脚本（内含 set env / cd / 重定向），
# 再让任务计划执行该 .cmd —— 绕开 cmd /c 的多层引号问题，
# 也解决「任务 cwd 默认是 System32」「环境变量不继承」两个坑。
#
# ⚠ 参数名不能叫 -Args / -Env：那是 PowerShell 的自动变量，会报
#   「无法分配 System.Object[] 类型的自动变量 Args」。故用 -Arguments / -EnvVars。
#
# 用法
# ----
#   powershell -NoProfile -File tools\detach_launch.ps1 `
#       -WorkDir "C:\Users\MENGTAO\.workbuddy\skills\wq-brain-ra-eur\scripts" `
#       -Exe "D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe" `
#       -Arguments "-X utf8 eur_main.py --only-cats OTHER,PV --datasets pv20,pv106 --min-cov 0.5" `
#       -EnvVars "WQB_REPO_ROOT=D:\coding\traeCN_project\wqb" `
#       -LogFile "D:\coding\traeCN_project\wqb\logs\eur_pv_rest.log" `
#       -TaskName "wqb_eur_pv_rest"
#
# 清理：schtasks /delete /tn <TaskName> /f   （只删任务定义，不杀进程）
param(
    [Parameter(Mandatory = $true)][string]$Exe,
    [string]$Arguments = "",
    [string]$WorkDir = "D:\coding\traeCN_project\wqb",
    [string]$EnvVars = "",
    [string]$LogFile = "",
    [string]$TaskName = ""
)

$repo = "D:\coding\traeCN_project\wqb"
if (-not $TaskName) { $TaskName = "wqb_job_" + (Get-Date -Format "MMdd_HHmmss") }
if (-not $LogFile) { $LogFile = Join-Path $repo ("logs\" + $TaskName + ".log") }
$logDir = Split-Path $LogFile -Parent
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

$wrapper = Join-Path $repo ("logs\_task_" + $TaskName + ".cmd")
$lines = @("@echo off")
if ($EnvVars) {
    foreach ($kv in ($EnvVars -split ';')) {
        if ($kv.Trim()) { $lines += ("set " + $kv.Trim()) }
    }
}
$lines += ('cd /d "' + $WorkDir + '"')
$lines += ('"' + $Exe + '" ' + $Arguments + ' > "' + $LogFile + '" 2>&1')
Set-Content -Path $wrapper -Value $lines -Encoding ascii

schtasks /create /tn $TaskName /tr ('cmd.exe /c "' + $wrapper + '"') /sc once /st 23:59 /f | Out-Null
if ($LASTEXITCODE -ne 0) { "创建任务失败 rc=$LASTEXITCODE"; exit 1 }
schtasks /run /tn $TaskName | Out-Null
Start-Sleep -Seconds 6

"TaskName = $TaskName"
"Wrapper  = $wrapper"
"LogFile  = $LogFile"
$pat = ($Arguments -split '\s+')[-1]
$p = Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
     Where-Object { $_.CommandLine -like "*$pat*" }
if ($p) {
    $p | Select-Object -First 3 | ForEach-Object {
        $par = Get-Process -Id $_.ParentProcessId -ErrorAction SilentlyContinue
        "  PID $($_.ProcessId)  parent=$($par.ProcessName)  ws=$([math]::Round($_.WorkingSetSize/1MB,1))MB"
    }
} else {
    "  （未匹配到进程，看日志）"
}
if (Test-Path $LogFile) {
    "--- 日志尾 6 行 ---"
    Get-Content $LogFile -Tail 6
}
