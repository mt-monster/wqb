' =====================================================================
' 停止 wq-brain-http (8000) 与 wqb-db (8001) 两个 MCP HTTP 常驻服务。
'
' 为什么用 VBS 而不是 BAT：本机双击 .bat 会被静默拦截（已实证）。
' 本文件调用 Python 停止器（stop_mcp_http_servers.py）精确找出并结束进程，
' 再把结果用 MessageBox 弹出来，不再"黑盒"。
'
' 用法：双击本文件 -> 结束两个服务并弹出结果
' =====================================================================
On Error Resume Next

Py      = "D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe"
Stopper = "D:\coding\traeCN_project\wqb\world-quant-brain-mcp\stop_mcp_http_servers.py"

Set ws = CreateObject("WScript.Shell")
cmd = """" & Py & """ """ & Stopper & """"

Set exec = ws.Exec(cmd)

out = ""
Do While Not exec.StdOut.AtEndOfStream
    out = out & exec.StdOut.ReadLine & vbCrLf
Loop

If Err.Number <> 0 Then
    MsgBox "执行失败：" & vbCrLf & Err.Description & vbCrLf & vbCrLf & "命令：" & cmd, _
           0, "MCP 关闭"
    WScript.Quit 1
End If

If out = "" Then out = "(无输出 —— 请确认 python 与 stop_mcp_http_servers.py 是否存在)"

MsgBox out, 0, "MCP 关闭结果"
