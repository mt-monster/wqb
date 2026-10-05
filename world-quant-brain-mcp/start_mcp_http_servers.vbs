' =====================================================================
' 启动 wq-brain-http (8000) 与 wqb-db (8001) 两个 MCP HTTP 常驻服务。
'
' 为什么用 VBS 而不是 BAT：本机双击 .bat 会被静默拦截（已实证——.bat 第一行
' 的 bat_trace.log 自痕从未生成）。VBS 由 wscript.exe 处理，双击可稳定执行。
' 本文件只是拉起 Python 启动器（start_mcp_http_servers.py），由后者用
' subprocess(DETACHED_PROCESS) 起两个服务并脱离窗口常驻。
'
' 用法：
'   双击本文件            -> 拉起两服务，弹出 python 窗口显示自检，回车关窗后服务继续
'   登录自启(Startup)     -> WQB_MCP_HTTP_Servers.vbs 以 "auto" 调用，不弹窗等待
'   关闭服务              -> 运行 stop_mcp_http_servers.bat，或任务管理器结束 python
' =====================================================================
On Error Resume Next

Py       = "D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe"
Launcher = "D:\coding\traeCN_project\wqb\world-quant-brain-mcp\start_mcp_http_servers.py"
LogDir   = "D:\coding\traeCN_project\wqb\world-quant-brain-mcp\logs"
Trace    = LogDir & "\vbs_trace.log"

arg = ""
If WScript.Arguments.Count > 0 Then arg = WScript.Arguments(0)

' --- 自痕：证明本 .vbs 确实被双击执行到（排查用）---
Set fso = CreateObject("Scripting.FileSystemObject")
If Not fso.FolderExists(LogDir) Then fso.CreateFolder(LogDir)
Set tf = fso.OpenTextFile(Trace, 8, True)   ' 8=追加, True=不存在则创建
tf.WriteLine(Now & " vbs-started arg=" & arg)
tf.Close

' --- 前置检查：确认 python 与启动器都在 ---
If Not fso.FileExists(Py) Then
    MsgBox "找不到 python 解释器：" & vbCrLf & Py, 0, "MCP 启动器"
    WScript.Quit 1
End If
If Not fso.FileExists(Launcher) Then
    MsgBox "找不到 Python 启动器：" & vbCrLf & Launcher, 0, "MCP 启动器"
    WScript.Quit 1
End If

' --- 拉起 Python 启动器（窗口样式 1=正常显示, False=不等待异步）---
cmd = """" & Py & """ """ & Launcher & """ " & arg
Set ws = CreateObject("WScript.Shell")
ws.Run cmd, 1, False

If Err.Number <> 0 Then
    MsgBox "MCP 启动失败：" & vbCrLf & Err.Description & vbCrLf & vbCrLf & "命令：" & cmd, _
           0, "MCP 启动器"
    WScript.Quit 1
End If
