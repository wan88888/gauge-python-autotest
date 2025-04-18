from selenium.webdriver.common.by import By
from core.web.base_page import BasePage

class SecurePage(BasePage):
    """Page Object for the Secure Page (after login)"""
    
    # Page locators
    LOGOUT_BUTTON = (By.CSS_SELECTOR, ".button.secondary")
    FLASH_MESSAGE = (By.ID, "flash")
    SECURE_AREA_HEADER = (By.CSS_SELECTOR, "h2")
    
    def click_logout_button(self):
        """Click the logout button"""
        self.logger.info("Clicking logout button")
        self.click(self.LOGOUT_BUTTON)
        return self
    
    def get_flash_message(self):
        """Get the flash message text"""
        return self.get_text(self.FLASH_MESSAGE)
    
    def get_header_text(self):
        """Get the header text"""
        return self.get_text(self.SECURE_AREA_HEADER)
    
    def is_secure_page_displayed(self):
        """Check if the secure page is displayed"""
        header_text = self.get_header_text()
        return "Secure Area" in header_text 