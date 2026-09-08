# -*- coding: utf-8 -*-
"""
Shared config loader for BRAIN skills.

Provides a unified config interface that:
1. Reads from environment variables first (BRAIN_EMAIL, BRAIN_PASSWORD, DEEPSEEK_API_KEY)
2. Falls back to skill-local config.json files
3. Handles all 4 historical credential formats transparently

Usage:
    from shared_libs.config_loader import load_config
    config = load_config(skill_dir="path/to/skill")
    email = config.get("email")
    password = config.get("password")
"""

import json
import os
import sys

ENV_VARS = {
    "email": ["BRAIN_EMAIL"],
    "password": ["BRAIN_PASSWORD"],
    "llm_api_key": ["DEEPSEEK_API_KEY", "LLM_API_KEY"],
}

DEFAULTS = {
    "api_url": "https://api.worldquantbrain.com",
    "ui_url": "https://platform.worldquantbrain.com",
    "llm_enabled": False,
}


def _env_value(names):
    """Get value from environment variables, trying multiple names."""
    for name in names:
        val = os.environ.get(name)
        if val and val.strip():
            return val.strip()
    return None


def _load_file(config_path):
    """Load a JSON config file. Returns {} if not found."""
    if not os.path.isfile(config_path):
        return None
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def _extract_credentials(raw):
    """
    Extract email/password from any of the 4 historical formats:
      1. {"username": "...", "password": "..."}
      2. {"email": "...", "password": "..."}
      3. {"BRAIN_CREDENTIALS": {"email": "...", "password": "..."}}
      4. {"brain_email": "...", "brain_password": "..."}
    """
    if not raw or not isinstance(raw, dict):
        return {}

    # Format 0: unified {"credentials": {"email": "...", "password": "..."}}
    creds = raw.get("credentials")
    if creds and isinstance(creds, dict) and "email" in creds:
        return {
            "email": creds.get("email", ""),
            "password": creds.get("password", ""),
        }

    # Format 1: username/password
    if "username" in raw and "password" in raw:
        return {"email": raw["username"], "password": raw["password"]}

    # Format 3: BRAIN_CREDENTIALS nested
    creds = raw.get("BRAIN_CREDENTIALS")
    if creds and isinstance(creds, dict):
        return {
            "email": creds.get("email", ""),
            "password": creds.get("password", ""),
        }

    # Format 4: brain_email / brain_password
    if "brain_email" in raw:
        return {
            "email": raw.get("brain_email", ""),
            "password": raw.get("brain_password", ""),
        }

    # Format 2: email / password (plain)
    if "email" in raw:
        return {"email": raw.get("email", ""), "password": raw.get("password", "")}

    return {}


def load_config(skill_dir=None, config_path=None):
    """
    Load unified config from environment + config file.

    Args:
        skill_dir: Root directory of the skill (used to find config.json)
        config_path: Explicit path to config.json (overrides skill_dir lookup)

    Returns:
        dict with unified keys: email, password, api_url, ui_url, llm, overrides
    """
    result = {
        "email": "",
        "password": "",
        "api_url": DEFAULTS["api_url"],
        "ui_url": DEFAULTS["ui_url"],
        "llm": {
            "enabled": DEFAULTS["llm_enabled"],
            "provider": "",
            "model": "",
            "api_url": "",
            "api_key": "",
        },
        "overrides": {},
    }

    # 1. Load file
    raw = None
    if config_path:
        raw = _load_file(config_path)
    elif skill_dir:
        # Try common config locations
        candidates = [
            os.path.join(skill_dir, "config.json"),
            os.path.join(skill_dir, "configs", "config.json"),
        ]
        for p in candidates:
            raw = _load_file(p)
            if raw:
                break

    # 2. Extract credentials from file (handles all formats)
    if raw:
        creds = _extract_credentials(raw)
        if creds.get("email"):
            result["email"] = creds["email"]
        if creds.get("password"):
            result["password"] = creds["password"]

        # Platform URLs (also handle unified "platform" block)
        if raw.get("BRAIN_API_URL"):
            result["api_url"] = raw["BRAIN_API_URL"]
        if raw.get("BRAIN_URL"):
            result["ui_url"] = raw["BRAIN_URL"]
        platform = raw.get("platform")
        if platform and isinstance(platform, dict):
            if platform.get("api_url"):
                result["api_url"] = platform["api_url"]
            if platform.get("ui_url"):
                result["ui_url"] = platform["ui_url"]

        # LLM settings (also handle unified "llm" block)
        if "judge" in raw and isinstance(raw["judge"], dict):
            llm_cfg = raw["judge"].get("llm", {})
            if llm_cfg:
                result["llm"].update({
                    "enabled": llm_cfg.get("enabled", False),
                    "provider": llm_cfg.get("provider", ""),
                    "model": llm_cfg.get("model", ""),
                    "api_url": llm_cfg.get("api_url", ""),
                    "api_key": llm_cfg.get("api_key", ""),
                })
                judge_overrides = {k: v for k, v in raw["judge"].items() if k != "llm"}
                result["overrides"]["judge"] = judge_overrides
        elif raw.get("llm") and isinstance(raw["llm"], dict):
            llm_block = raw["llm"]
            if isinstance(llm_block.get("enabled"), bool):
                result["llm"]["enabled"] = llm_block["enabled"]
            if llm_block.get("provider"):
                result["llm"]["provider"] = llm_block["provider"]
            if llm_block.get("model"):
                result["llm"]["model"] = llm_block["model"]
            if llm_block.get("api_url"):
                result["llm"]["api_url"] = llm_block["api_url"]
            if llm_block.get("api_key"):
                result["llm"]["api_key"] = llm_block["api_key"]
        else:
            # brain-enhance-template / makeSomeGem format: moonshot_* keys
            if raw.get("moonshot_base_url"):
                result["llm"] = {
                    "enabled": True,
                    "provider": "openai-compatible",
                    "model": raw.get("moonshot_model", ""),
                    "api_url": raw.get("moonshot_base_url", ""),
                    "api_key": raw.get("moonshot_api_key", ""),
                }

        # Carry over any unknown top-level keys as overrides
        known_keys = {"username", "password", "email", "BRAIN_API_URL", "BRAIN_URL",
                      "BRAIN_CREDENTIALS", "brain_email", "brain_password",
                      "moonshot_base_url", "moonshot_model", "moonshot_api_key",
                      "judge", "version", "credentials", "platform", "llm", "overrides"}
        for k, v in raw.items():
            if k not in known_keys:
                result["overrides"][k] = v

    # 3. Environment overrides (always win)
    env_email = _env_value(["BRAIN_EMAIL"])
    if env_email:
        result["email"] = env_email

    env_password = _env_value(["BRAIN_PASSWORD"])
    if env_password:
        result["password"] = env_password

    env_key = _env_value(["DEEPSEEK_API_KEY", "LLM_API_KEY"])
    if env_key:
        result["llm"]["api_key"] = env_key

    return result


def save_config(config_path, config_dict):
    """
    Save a unified config dict to a JSON file.

    Args:
        config_path: Full path for the output config.json
        config_dict: Dict with unified keys (email, password, api_url, etc.)
    """
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    output = {
        "version": "1.0",
        "credentials": {
            "email": config_dict.get("email", ""),
            "password": config_dict.get("password", ""),
        },
        "platform": {
            "api_url": config_dict.get("api_url", DEFAULTS["api_url"]),
            "ui_url": config_dict.get("ui_url", DEFAULTS["ui_url"]),
        },
        "llm": config_dict.get("llm", {}),
        "overrides": config_dict.get("overrides", {}),
    }
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)