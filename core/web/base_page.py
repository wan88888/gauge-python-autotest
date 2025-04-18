import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException, WebDriverException
from core.utils.common import take_screenshot, retry

class BasePage:
    """Base Page Object class for all pages"""
    
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
    
    def navigate_to(self, url):
        """Navigate to a URL"""
        self.logger.info(f"Navigating to {url}")
        self.driver.get(url)
    
    def find_element(self, locator, timeout=10):
        """Find an element on the page"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Element not found: {str(e)}")
            take_screenshot(self.driver, "element_not_found")
            raise
    
    def find_elements(self, locator, timeout=10):
        """Find elements on the page"""
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Elements not found: {str(e)}")
            take_screenshot(self.driver, "elements_not_found")
            return []
    
    def click(self, locator, timeout=10):
        """Click an element on the page with improved error handling and fallbacks"""
        try:
            # 首先尝试常规点击
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            try:
                element.click()
            except (ElementNotInteractableException, WebDriverException) as e:
                self.logger.warning(f"Normal click failed, trying JS click: {str(e)}")
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                except Exception as js_error:
                    self.logger.error(f"JS click also failed: {str(js_error)}")
                    # 尝试使用Actions类点击
                    from selenium.webdriver.common.action_chains import ActionChains
                    self.logger.warning("Trying click with ActionChains")
                    ActionChains(self.driver).move_to_element(element).click().perform()
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
            self.logger.error(f"Element not clickable: {locator} - {str(e)}")
            take_screenshot(self.driver, "element_not_clickable", error_context=f"Failed to click {locator}")
            raise
    
    def send_keys(self, locator, text, timeout=10):
        """Send keys to an element on the page"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            element.clear()
            element.send_keys(text)
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Cannot send keys to element: {str(e)}")
            take_screenshot(self.driver, "send_keys_failed")
            raise
    
    def get_text(self, locator, timeout=10):
        """Get text from an element on the page"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.text
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Cannot get text from element: {str(e)}")
            take_screenshot(self.driver, "get_text_failed")
            return ""
    
    def is_element_visible(self, locator, timeout=5):
        """Check if an element is visible on the page with improved error handling"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def wait_for_element_to_disappear(self, locator, timeout=10):
        """Wait for an element to disappear from the page"""
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_page_load(self, timeout=30):
        """等待页面加载完成
        
        等待页面document.readyState为complete
        """
        self.logger.info("Waiting for page to load...")
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return True
        except Exception as e:
            self.logger.error(f"Error waiting for page load: {str(e)}")
            take_screenshot(self.driver, "page_load_timeout", error_context="Page load timeout")
            return False
    
    def execute_script_safely(self, script, *args):
        """安全地执行JavaScript代码，处理可能的异常"""
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            self.logger.error(f"Error executing JavaScript: {str(e)}")
            take_screenshot(self.driver, "js_error", error_context=f"JS error: {script[:50]}...")
            return None
    
    def verify_page_title(self, expected_title, contains=True, timeout=10):
        """验证页面标题是否符合预期
        
        Args:
            expected_title: 期望的标题
            contains: 是否只需包含而非完全匹配
            timeout: 超时时间
        
        Returns:
            布尔值表示验证结果
        """
        try:
            if contains:
                WebDriverWait(self.driver, timeout).until(
                    lambda driver: expected_title in driver.title
                )
                self.logger.info(f"Page title contains '{expected_title}'")
                return True
            else:
                WebDriverWait(self.driver, timeout).until(
                    lambda driver: driver.title == expected_title
                )
                self.logger.info(f"Page title is exactly '{expected_title}'")
                return True
        except TimeoutException:
            actual_title = self.driver.title
            self.logger.error(f"Page title verification failed. Expected: '{expected_title}', Actual: '{actual_title}'")
            take_screenshot(self.driver, "title_verification_failed")
            return False
    
    def scroll_to_element(self, locator, timeout=10):
        """滚动页面直到元素可见
        
        Args:
            locator: 元素定位器
            timeout: 超时时间(秒)
        
        Returns:
            元素对象或None
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            # 等待滚动完成
            import time
            time.sleep(0.5)
            return element
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Cannot scroll to element {locator}: {str(e)}")
            take_screenshot(self.driver, "scroll_to_element_failed", error_context=f"Failed to scroll to {locator}")
            return None 