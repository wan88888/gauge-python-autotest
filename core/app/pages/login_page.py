try:
    from appium.webdriver.common.mobileby import MobileBy
    from appium.webdriver.common.appiumby import AppiumBy
except ImportError:
    # 使用模拟的MobileBy和AppiumBy类，允许代码加载但不能实际运行
    class MobileBy:
        ACCESSIBILITY_ID = "accessibility id"
        XPATH = "xpath"
        ID = "id"
        CLASS_NAME = "class name"
    AppiumBy = MobileBy

import os
from core.app.base_page import BaseMobilePage

class MobileLoginPage(BaseMobilePage):
    """Page Object for the SauceLabs Sample App Login Page"""
    
    # SwagLabs应用的定位器 - 多种定位策略
    # Android locators - 使用id、resource-id、class等多种策略
    USERNAME_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[@content-desc='test-Username']")
    PASSWORD_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[@content-desc='test-Password']")
    LOGIN_BUTTON = (AppiumBy.XPATH, "//android.view.ViewGroup[@content-desc='test-LOGIN']")
    ERROR_MESSAGE = (AppiumBy.XPATH, "//android.view.ViewGroup[@content-desc='test-Error message']/android.widget.TextView")
    
    # 备用定位器，使用class name和text属性
    ALT_USERNAME_INPUT = (MobileBy.CLASS_NAME, "android.widget.EditText")
    ALT_PASSWORD_INPUT = (MobileBy.XPATH, "//android.widget.EditText[2]")
    ALT_LOGIN_BUTTON = (MobileBy.XPATH, "//*[@text='LOGIN']")
    ALT_ERROR_MESSAGE = (MobileBy.XPATH, "//*[contains(@text, 'Username and password')]")
    
    # iOS specific locators
    IOS_USERNAME_INPUT = (MobileBy.ACCESSIBILITY_ID, "test-Username")
    IOS_PASSWORD_INPUT = (MobileBy.ACCESSIBILITY_ID, "test-Password")
    IOS_LOGIN_BUTTON = (MobileBy.ACCESSIBILITY_ID, "test-LOGIN")
    IOS_ERROR_MESSAGE = (MobileBy.ACCESSIBILITY_ID, "test-Error message")
    
    def __init__(self, driver, platform='android'):
        super().__init__(driver)
        self.platform = platform.lower()
        
        # Set the correct locators based on platform
        if self.platform == 'ios':
            self.USERNAME_INPUT = self.IOS_USERNAME_INPUT
            self.PASSWORD_INPUT = self.IOS_PASSWORD_INPUT
            self.LOGIN_BUTTON = self.IOS_LOGIN_BUTTON
            self.ERROR_MESSAGE = self.IOS_ERROR_MESSAGE
            
        # 确保截图目录存在
        self.screenshots_dir = os.path.join(os.getcwd(), 'screenshots')
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
        # 截取并保存屏幕截图，帮助我们调试
        try:
            screenshot_path = os.path.join(self.screenshots_dir, 'login_screen.png')
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"保存了登录屏幕截图到{screenshot_path}")
        except Exception as e:
            self.logger.warning(f"无法保存截图: {str(e)}")
    
    def enter_username(self, username):
        """Enter the username"""
        self.logger.info(f"Entering username: {username}")
        try:
            self.send_keys(self.USERNAME_INPUT, username)
        except Exception as e:
            self.logger.warning(f"Failed to find username field with primary locator: {str(e)}")
            self.logger.info("Trying alternative locator for username field")
            try:
                self.send_keys(self.ALT_USERNAME_INPUT, username)
            except Exception as e:
                self.logger.error(f"Cannot send keys to element: {str(e)}")
                # 获取页面源代码以便调试
                try:
                    page_source = self.driver.page_source
                    self.logger.info(f"Page source: {page_source[:500]}...")
                except Exception as e:
                    self.logger.warning(f"Cannot get page source: {str(e)}")
                raise
        return self
    
    def enter_password(self, password):
        """Enter the password"""
        self.logger.info(f"Entering password: {'*' * len(password)}")
        try:
            self.send_keys(self.PASSWORD_INPUT, password)
        except Exception as e:
            self.logger.warning(f"Failed to find password field with primary locator: {str(e)}")
            self.logger.info("Trying alternative locator for password field")
            try:
                self.send_keys(self.ALT_PASSWORD_INPUT, password)
            except Exception as e:
                self.logger.error(f"Cannot send keys to password element: {str(e)}")
                # 获取页面源代码以便调试
                try:
                    page_source = self.driver.page_source
                    self.logger.info(f"Page source: {page_source[:500]}...")
                except Exception as e:
                    self.logger.warning(f"Cannot get page source: {str(e)}")
                # 尝试截图
                try:
                    screenshot_path = os.path.join(self.screenshots_dir, 'password_error.png')
                    self.driver.save_screenshot(screenshot_path)
                    self.logger.info(f"保存了错误截图到{screenshot_path}")
                except Exception as e:
                    self.logger.warning(f"无法保存截图: {str(e)}")
                raise
        return self
    
    def click_login_button(self):
        """Click the login button"""
        self.logger.info("Clicking login button")
        try:
            self.click(self.LOGIN_BUTTON)
        except Exception as e:
            self.logger.warning(f"Failed to find login button with primary locator: {str(e)}")
            self.logger.info("Trying alternative locator for login button")
            try:
                self.click(self.ALT_LOGIN_BUTTON)
            except Exception as e:
                self.logger.error(f"Cannot click login button: {str(e)}")
                # 获取页面源代码以便调试
                try:
                    page_source = self.driver.page_source
                    self.logger.info(f"Page source: {page_source[:500]}...")
                except Exception as e:
                    self.logger.warning(f"Cannot get page source: {str(e)}")
                # 尝试截图
                try:
                    screenshot_path = os.path.join(self.screenshots_dir, 'login_button_error.png')
                    self.driver.save_screenshot(screenshot_path)
                    self.logger.info(f"保存了错误截图到{screenshot_path}")
                except Exception as e:
                    self.logger.warning(f"无法保存截图: {str(e)}")
                # 尝试直接通过坐标点击
                try:
                    self.logger.info("尝试通过坐标点击登录按钮")
                    # 中心位置坐标，这个值需要根据实际情况调整
                    size = self.driver.get_window_size()
                    width = size['width']
                    height = size['height']
                    x = width // 2
                    y = int(height * 0.6)  # 假设按钮在屏幕下方60%位置
                    self.driver.tap([(x, y)], 500)
                except Exception as e:
                    self.logger.error(f"Cannot tap on screen: {str(e)}")
                raise
        return self
    
    def login(self, username, password):
        """Perform login with given credentials"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def get_error_message(self):
        """Get the error message text"""
        try:
            if self.is_element_visible(self.ERROR_MESSAGE):
                return self.get_text(self.ERROR_MESSAGE)
        except:
            if self.is_element_visible(self.ALT_ERROR_MESSAGE):
                return self.get_text(self.ALT_ERROR_MESSAGE)
        return ""
    
    def is_error_displayed(self):
        """Check if an error message is displayed"""
        try:
            return self.is_element_visible(self.ERROR_MESSAGE)
        except:
            return self.is_element_visible(self.ALT_ERROR_MESSAGE)
    
    def is_login_page_displayed(self):
        """Check if the login page is displayed"""
        try:
            return self.is_element_visible(self.USERNAME_INPUT) and self.is_element_visible(self.PASSWORD_INPUT)
        except:
            return self.is_element_visible(self.ALT_USERNAME_INPUT) and self.is_element_visible(self.ALT_PASSWORD_INPUT) 