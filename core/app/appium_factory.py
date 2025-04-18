import logging
import os
import subprocess
import time
import platform

try:
    from appium import webdriver
    from appium.options.android import UiAutomator2Options
    from appium.options.ios import XCUITestOptions
except ImportError:
    # 创建模拟的webdriver，允许代码加载但不能实际运行
    class WebDriverMock:
        @staticmethod
        def Remote(*args, **kwargs):
            class DriverMock:
                def implicitly_wait(self, timeout):
                    pass
            return DriverMock()
    
    class webdriver:
        Remote = WebDriverMock.Remote
    
    class UiAutomator2Options:
        pass
    
    class XCUITestOptions:
        pass

from core.utils.config_manager import ConfigManager

class AppiumFactory:
    """Factory class for creating Appium driver instances with improved error handling"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.logger = logging.getLogger(__name__)
        
        # 创建标准目录
        self.screenshots_dir = os.path.join(os.getcwd(), 'screenshots')
        self.apps_dir = os.path.join(os.getcwd(), 'resources', 'apps')
        os.makedirs(self.screenshots_dir, exist_ok=True)
        os.makedirs(self.apps_dir, exist_ok=True)
    
    def _verify_appium_server(self, url, max_retries=3, retry_interval=2):
        """验证Appium服务器是否运行
        
        Args:
            url: Appium服务器URL
            max_retries: 最大重试次数
            retry_interval: 重试间隔(秒)
            
        Returns:
            布尔值表示验证结果
        """
        import requests
        
        self.logger.info(f"Verifying Appium server at {url}")
        url_parts = url.split(":")
        if len(url_parts) >= 3:
            host = url_parts[1].replace("//", "")
            port = url_parts[2].split("/")[0]
            
            # 检查端口是否开放
            retry_count = 0
            while retry_count < max_retries:
                try:
                    # 尝试连接到服务器根路径
                    response = requests.get(f"{url}/status", timeout=5)
                    if response.status_code == 200:
                        self.logger.info(f"Appium server is running at {url}")
                        return True
                except requests.RequestException:
                    # 如果请求失败，我们检查端口是否被监听
                    if platform.system() == "Windows":
                        result = subprocess.run(f"netstat -an | findstr {port}", shell=True, 
                                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        if f":{port}" in result.stdout.decode():
                            self.logger.info(f"Port {port} is open, but server might not be ready")
                    else:  # Linux, MacOS
                        result = subprocess.run(f"lsof -i :{port}", shell=True, 
                                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        if result.returncode == 0:
                            self.logger.info(f"Port {port} is open, but server might not be ready")
                
                retry_count += 1
                if retry_count < max_retries:
                    self.logger.warning(f"Appium server check failed, retrying in {retry_interval} seconds...")
                    time.sleep(retry_interval)
            
            self.logger.error(f"Appium server not detected at {url} after {max_retries} retries")
            return False
        else:
            self.logger.error(f"Invalid Appium server URL format: {url}")
            return False
    
    def get_android_driver(self):
        """Get an Android Appium driver instance"""
        android_config = self.config.get_android_config()
        
        self.logger.info(f"Creating Android Appium driver with config: {android_config}")
        
        # 添加详细配置信息的日志
        self.logger.info(f"Android device name: {android_config.get('device_name')}")
        self.logger.info(f"Android platform version: {android_config.get('platform_version')}")
        self.logger.info(f"Android app package: {android_config.get('app_package')}")
        self.logger.info(f"Android app activity: {android_config.get('app_activity')}")
        self.logger.info(f"Appium server URL: {android_config.get('appium_server')}")
        
        try:
            # 检查Appium服务器是否运行
            appium_server = android_config.get('appium_server')
            # 确保使用正确的协议和端口
            if not appium_server.startswith('http'):
                appium_server = f"http://{appium_server}"
                
            if not self._verify_appium_server(appium_server):
                raise RuntimeError(f"Appium server not running at {appium_server}")
                
            # 首先检查应用是否安装
            app_package = android_config.get('app_package')
            try:
                check_cmd = f"adb shell pm list packages | grep {app_package}"
                self.logger.info(f"Checking if app {app_package} is installed with command: {check_cmd}")
                
                result = subprocess.run(check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode != 0:
                    self.logger.error(f"Application {app_package} is not installed on the device")
                    self.logger.error("Please install the SauceLabs demo app on your emulator first")
                    raise RuntimeError(f"Application {app_package} is not installed on the device. Please install the app first.")
            except subprocess.SubprocessError as e:
                self.logger.warning(f"Error checking app installation: {str(e)}")
                self.logger.warning("Will proceed assuming app may be installed or will be installed through app capability")
            
            app_activity = android_config.get('app_activity')
            self.logger.info(f"Original app_activity from config: {app_activity}")
            # 错误信息显示路径被添加了一个额外的点号，尝试移除app_activity前面的点号以修复问题
            if app_activity.startswith('.'):
                app_activity = app_activity[1:]
            
            # 使用UiAutomator2Options而不是直接的capabilities字典
            options = UiAutomator2Options()
            options.set_capability("deviceName", android_config.get('device_name'))
            options.set_capability("platformVersion", android_config.get('platform_version'))
            options.set_capability("appPackage", android_config.get('app_package'))
            options.set_capability("appActivity", app_activity)
            options.set_capability("automationName", "UiAutomator2")
            options.set_capability("newCommandTimeout", 600)
            # 修改重置策略，确保每次测试从干净的状态开始
            options.set_capability("noReset", False)  # 在每次会话之前不要保留应用数据（如cookies、存储）
            options.set_capability("fullReset", False)  # 不需要重新安装应用
            
            # 在resources/apps目录中查找APK文件（如果存在）
            app_path = os.path.join(self.apps_dir, 'saucelabs-demo.apk')
            if os.path.exists(app_path):
                self.logger.info(f"Using app at {app_path}")
                options.set_capability("app", app_path)
            else:
                self.logger.warning(f"App not found at {app_path}, assuming it's preinstalled")
                
            self.logger.info(f"Using capabilities through options: {options.to_capabilities()}")
            
            # Appium 2.x 不再使用 /wd/hub 路径
            # 我们不再附加 /wd/hub，因为这在 Appium 2.x 中不需要
            # 如果 Appium 服务器配置为在 1.x 中使用特定路径，它应该已经包含在 config.ini 中
            
            self.logger.info(f"Connecting to Appium server at {appium_server} with options")
            driver = webdriver.Remote(appium_server, options=options)
            driver.implicitly_wait(android_config.get('implicit_wait'))
            self.logger.info("Successfully connected to Android device")
            return driver
        except Exception as e:
            self.logger.error(f"Error connecting to Android device: {str(e)}")
            raise
    
    def get_ios_driver(self):
        """Get an iOS Appium driver instance"""
        ios_config = self.config.get_ios_config()
        
        self.logger.info(f"Creating iOS Appium driver with config: {ios_config}")
        
        # 添加详细配置信息的日志
        self.logger.info(f"iOS device name: {ios_config.get('device_name')}")
        self.logger.info(f"iOS platform version: {ios_config.get('platform_version')}")
        self.logger.info(f"iOS bundle ID: {ios_config.get('bundle_id')}")
        self.logger.info(f"Appium server URL: {ios_config.get('appium_server')}")
        
        try:
            # 检查Appium服务器是否运行
            appium_server = ios_config.get('appium_server')
            # 确保使用正确的协议和端口
            if not appium_server.startswith('http'):
                appium_server = f"http://{appium_server}"
                
            if not self._verify_appium_server(appium_server):
                raise RuntimeError(f"Appium server not running at {appium_server}")
            
            # 使用XCUITestOptions替代直接传递capabilities字典
            options = XCUITestOptions()
            options.set_capability("deviceName", ios_config.get('device_name'))
            options.set_capability("platformVersion", ios_config.get('platform_version'))
            options.set_capability("bundleId", ios_config.get('bundle_id'))
            options.set_capability("automationName", "XCUITest")
            options.set_capability("newCommandTimeout", 600)
            # 修改重置策略，确保每次测试从干净的状态开始
            options.set_capability("noReset", False)
            options.set_capability("fullReset", False)
            
            # 在resources/apps目录中查找IPA文件（如果存在）
            app_path = os.path.join(self.apps_dir, 'saucelabs-demo.ipa')
            if os.path.exists(app_path):
                self.logger.info(f"Using app at {app_path}")
                options.set_capability("app", app_path)
            else:
                self.logger.warning(f"App not found at {app_path}, assuming it's preinstalled")
            
            self.logger.info(f"Using capabilities through options: {options.to_capabilities()}")
            
            # Appium 2.x 不再使用 /wd/hub 路径
            # 我们不再附加 /wd/hub，因为这在 Appium 2.x 中不需要
            # 如果 Appium 服务器配置为在 1.x 中使用特定路径，它应该已经包含在 config.ini 中
                
            self.logger.info(f"Connecting to Appium server at {appium_server} with options")
            driver = webdriver.Remote(appium_server, options=options)
            driver.implicitly_wait(ios_config.get('implicit_wait'))
            self.logger.info("Successfully connected to iOS device")
            return driver
        except Exception as e:
            self.logger.error(f"Error connecting to iOS device: {str(e)}")
            raise 