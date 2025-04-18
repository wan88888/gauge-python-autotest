try:
    from appium.webdriver.common.mobileby import MobileBy
    from appium.webdriver.common.appiumby import AppiumBy
except ImportError:
    # 使用模拟的MobileBy类，允许代码加载但不能实际运行
    class MobileBy:
        ACCESSIBILITY_ID = "accessibility id"
        XPATH = "xpath"
        ID = "id"
    AppiumBy = MobileBy

from core.app.base_page import BaseMobilePage

class MobileHomePage(BaseMobilePage):
    """Page Object for the SauceLabs Sample App Home Page (after login)"""
    
    # Android locators
    PRODUCTS_TITLE = (MobileBy.ACCESSIBILITY_ID, "test-PRODUCTS")
    MENU_BUTTON = (MobileBy.ACCESSIBILITY_ID, "test-Menu")
    CART_BUTTON = (MobileBy.ACCESSIBILITY_ID, "test-Cart")
    CART_BADGE = (MobileBy.XPATH, "//android.view.ViewGroup[@content-desc='test-Cart']/android.view.ViewGroup/android.widget.TextView")
    LOGOUT_BUTTON = (MobileBy.ACCESSIBILITY_ID, "test-LOGOUT")
    PRODUCT_ITEM = (MobileBy.ACCESSIBILITY_ID, "test-Item")
    
    # Alternative locators using XPATH
    ALT_PRODUCTS_TITLE = (MobileBy.XPATH, "//android.widget.TextView[@text='PRODUCTS']")
    ALT_MENU_BUTTON = (MobileBy.XPATH, "//android.view.ViewGroup[@content-desc='test-Menu']/android.widget.ImageView")
    ALT_CART_BUTTON = (MobileBy.XPATH, "//android.view.ViewGroup[@content-desc='test-Cart']/android.widget.ImageView")
    ALT_CART_BADGE = (MobileBy.XPATH, "//android.view.ViewGroup[@content-desc='test-Cart']/android.widget.TextView")
    ALT_LOGOUT_BUTTON = (MobileBy.XPATH, "//android.view.ViewGroup[@content-desc='test-LOGOUT']")
    ALT_PRODUCT_ITEM = (MobileBy.XPATH, "//android.view.ViewGroup[@content-desc='test-Item']")
    
    # iOS specific locators
    IOS_PRODUCTS_TITLE = (MobileBy.ACCESSIBILITY_ID, "test-PRODUCTS")
    IOS_MENU_BUTTON = (MobileBy.ACCESSIBILITY_ID, "test-Menu")
    IOS_CART_BUTTON = (MobileBy.ACCESSIBILITY_ID, "test-Cart")
    IOS_CART_BADGE = (MobileBy.XPATH, "//XCUIElementTypeOther[@name='test-Cart']/XCUIElementTypeOther/XCUIElementTypeStaticText")
    IOS_LOGOUT_BUTTON = (MobileBy.ACCESSIBILITY_ID, "test-LOGOUT")
    IOS_PRODUCT_ITEM = (MobileBy.ACCESSIBILITY_ID, "test-Item")
    
    # iOS alternative locators
    IOS_ALT_PRODUCTS_TITLE = (MobileBy.XPATH, "//XCUIElementTypeStaticText[@name='PRODUCTS']")
    IOS_ALT_MENU_BUTTON = (MobileBy.XPATH, "//XCUIElementTypeOther[@name='test-Menu']")
    IOS_ALT_CART_BUTTON = (MobileBy.XPATH, "//XCUIElementTypeOther[@name='test-Cart']")
    IOS_ALT_CART_BADGE = (MobileBy.XPATH, "//XCUIElementTypeOther[@name='test-Cart']/XCUIElementTypeStaticText")
    IOS_ALT_LOGOUT_BUTTON = (MobileBy.XPATH, "//XCUIElementTypeOther[@name='test-LOGOUT']")
    IOS_ALT_PRODUCT_ITEM = (MobileBy.XPATH, "//XCUIElementTypeOther[@name='test-Item']")
    
    def __init__(self, driver, platform='android'):
        super().__init__(driver)
        self.platform = platform.lower()
        
        # Set the correct locators based on platform
        if self.platform == 'ios':
            self.PRODUCTS_TITLE = self.IOS_PRODUCTS_TITLE
            self.MENU_BUTTON = self.IOS_MENU_BUTTON
            self.CART_BUTTON = self.IOS_CART_BUTTON
            self.CART_BADGE = self.IOS_CART_BADGE
            self.LOGOUT_BUTTON = self.IOS_LOGOUT_BUTTON
            self.PRODUCT_ITEM = self.IOS_PRODUCT_ITEM
            self.ALT_PRODUCTS_TITLE = self.IOS_ALT_PRODUCTS_TITLE
            self.ALT_MENU_BUTTON = self.IOS_ALT_MENU_BUTTON
            self.ALT_CART_BUTTON = self.IOS_ALT_CART_BUTTON
            self.ALT_CART_BADGE = self.IOS_ALT_CART_BADGE
            self.ALT_LOGOUT_BUTTON = self.IOS_ALT_LOGOUT_BUTTON
            self.ALT_PRODUCT_ITEM = self.IOS_ALT_PRODUCT_ITEM
    
    def click_menu_button(self):
        """Click the menu button"""
        self.logger.info("Clicking menu button")
        try:
            self.click(self.MENU_BUTTON)
        except Exception as e:
            self.logger.warning(f"Failed to find menu button with primary locator: {str(e)}")
            self.logger.info("Trying alternative locator for menu button")
            self.click(self.ALT_MENU_BUTTON)
        return self
    
    def click_cart_button(self):
        """Click the cart button"""
        self.logger.info("Clicking cart button")
        try:
            self.click(self.CART_BUTTON)
        except Exception as e:
            self.logger.warning(f"Failed to find cart button with primary locator: {str(e)}")
            self.logger.info("Trying alternative locator for cart button")
            self.click(self.ALT_CART_BUTTON)
        return self
    
    def get_cart_badge_count(self):
        """Get the cart badge count"""
        self.logger.info("Getting cart badge count")
        try:
            if self.is_element_visible(self.CART_BADGE):
                return self.get_text(self.CART_BADGE)
            else:
                return "0"  # 如果徽章不可见，返回0
        except Exception as e:
            self.logger.warning(f"Failed to find cart badge with primary locator: {str(e)}")
            self.logger.info("Trying alternative locator for cart badge")
            if self.is_element_visible(self.ALT_CART_BADGE):
                return self.get_text(self.ALT_CART_BADGE)
            else:
                return "0"
    
    def click_product_item(self, index=0):
        """Click on a product item at the given index"""
        self.logger.info(f"Clicking product item at index {index}")
        try:
            items = self.find_elements(self.PRODUCT_ITEM)
            if items and len(items) > index:
                items[index].click()
            else:
                raise Exception(f"No product item found at index {index}")
        except Exception as e:
            self.logger.warning(f"Failed to find/click product item with primary locator: {str(e)}")
            self.logger.info("Trying alternative locator for product item")
            items = self.find_elements(self.ALT_PRODUCT_ITEM)
            if items and len(items) > index:
                items[index].click()
            else:
                raise Exception(f"No product item found at index {index} with alternative locator")
        return self
    
    def click_logout_button(self):
        """Click the logout button in the menu"""
        self.logger.info("Clicking logout button")
        try:
            self.click(self.LOGOUT_BUTTON)
        except Exception as e:
            self.logger.warning(f"Failed to find logout button with primary locator: {str(e)}")
            self.logger.info("Trying alternative locator for logout button")
            self.click(self.ALT_LOGOUT_BUTTON)
        return self
    
    def get_products_title(self):
        """Get the products title text"""
        try:
            return self.get_text(self.PRODUCTS_TITLE)
        except Exception as e:
            self.logger.warning(f"Failed to find products title with primary locator: {str(e)}")
            self.logger.info("Trying alternative locator for products title")
            return self.get_text(self.ALT_PRODUCTS_TITLE)
    
    def is_home_page_displayed(self):
        """Check if the home page is displayed"""
        if self.is_element_visible(self.PRODUCTS_TITLE):
            return True
        self.logger.info("Products title not found with primary locator, trying alternative")
        return self.is_element_visible(self.ALT_PRODUCTS_TITLE) 