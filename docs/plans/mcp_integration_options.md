# MCP 集成方案对比分析

## 背景
wqb-mcp 是一个 FastMCP 服务，支持两种传输模式：
- **stdio**: 通过标准输入输出通信（.mcp.json 配置）
- **streamable-http**: HTTP 服务器模式（Docker/手动启动）

当前 .mcp.json 配置使用 stdio 模式，由 Qoder 客户端自动启动。

---

## 方案对比

### 方案 1：直接 HTTP 调用（推荐）

**原理**：启动 wqb-mcp 的 HTTP 模式，pipeline 通过 HTTP 请求调用

**优点**：
- ✅ 无需修改 MCP 代码
- ✅ 标准 HTTP 协议，易于调试
- ✅ 支持异步/并发调用
- ✅ 与现有 stdio 模式共存（不同端口）

**缺点**：
- ⚠️ 需要额外启动 HTTP 服务
- ⚠️ 需要管理端口冲突

**实现**：
```python
# 启动 HTTP 模式（一次性）
# cd world-quant-brain-mcp && MCP_TRANSPORT=streamable-http python main.py

# pipeline 中调用
import requests

def create_multi_simulation(exprs, **kwargs):
    response = requests.post(
        "http://localhost:8000/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "create_multi_simulation",
                "arguments": {"expressions": exprs, **kwargs}
            }
        }
    )
    return response.json()
```

---

### 方案 2：Python 直接 import（最快落地）

**原理**：将 wqb-mcp 的 brain_api 作为库直接 import

**优点**：
- ✅ 无需启动额外服务
- ✅ 调用速度最快（无 IPC 开销）
- ✅ 代码最简洁

**缺点**：
- ⚠️ 需要处理依赖（redis 等）
- ⚠️ 与 MCP 服务版本可能不同步
- ⚠️ 需要 .env 凭据文件

**实现**：
```python
# pipeline/core/brain_direct.py
import sys
sys.path.insert(0, "world-quant-brain-mcp")

from brain_api import brain_client, load_config

def create_multi_simulation(exprs, **kwargs):
    # 直接调用 brain_client
    return brain_client.create_multi_simulation(exprs, **kwargs)
```

---

### 方案 3：子进程 stdio 通信（最复杂）

**原理**：pipeline 启动 wqb-mcp 子进程，通过 stdio 发送 JSON-RPC

**优点**：
- ✅ 与 Qoder 客户端行为一致
- ✅ 隔离性好

**缺点**：
- ❌ 实现复杂（需要管理子进程生命周期）
- ❌ stdio 通信效率低
- ❌ 调试困难
- ❌ 需要处理 JSON-RPC 协议细节

---

### 方案 4：文件队列（最简单但最慢）

**原理**：pipeline 写请求文件，MCP 服务轮询处理

**优点**：
- ✅ 实现最简单
- ✅ 无需网络/进程管理

**缺点**：
- ❌ 延迟高（轮询间隔）
- ❌ 需要文件锁管理
- ❌ 不适合实时性要求高的场景

---

## 推荐方案：方案 1（HTTP）+ 方案 2（直接 import）混合

### 架构设计

```
pipeline/
├── core/
│   ├── mcp_bridge.py          # MCP 桥接器（抽象层）
│   ├── mcp_http.py            # HTTP 模式实现
│   ├── mcp_direct.py          # 直接 import 实现
│   └── campaign_pipeline.py   # 使用桥接器
```

### 使用方式

```python
# 自动选择最佳模式
from pipeline.core.mcp_bridge import MCPBridge

# 优先 HTTP，fallback 到直接 import
bridge = MCPBridge(mode="auto")  # auto/http/direct

# 提交回测
result = bridge.create_multi_simulation(
    expressions=["rank(close)", "rank(volume)"],
    region="GBR",
    universe="TOP700",
    delay=1
)
```

---

## 立即可落地的代码

### 方案 2：直接 import（最快）

```python
# pipeline/core/mcp_direct.py
import os
import sys
from pathlib import Path

# 添加 MCP 目录到路径
MCP_DIR = Path(__file__).resolve().parent.parent.parent / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP_DIR))

# 设置环境变量（模拟 stdio 模式）
os.environ["MCP_TRANSPORT"] = "stdio"

from brain_api import brain_client, load_config

class DirectMCPClient:
    """直接 import 的 MCP 客户端"""
    
    def __init__(self):
        self.config = load_config()
        self.client = brain_client
    
    def create_multi_simulation(self, expressions, **kwargs):
        """创建批量模拟"""
        # 调用 brain_client 的批量模拟方法
        # 注意：需要查看 brain_api.py 的实际接口
        pass
    
    def get_simulation_status(self, sim_id):
        """查询模拟状态"""
        pass
```

### 方案 1：HTTP 模式

```python
# pipeline/core/mcp_http.py
import requests
import json

class HTTPMCPClient:
    """HTTP 模式的 MCP 客户端"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.mcp_path = "/mcp"
    
    def _call(self, tool_name, arguments):
        """调用 MCP 工具"""
        response = requests.post(
            f"{self.base_url}{self.mcp_path}",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            },
            timeout=300
        )
        return response.json()
    
    def create_multi_simulation(self, expressions, **kwargs):
        """创建批量模拟"""
        return self._call("create_multi_simulation", {
            "expressions": expressions,
            **kwargs
        })
```

---

## 决策建议

| 场景 | 推荐方案 | 理由 |
|:---|:---|:---|
| 快速验证 pipeline | 方案 2（直接 import） | 无需启动服务，代码最简 |
| 生产环境长期使用 | 方案 1（HTTP） | 与 Qoder 客户端解耦，可独立部署 |
| 调试/开发 | 方案 1（HTTP） | 易于抓包调试 |
| 资源受限环境 | 方案 2（直接 import） | 无额外进程开销 |

**当前建议**：先用方案 2（直接 import）快速落地，验证 pipeline 流程；后续再迁移到方案 1（HTTP）实现完全解耦。
