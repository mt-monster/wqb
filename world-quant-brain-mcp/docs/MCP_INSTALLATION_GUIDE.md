# WorldQuant BRAIN MCP 安装与配置指南

## 概述

这是 WorldQuant BRAIN 的 MCP（Model Context Protocol）服务器，提供了 50+ 个工具用于：
- Alpha 表达式创建与验证
- 数据集与字段探索
- 批量仿真与性能诊断
- Alpha 提交与监控
- 用户账户与金字塔信息
- 论坛搜索与交流

**MCP 服务器位置：** `D:\coding\traeCN_project\wqb\world-quant-brain-mcp`  
**默认监听端口：** `localhost:8876` (可配置)

---

## 方案 A: 本地 Python 运行（推荐用于开发）

### 前置条件

1. **Python 3.9+** 已安装
2. **Redis** 已安装或运行
   ```cmd
   redis-server
   ```
3. **WorldQuant BRAIN 账号** 凭证

### 安装步骤

#### 1. 准备环境

```cmd
cd D:\coding\traeCN_project\wqb\world-quant-brain-mcp
```

#### 2. 安装依赖

```cmd
# 如果还未安装 venv
python -m venv .venv

# 激活虚拟环境
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

#### 3. 配置凭证

编辑 `.env` 文件：
```dotenv
CREDENTIALS_EMAIL="your_brain_email@example.com"
CREDENTIALS_PASSWORD="your_brain_password"

# 可选
FORUM_SETTINGS_HEADLESS=true
FORUM_SETTINGS_TIMEOUT=180
API_SETTINGS_TIMEOUT=180
```

#### 4. 启动 MCP 服务

```cmd
python main.py
```

预期输出：
```
running the server
[INFO] Redis connection established successfully
[INFO] FastMCP server started on http://localhost:8876
```

---

## 方案 B: Docker 运行（推荐用于生产）

### 前置条件

- Docker Desktop 已安装

### 启动步骤

```cmd
cd D:\coding\traeCN_project\wqb\world-quant-brain-mcp

# 构建镜像
docker build -t wq-brain-mcp .

# 启动容器
docker run -d \
  --name wq-brain-mcp \
  -p 8876:8876 \
  -e CREDENTIALS_EMAIL="your_email" \
  -e CREDENTIALS_PASSWORD="your_password" \
  wq-brain-mcp
```

---

## 在 Claude 中配置 MCP

### 方案 1: Claude Desktop App (推荐)

1. **找到 Claude 配置文件**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **编辑配置文件** (如不存在则创建)

```json
{
  "mcpServers": {
    "wq-brain-http": {
      "command": "python",
      "args": [
        "D:/coding/traeCN_project/wqb/world-quant-brain-mcp/main.py"
      ],
      "disabled": false,
      "alwaysAllow": [
        "authenticate",
        "get_user_profile",
        "get_datasets",
        "create_multi_simulation",
        "submit_alpha",
        "check_correlation"
      ]
    }
  }
}
```

3. **重启 Claude Desktop**

4. **验证连接**
   - 在 Claude 中尝试调用工具（见下方工具列表）

### 方案 2: 网络连接（远程 MCP）

如果 MCP 服务运行在其他机器：

```json
{
  "mcpServers": {
    "wq-brain-http-remote": {
      "url": "http://remote-machine-ip:8876/mcp",
      "type": "http",
      "disabled": false
    }
  }
}
```

---

## MCP 工具清单

### 账户与认证 (tools_account)
- `authenticate()` - 认证 BRAIN 账号
- `get_user_profile()` - 获取用户信息
- `get_user_activities()` - 获取用户活动记录
- `get_leaderboard()` - 获取排行榜
- `get_pyramid_multipliers()` - 获取金字塔倍数
- `get_events()` - 获取最近事件

### Alpha 管理 (tools_alpha)
- `batch_get_alpha_metrics()` - 批量获取 Alpha 指标
- `get_alpha_details()` - 获取 Alpha 详情
- `get_alpha_pnl()` - 获取 Alpha 收益曲线
- `get_user_alphas()` - 获取用户所有 Alpha
- `set_alpha_properties()` - 修改 Alpha 属性
- `get_record_sets()` - 获取 Alpha 记录集

### 数据与字段 (tools_data)
- `get_datasets()` - 获取数据集列表
- `get_datafields()` - 获取字段列表
- `get_operators()` - 获取可用操作符
- `run_selection()` - 运行字段选择
- `recommend_datasets()` - 推荐数据集
- `value_factor_trendScore()` - 获取因子趋势得分

### 仿真 (tools_sim)
- `create_multi_simulation()` - 创建批量仿真 ⭐
- `create_simulation()` - 创建单个仿真
- `get_simulation_result()` - 获取仿真结果
- `run_diagnostics()` - 运行诊断
- `simulate_with_instrumentation()` - 带检测的仿真

### 提交与配额 (tools_submit)
- `submit_alpha()` - 提交 Alpha
- `get_submission_quota()` - 获取提交配额
- `query_submission_status()` - 查询提交状态
- `cancel_submission()` - 取消提交

### 相关性检查 (tools_corr)
- `check_correlation()` - 检查与其他 Alpha 的相关性
- `check_self_correlation()` - 检查自相关性
- `compute_mutual_correlation()` - 计算相互相关性

### 论坛与知识库 (tools_forum)
- `search_forum_posts()` - 搜索论坛帖子
- `read_forum_post()` - 读取论坛帖子
- `get_messages()` - 获取消息
- `get_glossary_terms()` - 获取术语表

### Brain Labs (tools_labs)
- `authenticate_brainlabs()` - 认证 Brain Labs
- `emit_labs_script()` - 发送 Labs 脚本
- `ingest_labs_result()` - 导入 Labs 结果

### 配置 (tools_config)
- `manage_config()` - 管理系统配置

### 运维 (tools_ops)
- `operator_audit()` - 操作符审计
- `batch_status()` - 批处理状态
- `submit_verdict()` - 提交判定
- `sa_probe()` - 超级 Alpha 探针
- `submit_batch()` - 提交批处理

---

## 验证安装

### 1. 检查 MCP 服务状态

```cmd
# Windows - 检查进程
netstat -ano | findstr :8876

