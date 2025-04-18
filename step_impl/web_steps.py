import logging
import os
from getgauge.python import step, data_store, before_scenario, after_scenario
from core.web.driver_factory import WebDriverFactory
from core.web.pages.login_page import LoginPage
from core.web.pages.secure_page import SecurePage

# Setup logging
logger = logging.getLogger(__name__)

# 检查是否是Web测试的辅助函数
def is_web_test(context):
    """检查当前测试是否是Web测试（即不是android或ios标签）"""
    # 从环境变量中获取GAUGE_TAGS
    gauge_tags = os.environ.get('GAUGE_TAGS', '').lower()
    
    # 如果标签中包含android或ios，则不是Web测试
    if 'android' in gauge_tags or 'ios' in gauge_tags:
        return False
        
    # 检查context中的tags
    if hasattr(context, 'tags') and context.tags:
        if any(tag.lower() in ['android', 'ios'] for tag in context.tags):
            return False
            
    # 检查scenario中的tags
    if hasattr(context, 'scenario') and hasattr(context.scenario, 'tags'):
        if any(tag.lower() in ['android', 'ios'] for tag in context.scenario.tags):
            return False
    
    # 默认认为是Web测试
    return True

# 只在Web测试情况下创建WebDriver
@before_scenario
def before_scenario_hook(context):
    # 仅在非移动测试时创建WebDriver
    if is_web_test(context):
        logger.info("Setting up WebDriver for Web test scenario")
        try:
            driver_factory = WebDriverFactory()
            driver = driver_factory.get_driver()
            # Store the driver in the data store for later use
            data_store.scenario["web_driver"] = driver  # 使用独立的键存储Web驱动
            logger.info("WebDriver created successfully")
        except Exception as e:
            logger.error(f"Error creating WebDriver: {str(e)}")
            raise
    else:
        logger.info("Skipping WebDriver setup for mobile test scenario")

@after_scenario
def after_scenario_hook(context):
    # 仅在非移动测试时清理WebDriver
    if is_web_test(context):
        logger.info("Tearing down WebDriver after the scenario")
        try:
            # Get the driver from the data store using the web-specific key
            driver = data_store.scenario.get("web_driver")
            if driver:
                # Quit the driver
                driver.quit()
                logger.info("WebDriver quit successfully")
        except Exception as e:
            logger.error(f"Error quitting WebDriver: {str(e)}")
    else:
        logger.info("Skipping WebDriver teardown for mobile test scenario")

@step("I open the login page")
def open_login_page():
    logger.info("Opening the login page")
    driver = data_store.scenario["web_driver"]
    login_page = LoginPage(driver)
    login_page.open()
    # Store the login page in the data store for later use
    data_store.scenario["login_page"] = login_page

@step("I enter username <username>")
def enter_username(username):
    logger.info(f"Entering username: {username}")
    login_page = data_store.scenario["login_page"]
    login_page.enter_username(username)

@step("I enter password <password>")
def enter_password(password):
    logger.info(f"Entering password: {'*' * len(password)}")
    login_page = data_store.scenario["login_page"]
    login_page.enter_password(password)

@step("I click the login button")
def click_login_button():
    logger.info("Clicking the login button")
    login_page = data_store.scenario["login_page"]
    login_page.click_login_button()

@step("I should be successfully logged in")
def verify_successful_login():
    logger.info("Verifying successful login")
    login_page = data_store.scenario["login_page"]
    assert login_page.is_login_successful(), "Login was not successful"
    
    # Create a secure page instance for the future steps
    driver = data_store.scenario["web_driver"]
    secure_page = SecurePage(driver)
    # Store the secure page in the data store for later use
    data_store.scenario["secure_page"] = secure_page

@step("The secure area page should be displayed")
def verify_secure_page_displayed():
    logger.info("Verifying secure area page is displayed")
    secure_page = data_store.scenario["secure_page"]
    assert secure_page.is_secure_page_displayed(), "Secure area page is not displayed"

@step("I should see an error message")
def verify_error_message_displayed():
    logger.info("Verifying error message is displayed")
    login_page = data_store.scenario["login_page"]
    # 修改断言逻辑，检查flash消息中是否包含更通用的失败提示文本
    flash_message = login_page.get_flash_message().lower()
    assert "invalid" in flash_message, f"Error message is not displayed. Flash message: '{flash_message}'"

@step("The error message should contain <message>")
def verify_error_message_content(message):
    logger.info(f"Verifying error message contains: {message}")
    login_page = data_store.scenario["login_page"]
    assert message in login_page.get_flash_message(), f"Error message does not contain: {message}"

@step("I click the logout button")
def click_logout_button():
    logger.info("Clicking the logout button")
    secure_page = data_store.scenario["secure_page"]
    secure_page.click_logout_button()

@step("I should be logged out")
def verify_logged_out():
    logger.info("Verifying logged out")
    driver = data_store.scenario["web_driver"]
    login_page = LoginPage(driver)
    # Store the login page in the data store for later use
    data_store.scenario["login_page"] = login_page
    # 修改断言逻辑，检查flash消息中是否包含更通用的注销提示文本
    flash_message = login_page.get_flash_message()
    assert "logged out" in flash_message.lower(), f"Logout message is not displayed. Flash message: '{flash_message}'"

@step("The login page should be displayed")
def verify_login_page_displayed():
    logger.info("Verifying login page is displayed")
    driver = data_store.scenario["web_driver"]
    assert "login" in driver.current_url.lower(), "Login page is not displayed" 