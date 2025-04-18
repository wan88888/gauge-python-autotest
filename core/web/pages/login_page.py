from selenium.webdriver.common.by import By
from core.web.base_page import BasePage
from core.utils.config_manager import ConfigManager

class LoginPage(BasePage):
    """Page Object for the Login Page"""
    
    # Page locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH_MESSAGE = (By.ID, "flash")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.config = ConfigManager()
        self.base_url = self.config.get_web_config().get('base_url')
    
    def open(self):
        """Open the login page"""
        url = f"{self.base_url}/login"
        self.navigate_to(url)
        return self
    
    def enter_username(self, username):
        """Enter the username"""
        self.logger.info(f"Entering username: {username}")
        self.send_keys(self.USERNAME_INPUT, username)
        return self
    
    def enter_password(self, password):
        """Enter the password"""
        self.logger.info(f"Entering password: {'*' * len(password)}")
        self.send_keys(self.PASSWORD_INPUT, password)
        return self
    
    def click_login_button(self):
        """Click the login button"""
        self.logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)
        return self
    
    def login(self, username, password):
        """Perform login with given credentials"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def get_flash_message(self):
        """Get the flash message text"""
        return self.get_text(self.FLASH_MESSAGE)
    
    def is_login_successful(self):
        """Check if login was successful"""
        message = self.get_flash_message()
        return "You logged into a secure area!" in message 