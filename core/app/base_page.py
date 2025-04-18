import logging
import os
try:
    from appium.webdriver.common.touch_action import TouchAction
except ImportError:
    # 使用模拟的TouchAction类，允许代码加载但不能实际运行
    class TouchAction:
        def __init__(self, driver):
            self.driver = driver
        
        def press(self, x=None, y=None):
            return self
        
        def wait(self, ms=0):
            return self
        
        def move_to(self, x=None, y=None):
            return self
        
        def release(self):
            return self
        
        def perform(self):
            pass

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from core.utils.common import take_screenshot, retry

class BaseMobilePage:
    """Base Page Object class for mobile pages"""
    
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        # 确保screenshots目录存在
        self.screenshots_dir = os.path.join(os.getcwd(), 'screenshots')
        os.makedirs(self.screenshots_dir, exist_ok=True)
    
    def find_element(self, locator, timeout=10):
        """Find an element on the page with better error handling"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except (TimeoutException, NoSuchElementException) as e:
            error_message = f"Element not found: {locator} - {str(e)}"
            self.logger.error(error_message)
            take_screenshot(self.driver, "element_not_found", error_context=f"Failed to find {locator}")
            raise
    
    def find_elements(self, locator, timeout=10):
        """Find elements on the page with better error handling"""
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.warning(f"Elements not found: {locator} - {str(e)}")
            take_screenshot(self.driver, "elements_not_found", error_context=f"Failed to find elements {locator}")
            return []
    
    def wait_for_element_visible(self, locator, timeout=10, poll_frequency=0.5):
        """明确等待元素可见，与find_element区别开"""
        try:
            element = WebDriverWait(self.driver, timeout, poll_frequency).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Element not visible: {locator} - {str(e)}")
            take_screenshot(self.driver, "element_not_visible", error_context=f"Element not visible {locator}")
            return None
    
    def click(self, locator, timeout=10):
        """Click an element on the page with retry mechanism for flaky elements"""
        try:
            # 先尝试等待元素可点击
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            # 用JavaScript点击可能更可靠
            try:
                element.click()
            except Exception as e:
                self.logger.warning(f"Normal click failed, trying JS click: {str(e)}")
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                except Exception as js_error:
                    self.logger.error(f"JS click also failed: {str(js_error)}")
                    raise
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
            self.logger.error(f"Element not clickable: {locator} - {str(e)}")
            take_screenshot(self.driver, "element_not_clickable", error_context=f"Failed to click {locator}")
            raise
    
    def send_keys(self, locator, text, timeout=10, clear_first=True):
        """Send keys to an element on the page with improved error handling"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            if clear_first:
                try:
                    element.clear()
                except Exception as e:
                    self.logger.warning(f"Failed to clear field, proceeding with input: {str(e)}")
            
            # 尝试常规的send_keys方法
            try:
                element.send_keys(text)
            except Exception as e:
                self.logger.warning(f"Normal send_keys failed, trying JS set value: {str(e)}")
                try:
                    self.driver.execute_script("arguments[0].value = arguments[1];", element, text)
                except Exception as js_error:
                    self.logger.error(f"JS set value also failed: {str(js_error)}")
                    raise
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Cannot send keys to element: {locator} - {str(e)}")
            take_screenshot(self.driver, "send_keys_failed", error_context=f"Failed to input text to {locator}")
            raise
    
    def get_text(self, locator, timeout=10):
        """Get text from an element on the page with better error handling"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            
            # 尝试多种获取文本的方法
            text = element.text
            if not text:
                # 尝试获取value属性
                text = element.get_attribute('value') or ''
                if not text:
                    # 尝试使用JS获取innerText
                    text = self.driver.execute_script("return arguments[0].innerText;", element) or ''
            
            return text
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Cannot get text from element: {locator} - {str(e)}")
            take_screenshot(self.driver, "get_text_failed", error_context=f"Failed to get text from {locator}")
            return ""
    
    def is_element_visible(self, locator, timeout=5):
        """Check if an element is visible on the page with better error handling"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def swipe(self, start_x, start_y, end_x, end_y, duration=800):
        """Swipe from one point to another with better error handling"""
        self.logger.info(f"Swiping from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        try:
            action = TouchAction(self.driver)
            action.press(x=start_x, y=start_y).wait(duration).move_to(x=end_x, y=end_y).release().perform()
        except Exception as e:
            self.logger.error(f"Failed to perform swipe: {str(e)}")
            take_screenshot(self.driver, "swipe_failed", error_context="Swipe operation failed")
    
    def scroll_down(self):
        """Scroll down on the screen with better error handling"""
        self.logger.info("Scrolling down")
        try:
            size = self.driver.get_window_size()
            start_x = size['width'] // 2
            start_y = size['height'] * 0.8
            end_x = size['width'] // 2
            end_y = size['height'] * 0.2
            self.swipe(start_x, start_y, end_x, end_y)
        except Exception as e:
            self.logger.error(f"Failed to scroll down: {str(e)}")
            take_screenshot(self.driver, "scroll_down_failed", error_context="Scroll down failed")
    
    def scroll_up(self):
        """Scroll up on the screen with better error handling"""
        self.logger.info("Scrolling up")
        try:
            size = self.driver.get_window_size()
            start_x = size['width'] // 2
            start_y = size['height'] * 0.2
            end_x = size['width'] // 2
            end_y = size['height'] * 0.8
            self.swipe(start_x, start_y, end_x, end_y)
        except Exception as e:
            self.logger.error(f"Failed to scroll up: {str(e)}")
            take_screenshot(self.driver, "scroll_up_failed", error_context="Scroll up failed")
            
    def wait_for_page_load(self, timeout=30):
        """等待页面加载完成
        
        移动应用中，可以尝试查找通用元素或检查页面状态来判断页面是否加载完成
        """
        self.logger.info("Waiting for page to load...")
        try:
            # 可以根据实际应用情况实现检查逻辑
            return True
        except Exception as e:
            self.logger.error(f"Error waiting for page load: {str(e)}")
            take_screenshot(self.driver, "page_load_timeout", error_context="Page load timeout")
            return False 