# 或在 Redis CLI 中验证连接
redis-cli ping
```

### 2. 在 Claude 中测试工具

在 Claude 中尝试以下操作：

```
调用 authenticate 工具进行身份验证
```

预期返回：
```json
{
  "authenticated": true,
  "user_id": "your_user_id",
  "email": "mthyzx@126.com"
}
```

### 3. 列出所有可用工具

在 Claude 中请求：
```
列出我可用的所有 WorldQuant BRAIN MCP 工具
```

Claude 应该显示 50+ 个可用工具。

---

## 常见问题

### Q1: "Redis connection failed"

**原因：** Redis 服务未运行  
**解决：**
```cmd
# 启动 Redis
redis-server

# 或使用 Docker
docker run -d -p 6379:6379 redis:latest
```

### Q2: "Authentication failed"

**原因：** .env 中的凭证错误  
**解决：**
1. 编辑 `.env` 文件
2. 验证邮箱和密码正确
3. 重启 MCP 服务

### Q3: "MCP server not responding"

**原因：** 服务未启动或端口被占用  
**解决：**
```cmd
# 查看是否有进程占用 8876
netstat -ano | findstr :8876

# 杀死占用进程
taskkill /PID <PID> /F

# 重启服务
python main.py
```

### Q4: Claude 中看不到 MCP 工具

**原因：** Claude 配置文件未更新或格式错误  
**解决：**
1. 检查 `claude_desktop_config.json` 路径
2. 验证 JSON 格式正确（使用 JSON 验证器）
3. 完全关闭并重启 Claude Desktop

---

## 生产部署建议

### 1. 系统服务化 (Windows)

使用 NSSM 将 Python 应用注册为服务：

```cmd
nssm install WQBrainMCP python.exe D:\path\to\main.py
nssm start WQBrainMCP
```

### 2. 环境变量管理

创建 `.env.production`：
```dotenv
CREDENTIALS_EMAIL="prod_email@company.com"
CREDENTIALS_PASSWORD="prod_password"
REDIS_URL="redis://redis-server:6379"
LOG_LEVEL="INFO"
```

### 3. 日志监控

```cmd
# 将日志重定向到文件
python main.py >> logs/mcp_server.log 2>&1
```

### 4. 健康检查

定期检查服务健康：
```python
import requests
response = requests.get("http://localhost:8876/health")
assert response.status_code == 200
```

---

## 卸载/清理

### 停止服务

```cmd
# 找到 Python 进程并停止
taskkill /IM python.exe /F

# 或停止 Docker 容器
docker stop wq-brain-mcp
docker rm wq-brain-mcp
```

### 删除配置

1. 从 Claude 配置中删除 `wq-brain-http` / `wqb-db` 条目
2. （可选）删除 MCP 目录或 venv

---

## 支持与文档

- **README：** `D:\coding\traeCN_project\wqb\world-quant-brain-mcp\README.md`
- **配置示例：** `.env.example`
- **API 文档：** `docs/` 目录

祝你使用愉快! 🚀
