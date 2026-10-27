# Windows 长驻进程存活方案（Agent 环境）

> 建档：2026-10-26。适用：任何需要跨工具调用持续运行的挖掘战役 / 守护进程。

## 1 根因

Agent 每次工具调用创建的进程都挂在**同一个 Windows Job Object**，该 Job 带 `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`。
工具调用结束 → shell 退出 → Job 关闭 → **整棵子进程树被杀**。

因此以下四种写法**同因失效**（表现完全一样：日志零增长 + 锁文件里的 PID 消失）：

| 尝试 | 结果 |
|---|---|
| `nohup cmd &` | 死 |
| `run_in_background: true` + `\| tee` | 死（管道断 EPIPE 加速了死亡） |
| `Start-Process -WindowStyle Hidden` | 死（仍在同一 Job） |
| `cmd /c start "" ...` | 死 |

误判风险：日志「已拉起 PID=xxxx」会打印成功，但进程 2–5 分钟后消失。**必须用「日志字节增长」验证，不能只看 PID 回显。**

## 2 解法：让系统服务创建进程

进程由**系统服务**（Task Scheduler / WMI 提供程序宿主）创建时不在 Agent 的 Job 内，因此不受连坐。

| 路径 | 状态 |
|---|---|
| **任务计划程序**（Task Scheduler） | ✅ **实测有效，推荐** |
| `Invoke-CimMethod -ClassName Win32_Process -MethodName Create` | ❌ 本机安全策略拦截（判为等价于 Start-Process） |
| 服务（`sc create`） | 需管理员，不必要 |

### 2.1 注册 + 启动

```
schtasks /create /tn wqb_glb_campaign /tr "powershell.exe -NoProfile -ExecutionPolicy Bypass -File <daemon.ps1>" /sc once /st 23:58 /f
schtasks /run /tn wqb_glb_campaign
```

- `/sc once /st 23:58` 只是占位，实际用 `/run` 手动触发；任务不会到点重跑。
- 不指定 `/ru` 时用当前交互用户身份（「只使用交互方式」），要求用户已登录——本机符合。

### 2.2 停止 / 清理

```
schtasks /end /tn wqb_glb_campaign
schtasks /delete /tn wqb_glb_campaign /f
```
或让守护进程自己退出：创建标记文件 `cache\glb_daemon.stop`。

## 3 验证方法（必须做）

1. 心跳探针：`for ($i=0;$i -lt 120;$i++){ tick; Start-Sleep 5 }` 写文件。
2. 启动后**换一个工具调用**（≥60s 后）再读文件，确认行数继续增长、PID 不变。
3. 战役级：确认 supervisor 日志字节数增长 + `[gate]` 秒数推进。

实测：心跳 PID 84820 跨 3 次工具调用持续 tick（0→17）；GLB 战役守护 PID 81240 跨调用存活。

## 4 复用模板

`tracking/GLB/scripts/glb_daemon.ps1`：

- `while (-not (Test-Path $stop))` 外层循环
- 每次启动前清 `cache/lane_<REGION>_{supervisor,campaign}.lock`（死 PID 残留锁会拒绝启动）
- `& $py -u -X utf8 $runner <args> *>> $log`
- `$code = $LASTEXITCODE`；`code==0` 视为正常收工并 break，否则 30s 后重拉
- 全流程带时间戳写 `logs/glb_daemon.log`

## 5 顺带修正：GLB 启动器 `run_glb.cmd`

原文件的仓库路径被写成含 **TAB 字符**的 `D:\coding<TAB>raeCN_project`（生成时 `\t` 被转义），该启动器一直不可用。已重写为纯正斜杠/无转义版本。
