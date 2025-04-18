import configparser
import os
import logging
import json
from typing import Dict, Any, Optional

class ConfigManager:
    """增强版配置管理类，支持环境变量、配置文件和缓存"""
    
    def __init__(self):
        """初始化配置管理器"""
        self.logger = logging.getLogger(__name__)
        # 配置缓存
        self._cache = {}
        self.logger.info("ConfigManager initialized")
    
    def get_api_base_url(self) -> str:
        """从环境变量获取API基础URL"""
        if 'api_base_url' not in self._cache:
            self._cache['api_base_url'] = os.environ.get('API_BASE_URL', '')
            self.logger.debug(f"API_BASE_URL from environment: {self._cache['api_base_url']}")
        return self._cache['api_base_url']
    
    def get_web_config(self) -> Dict[str, Any]:
        """从环境变量获取Web配置"""
        if 'web_config' not in self._cache:
            # 尝试获取浏览器窗口大小
            try:
                browser_width = int(os.environ.get('BROWSER_WIDTH', '0'))
                browser_height = int(os.environ.get('BROWSER_HEIGHT', '0'))
            except ValueError:
                browser_width, browser_height = 0, 0
                self.logger.warning("Invalid browser dimensions in environment variables")
            
            # 尝试获取implicit_wait
            try:
                implicit_wait = int(os.environ.get('WEB_IMPLICIT_WAIT', '10'))
            except ValueError:
                implicit_wait = 10
                self.logger.warning("Invalid implicit wait value in environment variables")

            # 解析headless值
            headless_value = os.environ.get('WEB_HEADLESS', 'True')
            if headless_value.lower() in ('true', 'yes', '1'):
                headless = True
            elif headless_value.lower() in ('false', 'no', '0'):
                headless = False
            else:
                headless = True
                self.logger.warning(f"Invalid headless value '{headless_value}', defaulting to True")
                
            self._cache['web_config'] = {
                'base_url': os.environ.get('WEB_BASE_URL', ''),
                'browser': os.environ.get('WEB_BROWSER', 'chrome'),
                'headless': headless,
                'implicit_wait': implicit_wait,
                'browser_width': browser_width,
                'browser_height': browser_height
            }
            self.logger.debug(f"Web config from environment: {json.dumps(self._cache['web_config'])}")
        return self._cache['web_config']
    
    def get_android_config(self) -> Dict[str, Any]:
        """返回Android配置，完全基于环境变量，带错误处理"""
        if 'android_config' not in self._cache:
            # 获取基本配置
            app_package = os.environ.get('ANDROID_APP_PACKAGE', '')
            app_activity = os.environ.get('ANDROID_APP_ACTIVITY', '')
            platform_version = os.environ.get('ANDROID_PLATFORM_VERSION', '')
            device_name = os.environ.get('ANDROID_DEVICE_NAME', '')
            appium_server = os.environ.get('APPIUM_SERVER', '')
            
            # 尝试获取implicit_wait
            try:
                implicit_wait = int(os.environ.get('IMPLICIT_WAIT', '10'))
            except ValueError:
                implicit_wait = 10
                self.logger.warning("Invalid implicit wait value for Android, defaulting to 10")
            
            # 验证必需的配置
            if not app_package:
                self.logger.warning("ANDROID_APP_PACKAGE is not set")
            if not app_activity:
                self.logger.warning("ANDROID_APP_ACTIVITY is not set")
            if not appium_server:
                self.logger.warning("APPIUM_SERVER is not set, using default localhost:4723")
                appium_server = "http://localhost:4723"
            
            self._cache['android_config'] = {
                'app_package': app_package,
                'app_activity': app_activity,
                'platform_version': platform_version,
                'device_name': device_name,
                'appium_server': appium_server,
                'implicit_wait': implicit_wait
            }
            self.logger.debug(f"Android config from environment: {json.dumps(self._cache['android_config'])}")
        return self._cache['android_config']
    
    def get_ios_config(self) -> Dict[str, Any]:
        """返回iOS配置，完全基于环境变量，带错误处理"""
        if 'ios_config' not in self._cache:
            # 获取基本配置
            bundle_id = os.environ.get('IOS_BUNDLE_ID', '')
            platform_version = os.environ.get('IOS_PLATFORM_VERSION', '')
            device_name = os.environ.get('IOS_DEVICE_NAME', '')
            appium_server = os.environ.get('APPIUM_SERVER', '')
            
            # 尝试获取implicit_wait
            try:
                implicit_wait = int(os.environ.get('IMPLICIT_WAIT', '10'))
            except ValueError:
                implicit_wait = 10
                self.logger.warning("Invalid implicit wait value for iOS, defaulting to 10")
            
            # 验证必需的配置
            if not bundle_id:
                self.logger.warning("IOS_BUNDLE_ID is not set")
            if not appium_server:
                self.logger.warning("APPIUM_SERVER is not set, using default localhost:4724")
                appium_server = "http://localhost:4724"
            
            self._cache['ios_config'] = {
                'bundle_id': bundle_id,
                'platform_version': platform_version,
                'device_name': device_name,
                'appium_server': appium_server,
                'implicit_wait': implicit_wait
            }
            self.logger.debug(f"iOS config from environment: {json.dumps(self._cache['ios_config'])}")
        return self._cache['ios_config']
        
    def clear_cache(self) -> None:
        """清除配置缓存"""
        self._cache.clear()
        self.logger.debug("Configuration cache cleared") 