import logging
import os
import subprocess
import re
import requests
from typing import Dict, Any, Optional

try:
    from appium import webdriver
    from appium.options.android import UiAutomator2Options
    from appium.options.ios import XCUITestOptions
    APPIUM_AVAILABLE = True
except ImportError:
    # 如果没有安装Appium，提供模拟实现
    webdriver = type('MockWebdriver', (), {'Remote': lambda *args, **kwargs: None})
    UiAutomator2Options = type('MockUiAutomator2Options', (), {'load_capabilities': lambda *args, **kwargs: {}})
    XCUITestOptions = type('MockXCUITestOptions', (), {'load_capabilities': lambda *args, **kwargs: {}})
    APPIUM_AVAILABLE = False

from core.utils.config_manager import ConfigManager

class AppiumFactory:
    """Appium驱动工厂，负责创建Android和iOS驱动"""
    
    def __init__(self):
        """初始化Appium工厂"""
        self.logger = logging.getLogger(__name__)
        
        # 导入配置管理器
        self.config_manager = ConfigManager()
        
        # 设置默认超时时间
        self.timeout = 600  # 10分钟，足够应用安装
        
        # 设置一些辅助属性
        self.logger.info("Appium factory initialized")
    
    def get_android_driver(self) -> Optional[webdriver.Remote]:
        """创建Android驱动
        
        Returns:
            Appium WebDriver对象或None（如果创建失败）
        """
        if not APPIUM_AVAILABLE:
            self.logger.error("Appium is not available. Cannot create Android driver.")
            return None
            
        # 获取Android配置
        config = self.config_manager.get_android_config()
        self.logger.info(f"Creating Android Appium driver with config: {config}")
        
        # 检查必需的配置
        app_package = config.get('app_package', '')
        app_activity = config.get('app_activity', '')
        platform_version = config.get('platform_version', '')
        device_name = config.get('device_name', '')
        appium_server = config.get('appium_server', 'http://localhost:4723')
        
        # 记录配置信息
        self.logger.info(f"Android device name: {device_name}")
        self.logger.info(f"Android platform version: {platform_version}")
        self.logger.info(f"Android app package: {app_package}")
        self.logger.info(f"Android app activity: {app_activity}")
        self.logger.info(f"Appium server URL: {appium_server}")
        
        # 验证Appium服务器是否可用
        self._verify_appium_server(appium_server)
        
        # 检查应用是否已安装
        is_app_installed = self._is_android_app_installed(app_package)
        
        # 设备上可能没有这个应用，但我们可以继续进行，因为启动应用可能会自动安装
        if not is_app_installed:
            self.logger.warning(f"App {app_package} might not be installed on the device.")
        
        # 记录原始app_activity
        self.logger.info(f"Original app_activity from config: {app_activity}")
        
        try:
            # 创建UiAutomator2选项
            options = UiAutomator2Options()
            options.automation_name = 'UIAutomator2'
            options.platform_name = 'Android'
            options.device_name = device_name
            options.platform_version = platform_version
            options.app_package = app_package
            options.app_activity = app_activity
            options.automation_name = "UiAutomator2"
            options.new_command_timeout = self.timeout
            options.no_reset = False
            options.full_reset = False
            
            # 记录使用的capabilities
            capabilities = options.to_capabilities()
            self.logger.info(f"Using capabilities through options: {capabilities}")
            
            # 创建Appium连接
            self.logger.info(f"Connecting to Appium server at {appium_server} with options")
            driver = webdriver.Remote(appium_server, options=options)
            self.logger.info("Successfully connected to Android device")
            
            return driver
        except Exception as e:
            self.logger.error(f"Error creating Android driver: {str(e)}")
            raise
    
    def get_ios_driver(self) -> Optional[webdriver.Remote]:
        """创建iOS驱动
        
        Returns:
            Appium WebDriver对象或None（如果创建失败）
        """
        if not APPIUM_AVAILABLE:
            self.logger.error("Appium is not available. Cannot create iOS driver.")
            return None
            
        # 获取iOS配置
        config = self.config_manager.get_ios_config()
        self.logger.info(f"Creating iOS Appium driver with config: {config}")
        
        # 检查必需的配置
        bundle_id = config.get('bundle_id', '')
        platform_version = config.get('platform_version', '')
        device_name = config.get('device_name', '')
        appium_server = config.get('appium_server', 'http://localhost:4724')
        
        # 记录配置信息
        self.logger.info(f"iOS device name: {device_name}")
        self.logger.info(f"iOS platform version: {platform_version}")
        self.logger.info(f"iOS bundle ID: {bundle_id}")
        self.logger.info(f"Appium server URL: {appium_server}")
        
        # 验证Appium服务器是否可用
        self._verify_appium_server(appium_server)
        
        # 假设应用已经安装，否则iOS自动化将失败
        self.logger.warning(f"Assuming app {bundle_id} is preinstalled")
        
        try:
            # 创建XCUITest选项
            options = XCUITestOptions()
            options.automation_name = 'XCUITest'
            options.platform_name = 'iOS'
            options.device_name = device_name
            options.platform_version = platform_version
            options.bundle_id = bundle_id
            options.automation_name = "XCUITest"
            options.new_command_timeout = self.timeout
            options.no_reset = False
            options.full_reset = False
            
            # 记录使用的capabilities
            capabilities = options.to_capabilities()
            self.logger.info(f"Using capabilities through options: {capabilities}")
            
            # 创建Appium连接
            self.logger.info(f"Connecting to Appium server at {appium_server} with options")
            driver = webdriver.Remote(appium_server, options=options)
            self.logger.info("Successfully connected to iOS device")
            
            return driver
        except Exception as e:
            self.logger.error(f"Error creating iOS driver: {str(e)}")
            raise
    
    def _verify_appium_server(self, server_url: str) -> bool:
        """验证Appium服务器是否可用
        
        Args:
            server_url: Appium服务器URL
            
        Returns:
            布尔值表示服务器是否可用
        """
        self.logger.info(f"Verifying Appium server at {server_url}")
        
        # 确保URL以http开头
        if not server_url.startswith('http'):
            server_url = f"http://{server_url}"
        
        # Appium 2.x 不再使用/wd/hub路径
        if '/wd/hub' in server_url:
            server_url = server_url.replace('/wd/hub', '')
            self.logger.info(f"Removed '/wd/hub' from server URL for Appium 2.x compatibility: {server_url}")
        
        try:
            # 尝试连接到Appium服务器
            response = requests.get(f"{server_url}/status", timeout=5)
            if response.status_code == 200:
                self.logger.info(f"Appium server is running at {server_url}")
                return True
            else:
                self.logger.error(f"Appium server returned status code {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error connecting to Appium server: {str(e)}")
            return False
    
    def _is_android_app_installed(self, package_name: str) -> bool:
        """检查Android应用是否已安装
        
        Args:
            package_name: 应用包名
            
        Returns:
            布尔值表示应用是否已安装
        """
        if not package_name:
            return False
            
        try:
            # 使用adb检查应用是否已安装
            cmd = f"adb shell pm list packages | grep {package_name}"
            self.logger.info(f"Checking if app {package_name} is installed with command: {cmd}")
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return package_name in result.stdout
        except Exception as e:
            self.logger.error(f"Error checking if app is installed: {str(e)}")
            return False 