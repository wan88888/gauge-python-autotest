try:
    from appium.webdriver.common.mobileby import MobileBy
except ImportError:
    # 使用模拟的MobileBy类，允许代码加载但不能实际运行
    class MobileBy:
        ACCESSIBILITY_ID = "accessibility id"
        XPATH = "xpath"
        ID = "id"

from core.app.base_page import BaseMobilePage

class MobileProductPage(BaseMobilePage):
    """Page Object for the SauceLabs Sample App Product Page"""
    
    # Android locators
    PRODUCT_LIST = (MobileBy.ACCESSIBILITY_ID, "test-PRODUCTS")
    PRODUCT_ITEM = (MobileBy.ACCESSIBILITY_ID, "test-Item")
    PRODUCT_TITLE = (MobileBy.ACCESSIBILITY_ID, "test-Item title")
    PRODUCT_PRICE = (MobileBy.ACCESSIBILITY_ID, "test-Price")
    ADD_TO_CART_BUTTON = (MobileBy.ACCESSIBILITY_ID, "test-ADD TO CART")
    BACK_BUTTON = (MobileBy.ACCESSIBILITY_ID, "test-BACK TO PRODUCTS")
    
    # Alternative locators using XPATH
    ALT_PRODUCT_LIST = (MobileBy.XPATH, "//android.widget.ScrollView[@content-desc='test-PRODUCTS']")
    ALT_PRODUCT_ITEM = (MobileBy.XPATH, "//android.view.ViewGroup[@content-desc='test-Item']")
    ALT_PRODUCT_TITLE = (MobileBy.XPATH, "//android.widget.TextView[@content-desc='test-Item title']")
    ALT_PRODUCT_PRICE = (MobileBy.XPATH, "//android.widget.TextView[@content-desc='test-Price']")
    ALT_ADD_TO_CART_BUTTON = (MobileBy.XPATH, "//android.view.ViewGroup[@content-desc='test-ADD TO CART']")
    ALT_BACK_BUTTON = (MobileBy.XPATH, "//android.view.ViewGroup[@content-desc='test-BACK TO PRODUCTS']")
    
    # iOS specific locators
    IOS_PRODUCT_LIST = (MobileBy.ACCESSIBILITY_ID, "test-PRODUCTS")
    IOS_PRODUCT_ITEM = (MobileBy.ACCESSIBILITY_ID, "test-Item")
    IOS_PRODUCT_TITLE = (MobileBy.ACCESSIBILITY_ID, "test-Item title")
    IOS_PRODUCT_PRICE = (MobileBy.ACCESSIBILITY_ID, "test-Price")
    IOS_ADD_TO_CART_BUTTON = (MobileBy.ACCESSIBILITY_ID, "test-ADD TO CART")
    IOS_BACK_BUTTON = (MobileBy.ACCESSIBILITY_ID, "test-BACK TO PRODUCTS")
    
    # iOS alternative locators
    IOS_ALT_PRODUCT_LIST = (MobileBy.XPATH, "//XCUIElementTypeScrollView[@name='test-PRODUCTS']")
    IOS_ALT_PRODUCT_ITEM = (MobileBy.XPATH, "//XCUIElementTypeOther[@name='test-Item']")
    IOS_ALT_PRODUCT_TITLE = (MobileBy.XPATH, "//XCUIElementTypeStaticText[@name='test-Item title']")
    IOS_ALT_PRODUCT_PRICE = (MobileBy.XPATH, "//XCUIElementTypeStaticText[@name='test-Price']")
    IOS_ALT_ADD_TO_CART_BUTTON = (MobileBy.XPATH, "//XCUIElementTypeOther[@name='test-ADD TO CART']")
    IOS_ALT_BACK_BUTTON = (MobileBy.XPATH, "//XCUIElementTypeOther[@name='test-BACK TO PRODUCTS']")
    
    def __init__(self, driver, platform='android'):
        super().__init__(driver)
        self.platform = platform.lower()
        
        # Set the correct locators based on platform
        if self.platform == 'ios':
            self.PRODUCT_LIST = self.IOS_PRODUCT_LIST
            self.PRODUCT_ITEM = self.IOS_PRODUCT_ITEM
            self.PRODUCT_TITLE = self.IOS_PRODUCT_TITLE
            self.PRODUCT_PRICE = self.IOS_PRODUCT_PRICE
            self.ADD_TO_CART_BUTTON = self.IOS_ADD_TO_CART_BUTTON
            self.BACK_BUTTON = self.IOS_BACK_BUTTON
            self.ALT_PRODUCT_LIST = self.IOS_ALT_PRODUCT_LIST
            self.ALT_PRODUCT_ITEM = self.IOS_ALT_PRODUCT_ITEM
            self.ALT_PRODUCT_TITLE = self.IOS_ALT_PRODUCT_TITLE
            self.ALT_PRODUCT_PRICE = self.IOS_ALT_PRODUCT_PRICE
            self.ALT_ADD_TO_CART_BUTTON = self.IOS_ALT_ADD_TO_CART_BUTTON
            self.ALT_BACK_BUTTON = self.IOS_ALT_BACK_BUTTON
    
    def get_product_items(self):
        """Get all product items in the list"""
        self.logger.info("Getting all product items")
        try:
            return self.find_elements(self.PRODUCT_ITEM)
        except Exception as e:
            self.logger.warning(f"Failed to find product items with primary locator: {str(e)}")
            self.logger.info("Trying alternative locator for product items")
            return self.find_elements(self.ALT_PRODUCT_ITEM)
    
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
    
    def click_add_to_cart(self):
        """Click the Add to Cart button"""
        self.logger.info("Clicking Add to Cart button")
        try:
            self.click(self.ADD_TO_CART_BUTTON)
        except Exception as e:
            self.logger.warning(f"Failed to find Add to Cart button with primary locator: {str(e)}")
            self.logger.info("Trying alternative locator for Add to Cart button")
            self.click(self.ALT_ADD_TO_CART_BUTTON)
        return self
    
    def click_back_button(self):
        """Click the Back to Products button"""
        self.logger.info("Clicking Back to Products button")
        try:
            self.click(self.BACK_BUTTON)
        except Exception as e:
            self.logger.warning(f"Failed to find Back button with primary locator: {str(e)}")
            self.logger.info("Trying alternative locator for Back button")
            self.click(self.ALT_BACK_BUTTON)
        return self
    
    def get_product_title(self):
        """Get the product title text"""
        try:
            return self.get_text(self.PRODUCT_TITLE)
        except Exception as e:
            self.logger.warning(f"Failed to find product title with primary locator: {str(e)}")
            self.logger.info("Trying alternative locator for product title")
            return self.get_text(self.ALT_PRODUCT_TITLE)
    
    def get_product_price(self):
        """Get the product price text"""
        try:
            return self.get_text(self.PRODUCT_PRICE)
        except Exception as e:
            self.logger.warning(f"Failed to find product price with primary locator: {str(e)}")
            self.logger.info("Trying alternative locator for product price")
            return self.get_text(self.ALT_PRODUCT_PRICE)
    
    def is_product_page_displayed(self):
        """Check if the product page is displayed"""
        try:
            return self.is_element_visible(self.PRODUCT_TITLE)
        except Exception:
            self.logger.info("Product title not found with primary locator, trying alternative")
            return self.is_element_visible(self.ALT_PRODUCT_TITLE) 