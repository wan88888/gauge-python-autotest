import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from core.utils.config_manager import ConfigManager

class WebDriverFactory:
    """Factory class for creating WebDriver instances"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.web_config = self.config.get_web_config()
        self.logger = logging.getLogger(__name__)
    
    def get_driver(self):
        """Get a WebDriver instance based on the configuration"""
        browser = self.web_config.get('browser', 'chrome').lower()
        headless = self.web_config.get('headless', False)
        implicit_wait = self.web_config.get('implicit_wait', 10)
        
        self.logger.info(f"Creating WebDriver for browser: {browser}, headless: {headless}")
        
        if browser == 'chrome':
            return self._get_chrome_driver(headless, implicit_wait)
        elif browser == 'firefox':
            return self._get_firefox_driver(headless, implicit_wait)
        elif browser == 'edge':
            return self._get_edge_driver(headless, implicit_wait)
        else:
            self.logger.error(f"Unsupported browser: {browser}")
            raise ValueError(f"Unsupported browser: {browser}")
    
    def _get_chrome_driver(self, headless, implicit_wait):
        """Get a Chrome WebDriver instance"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless=new')
            options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        if not headless:
            driver.maximize_window()
        driver.implicitly_wait(implicit_wait)
        return driver
    
    def _get_firefox_driver(self, headless, implicit_wait):
        """Get a Firefox WebDriver instance"""
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--width=1920')
            options.add_argument('--height=1080')
        
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
        if not headless:
            driver.maximize_window()
        driver.implicitly_wait(implicit_wait)
        return driver
    
    def _get_edge_driver(self, headless, implicit_wait):
        """Get an Edge WebDriver instance"""
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
        if not headless:
            driver.maximize_window()
        driver.implicitly_wait(implicit_wait)
        return driver 