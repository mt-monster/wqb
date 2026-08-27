from __future__ import annotations
import logging
import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

def _resolve_config_path(for_write: bool = False) -> str:
    """
    Resolve the configuration file path.
    
    Checks for a file specified by the MCP_CONFIG_FILE environment variable,
    then falls back to ~/.brain_mcp_config.json. If for_write is True,
    it ensures the directory exists.
    """
    if 'MCP_CONFIG_FILE' in os.environ:
        return os.environ['MCP_CONFIG_FILE']
    
    config_path = Path(__file__).parent / "user_config.json"
    
    if for_write:
        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
        except (IOError, OSError) as e:
            logger.warning(f"Could not create config directory {config_path.parent}: {e}")
            # Fallback to a temporary file if home is not writable
            import tempfile
            return tempfile.NamedTemporaryFile(delete=False).name
            
    return str(config_path)

def _load_dotenv_into_environ():
    """Load .env into environment using python-dotenv if available; fallback to simple parser."""
    try:
        from dotenv import load_dotenv, find_dotenv
        env_path = find_dotenv(usecwd=True)
        if env_path:
            load_dotenv(env_path, override=False)
        else:
            # Try repo root relative to this file
            candidate = Path(__file__).parent / ".env"
            if candidate.exists():
                load_dotenv(candidate, override=False)
    except Exception:
        # Fallback: very simple .env parser (KEY=VALUE, no export, ignores quotes)
        try:
            candidate = Path(__file__).parent / ".env"
            if candidate.exists():
                for line in candidate.read_text().splitlines():
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' not in line:
                        continue
                    k, v = line.split('=', 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    os.environ.setdefault(k, v)
        except Exception:
            logging.getLogger(__name__).debug("swallowed exception", exc_info=True)

def load_config() -> Dict[str, Any]:
    """Load configuration from file and overlay environment variables (from .env if present)."""
    config: Dict[str, Any] = {}
    config_file = _resolve_config_path()
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f) or {}
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Error loading config file {config_file}: {e}")

    # Load .env into environment (no override of already-set env)
    _load_dotenv_into_environ()

    # Overlay credentials from env if available
    env_email = os.getenv("CREDENTIALS_EMAIL")
    env_password = os.getenv("CREDENTIALS_PASSWORD")
    if env_email or env_password:
        creds = dict(config.get("credentials", {}))
        if env_email:
            creds["email"] = env_email
        if env_password:
            creds["password"] = env_password
        config["credentials"] = creds

    return config

