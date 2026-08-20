from __future__ import annotations
import json
import time
import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
import re
import base64
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path
from time import sleep
from urllib.parse import urljoin
import redis
import hashlib
import math
import uuid
import random

import requests
import pandas as pd
import zlib
import msgpack
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, EmailStr, model_validator
from brain_api_models import AuthCredentials, SimulationData, SimulationSettings
from brain_config import load_config, _resolve_config_path, _load_dotenv_into_environ
logger = logging.getLogger("brain_api")


class AuthMixin:
    async def authenticate(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate with WorldQuant BRAIN platform with biometric support."""
        async with self._auth_lock:
            return await self._authenticate_unlocked(email, password)

    async def _authenticate_unlocked(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate while ``_auth_lock`` is already held."""
        self.log("🔐 Starting Authentication process...", "INFO")
        auth_timeout = self._default_timeout_seconds + 10  # Extra buffer for asyncio timeout
        
        try:
            # Store credentials for potential re-authentication
            self.auth_credentials = {'email': email, 'password': password}
            self._auth_validated_until = 0.0
            
            # Clear any existing session data (quick operation, no lock needed for this)
            self.session.cookies.clear()
            self.session.auth = None
            
            # Create Basic Authentication header (base64 encoded credentials)
            import base64
            credentials = f"{email}:{password}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            # Send POST request with Basic Authentication header
            headers = {
                'Authorization': f'Basic {encoded_credentials}'
            }
            
            # Use a direct thread call with timeout, no nested locks
            try:
                response = await asyncio.wait_for(
                    asyncio.to_thread(
                        self.session.request,
                        'POST',
                        'https://api.worldquantbrain.com/authentication',
                        headers=headers,
                        timeout=self._default_timeout_seconds,
                    ),
                    timeout=auth_timeout
                )
            except asyncio.TimeoutError:
                self.log(f"❌ Authentication request timed out after {auth_timeout}s", "ERROR")
                raise TimeoutError(f"Authentication timed out after {auth_timeout}s")

            # Check for successful authentication (status code 201)
            if response.status_code == 201:
                self.log("Authentication successful", "SUCCESS")
                
                # Check if JWT token was automatically stored by session
                jwt_token = self.session.cookies.get('t')
                if jwt_token:
                    self._auth_validated_until = time.time() + self._auth_check_ttl_seconds
                    self.log("JWT token automatically stored by session", "SUCCESS")
                
                # Return success response
                return {
                    'user': {'email': email},
                    'status': 'authenticated',
                    'permissions': ['read', 'write'],
                    'message': 'Authentication successful',
                    'status_code': response.status_code,
                    'has_jwt': jwt_token is not None
                }
            
            # Check if biometric authentication is required (401 with persona)
            elif response.status_code == 401:
                www_auth = response.headers.get("WWW-Authenticate")
                location = response.headers.get("Location")
                
                if www_auth == "persona" and location:
                    self.log("🔴 Biometric authentication required", "INFO")
                    
                    # Handle biometric authentication
                    from urllib.parse import urljoin
                    biometric_url = urljoin(response.url, location)
                    return await self._handle_biometric_auth(biometric_url, email)
                else:
                    raise Exception("Incorrect email or password")
            else:
                raise Exception(f"Authentication failed with status code: {response.status_code}")
                    
        except asyncio.TimeoutError:
            self.log(f"❌ Authentication timed out", "ERROR")
            raise TimeoutError("Authentication request timed out")
        except requests.HTTPError as e:
            self.log(f"❌ HTTP error during authentication: {e}", "ERROR")
            raise
        except Exception as e:
            self.log(f"❌ Authentication failed: {str(e)}", "ERROR")
            raise

    async def _handle_biometric_auth(self, biometric_url: str, email: str) -> Dict[str, Any]:
        """Handle biometric authentication using browser automation."""
        self.log("🌐 Starting biometric authentication...", "INFO")
        
        try:
            # Import playwright for browser automation
            from playwright.async_api import async_playwright
            import time
            
            # 尝试导入browser_setup模块来获取浏览器路径
            browser_path = None
            try:
                from browser_setup import ensure_browser_available
                browser_path = ensure_browser_available()
            except ImportError:
                # 如果导入失败，尝试从当前目录导入
                try:
                    import sys
                    from pathlib import Path
                    current_dir = Path(__file__).parent
                    sys.path.insert(0, str(current_dir))
                    from browser_setup import ensure_browser_available
                    browser_path = ensure_browser_available()
                except Exception as e:
                    self.log(f"浏览器路径探测失败，回退默认: {e}", "DEBUG")
            
            async with async_playwright() as p:
                # 设置浏览器启动参数
                browser_args = ['--headless=new', '--no-sandbox', '--disable-dev-shm-usage']
                
                if browser_path and os.path.exists(browser_path):
                    self.log(f"使用自定义浏览器路径: {browser_path}", "INFO")
                    browser = await p.chromium.launch(executable_path=browser_path, args=browser_args)
                else:
                    self.log("使用默认Playwright浏览器", "INFO")
                    browser = await p.chromium.launch(headless=True, args=browser_args)
                    
                page = await browser.new_page()

                self.log("🌐 Opening browser for biometric authentication...", "INFO")
                await page.goto(biometric_url)
                self.log("Browser page loaded successfully", "SUCCESS")

                # Print instructions
                print("\n" + "="*60, file=sys.stderr)
                print("BIOMETRIC AUTHENTICATION REQUIRED", file=sys.stderr)
                print("="*60, file=sys.stderr)
                print("Browser window is open with biometric authentication page", file=sys.stderr)
                print("Complete the biometric authentication in the browser", file=sys.stderr)
                print("The system will automatically check when you're done...", file=sys.stderr)
                print("="*60, file=sys.stderr)

                # Keep checking until authentication is complete
                max_attempts = 60  # 5 minutes maximum (60 * 5 seconds)
                attempt = 0

                while attempt < max_attempts:
                    await asyncio.sleep(5)  # Check every 5 seconds
                    attempt += 1

                    # Check if authentication completed
                    check_response = await self._request('POST', biometric_url)
                    self.log(f"🔄 Checking authentication status (attempt {attempt}/{max_attempts}): {check_response.status_code}", "INFO")

                    if check_response.status_code == 201:
                        self.log("Biometric authentication successful!", "SUCCESS")

                        await browser.close()
                        
                        # Check JWT token
                        jwt_token = self.session.cookies.get('t')
                        if jwt_token:
                            self.log("JWT token received", "SUCCESS")
                        
                        # Return success response
                        return {
                            'user': {'email': email},
                            'status': 'authenticated',
                            'permissions': ['read', 'write'],
                            'message': 'Biometric authentication successful',
                            'status_code': check_response.status_code,
                            'has_jwt': jwt_token is not None
                        }
                
                await browser.close()
                raise Exception("Biometric authentication timed out")

        except Exception as e:
            self.log(f"❌ Biometric authentication failed: {str(e)}", "ERROR")
            raise

    async def is_authenticated(self) -> bool:
        """Check if currently authenticated using JWT token."""
        try:
            # Check if we have a JWT token in cookies
            jwt_token = self.session.cookies.get('t')
            if not jwt_token:
                self.log("❌ No JWT token found", "INFO")
                self._auth_validated_until = 0.0
                return False

            if time.time() < self._auth_validated_until:
                return True
            
            # Test authentication with a simple API call
            response = await self._request('GET', f"{self.base_url}/authentication")
            if response.status_code == 200:
                self._auth_validated_until = time.time() + self._auth_check_ttl_seconds
                return True
            elif response.status_code == 401:
                self.log("❌ JWT token expired or invalid (401)", "INFO")
                self._auth_validated_until = 0.0
                return False
            else:
                self.log(f"⚠️ Unexpected status code during auth check: {response.status_code}", "WARNING")
                self._auth_validated_until = 0.0
                return False
        except (TimeoutError, ConnectionError) as e:
            self.log(f"❌ Network error checking authentication: {str(e)}", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Unexpected error checking authentication: {str(e)}", "ERROR")
            return False

    async def ensure_authenticated(self):
        """Ensure authentication is valid, re-authenticate if needed."""
        jwt_token = self.session.cookies.get('t')
        if jwt_token and time.time() < self._auth_validated_until:
            return

        async with self._auth_lock:
            # Double-check after waiting for another coroutine's auth refresh.
            jwt_token = self.session.cookies.get('t')
            if jwt_token and time.time() < self._auth_validated_until:
                return

            if jwt_token:
                try:
                    response = await self._request('GET', f"{self.base_url}/authentication")
                    if response.status_code == 200:
                        self._auth_validated_until = time.time() + self._auth_check_ttl_seconds
                        return
                    if response.status_code == 401:
                        self.log("❌ JWT token expired or invalid (401)", "INFO")
                    else:
                        self.log(f"⚠️ Unexpected status code during auth check: {response.status_code}", "WARNING")
                except (TimeoutError, ConnectionError) as e:
                    self.log(f"❌ Network error checking authentication: {str(e)}", "ERROR")

            self._auth_validated_until = 0.0
            if not self.auth_credentials:
                self.log("No credentials in memory, loading from config...", "INFO")
                config = load_config()
                creds = config.get("credentials", {})
                email = creds.get("email")
                password = creds.get("password")
                if not email or not password:
                    raise Exception("Authentication credentials not found in config. Please authenticate first.")
                self.auth_credentials = {'email': email, 'password': password}

            self.log("🔄 Re-authenticating...", "INFO")
            await self._authenticate_unlocked(self.auth_credentials['email'], self.auth_credentials['password'])

    async def get_authentication_status(self) -> Optional[Dict[str, Any]]:
        """Get current authentication status and user info."""
        try:
            response = await self._request('GET', f"{self.base_url}/users/self")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get auth status: {str(e)}", "ERROR")
            return None
