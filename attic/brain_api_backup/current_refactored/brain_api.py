#!/usr/bin/env python3
"""brain_api - BRAIN API 客户端门面 (P0 拆解: 模型 / transport / auth / simulation / spcdata / correlation 分包)。

纯数据模型见 brain_api_models.py；配置函数见 brain_config.py；客户端方法按职责拆到
brain_mixin_*.py (TransportMixin / AuthMixin / SimulationMixin / SpcDataMixin / CorrelationMixin)。
BrainApiClient 仅继承这些 mixin 并保持全部公开方法名与模块级单例 brain_client 不变，
以满足 ``from brain_api import brain_client / BrainApiClient / load_config / SimulationSettings`` 等旧导入路径。
"""

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from brain_api_models import (  # noqa: F401
    AuthCredentials,
    SimulationData,
    SimulationSettings,
)
from brain_config import (  # noqa: F401
    load_config,
    _resolve_config_path,
    _load_dotenv_into_environ,
)

from brain_mixin_transport import TransportMixin
from brain_mixin_auth import AuthMixin
from brain_mixin_simulation import SimulationMixin
from brain_mixin_spcread import SpcDataMixin
from brain_mixin_correlation import CorrelationMixin


class BrainApiClient(TransportMixin, AuthMixin, SimulationMixin, SpcDataMixin, CorrelationMixin):
    """WorldQuant BRAIN API client. Methods are inherited from the brain_mixin_* modules."""


brain_client = BrainApiClient()
