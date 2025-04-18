import logging
import os
import time
from getgauge.python import step, data_store, before_scenario, after_scenario, ExecutionContext

try:
    from core.app.appium_factory import AppiumFactory
    from core.app.pages.login_page import MobileLoginPage
    from core.app.pages.home_page import MobileHomePage
    from core.app.pages.product_page import MobileProductPage
    APPIUM_AVAILABLE = True
except ImportError:
    # 当缺少Appium时提供模拟实现
    AppiumFactory = MobileLoginPage = MobileHomePage = MobileProductPage = None
    APPIUM_AVAILABLE = False

# Setup logging
logger = logging.getLogger(__name__)

def is_mobile_test(context):
    """判断是否是移动测试（Android或iOS）
    
    Args:
        context: Gauge的执行上下文
        
    Returns:
        布尔值表示是否是移动测试
    """
    # 直接从环境变量获取GAUGE_TAGS
    gauge_tags = os.environ.get('GAUGE_TAGS', '').lower()
    env_tags = os.environ.get('TAGS', '').lower()
    
    # 如果任一标签中包含android或ios，则是移动测试
    is_mobile = any(tag in gauge_tags.split(',') for tag in ['android', 'ios'])
    is_mobile = is_mobile or any(tag in env_tags.split(',') for tag in ['android', 'ios'])
    
    # 检查context中的tags
    if hasattr(context, 'tags') and context.tags:
        is_mobile = is_mobile or any(tag.lower() in ['android', 'ios'] for tag in context.tags)
        
    # 检查scenario中的tags
    if hasattr(context, 'scenario') and hasattr(context.scenario, 'tags'):
        is_mobile = is_mobile or any(tag.lower() in ['android', 'ios'] for tag in context.scenario.tags)
    
    # 记录最终结果，帮助调试
    logger.debug(f"is_mobile_test result: {is_mobile}")
    return is_mobile

# 使用更可靠的标签检测方法
def has_tag(context, tag):
    """检查上下文是否有特定标签"""
    try:
        # 直接从环境变量获取GAUGE_TAGS
        gauge_tags = os.environ.get('GAUGE_TAGS', '').lower()
        env_tags = os.environ.get('TAGS', '').lower()
        
        # 如果命令行指定了标签
        if tag.lower() in gauge_tags.split(',') or tag.lower() in env_tags.split(','):
            return True
            
        # 检查context中的tags
        if hasattr(context, 'tags') and context.tags:
            return tag.lower() in [t.lower() for t in context.tags]
            
        # 检查scenario中的tags
        if hasattr(context, 'scenario') and hasattr(context.scenario, 'tags'):
            return tag.lower() in [t.lower() for t in context.scenario.tags]
            
        # 检查specification中的tags
        if hasattr(context, 'specification') and hasattr(context.specification, 'tags'):
            return tag.lower() in [t.lower() for t in context.specification.tags]
            
        return False
    except Exception as e:
        logger.error(f"Error checking tags: {str(e)}")
        return False

@before_scenario
def before_android_scenario(context):
    """Android场景前置钩子"""
    # 如果Appium不可用，跳过移动测试
    if not APPIUM_AVAILABLE:
        logger.warning("Appium is not available, skipping Android test setup")
        data_store.scenario["skip_mobile_test"] = True
        return
        
    # 检查是否是Android测试环境
    # 从环境变量TAGS获取标签而不是命令行
    env_tags = os.environ.get('TAGS', '').lower()
    is_android_test = 'android' in env_tags
    
    if is_android_test:
        logger.info(f"Setting up Android driver for the scenario with tags: {env_tags}")
        try:
            # 初始化Android driver
            appium_factory = AppiumFactory()
            driver = appium_factory.get_android_driver()
            # 存储driver和platform到data store
            data_store.scenario["app_driver"] = driver  # 使用独立的键存储Appium驱动
            data_store.scenario["platform"] = "android"
            logger.info("Android driver created successfully")
        except Exception as e:
            logger.error(f"Error creating Android driver: {str(e)}")
            data_store.scenario["android_setup_error"] = str(e)
            data_store.scenario["skip_mobile_test"] = True

@before_scenario
def before_ios_scenario_hook(context):
    """iOS场景前置钩子"""
    # 如果Appium不可用，跳过移动测试
    if not APPIUM_AVAILABLE:
        logger.warning("Appium is not available, skipping iOS test setup")
        data_store.scenario["skip_mobile_test"] = True
        return
        
    # 检查是否是iOS测试环境
    # 从环境变量TAGS获取标签而不是命令行
    env_tags = os.environ.get('TAGS', '').lower()
    is_ios_test = 'ios' in env_tags
    
    if is_ios_test:
        logger.info("Setting up iOS driver for the scenario")
        try:
            # 检查iOS设备上是否已安装应用
            # 这里为了简化，我们假设如果在iOS环境中，应用已经安装
            # 实际项目中可以添加更具体的检查
            
            # Initialize iOS driver
            appium_factory = AppiumFactory()
            driver = appium_factory.get_ios_driver()
            # Store the driver in the data store for later use
            data_store.scenario["app_driver"] = driver  # 使用独立的键存储Appium驱动
            data_store.scenario["platform"] = "ios"
            logger.info("iOS driver created successfully")
        except Exception as e:
            logger.error(f"Error setting up iOS driver: {str(e)}")
            logger.warning("Skipping iOS test due to setup error")
            # Gauge框架不支持在测试期间动态跳过场景，记录错误并继续
            # 后续步骤将因为缺少driver而无法执行
            data_store.scenario["ios_setup_error"] = str(e)
            data_store.scenario["skip_mobile_test"] = True

@after_scenario
def after_mobile_scenario_hook(context):
    """移动场景后置钩子"""
    # 只在有android或ios标签的场景中执行
    if has_tag(context, "android") or has_tag(context, "ios"):
        logger.info("Tearing down mobile driver after the scenario")
        # Get the driver from the data store
        driver = data_store.scenario.get("app_driver")  # 使用独立的键获取Appium驱动
        if driver:
            try:
                # Quit the driver
                driver.quit()
                logger.info("Mobile driver quit successfully")
            except Exception as e:
                logger.error(f"Error quitting mobile driver: {str(e)}")

def check_mobile_test_skipped(step_name):
    """检查移动测试是否应该被跳过
    
    Args:
        step_name: 步骤名称，用于日志
        
    Returns:
        如果测试应该被跳过，返回True
    """
    if data_store.scenario.get("skip_mobile_test", False):
        if "android_setup_error" in data_store.scenario:
            error = data_store.scenario["android_setup_error"]
            logger.error(f"Skipping step '{step_name}' due to Android setup error: {error}")
            assert False, f"Android setup failed: {error}"
        elif "ios_setup_error" in data_store.scenario:
            error = data_store.scenario["ios_setup_error"]
            logger.error(f"Skipping step '{step_name}' due to iOS setup error: {error}")
            assert False, f"iOS setup failed: {error}"
        else:
            logger.warning(f"Skipping step '{step_name}' due to mobile test being skipped")
            assert False, "Mobile test skipped due to setup issues"
        return True
    return False

@step("I launch the Android app")
def launch_android_app():
    """启动Android应用"""
    if check_mobile_test_skipped("I launch the Android app"):
        return
        
    logger.info("Launching the Android app")
    driver = data_store.scenario["app_driver"]  # 使用独立的键获取Appium驱动
    
    # 如果platform不在data_store中，设置默认值
    if "platform" not in data_store.scenario:
        logger.info("Setting default platform to android")
        data_store.scenario["platform"] = "android"
        
    platform = data_store.scenario["platform"]
    login_page = MobileLoginPage(driver, platform)
    # Store the login page in the data store for later use
    data_store.scenario["login_page"] = login_page

@step("I launch the iOS app")
def launch_ios_app():
    """启动iOS应用"""
    if check_mobile_test_skipped("I launch the iOS app"):
        return
        
    logger.info("Launching the iOS app")
    driver = data_store.scenario["app_driver"]  # 使用独立的键获取Appium驱动
    platform = data_store.scenario["platform"]
    login_page = MobileLoginPage(driver, platform)
    # Store the login page in the data store for later use
    data_store.scenario["login_page"] = login_page

@step("I enter mobile username <username>")
def enter_mobile_username(username):
    """输入移动端用户名"""
    if check_mobile_test_skipped("I enter mobile username"):
        return
        
    logger.info(f"Entering mobile username: {username}")
    login_page = data_store.scenario["login_page"]
    login_page.enter_username(username)

@step("I enter mobile password <password>")
def enter_mobile_password(password):
    """输入移动端密码"""
    if check_mobile_test_skipped("I enter mobile password"):
        return
        
    logger.info(f"Entering mobile password: {'*' * len(password)}")
    login_page = data_store.scenario["login_page"]
    login_page.enter_password(password)

@step("I click the mobile login button")
def click_mobile_login_button():
    """点击移动端登录按钮"""
    if check_mobile_test_skipped("I click the mobile login button"):
        return
        
    logger.info("Clicking the mobile login button")
    login_page = data_store.scenario["login_page"]
    login_page.click_login_button()

@step("I should be successfully logged into the mobile app")
def verify_mobile_successful_login():
    """验证移动端登录成功"""
    if check_mobile_test_skipped("I should be successfully logged into the mobile app"):
        return
        
    logger.info("Verifying successful login to the mobile app")
    driver = data_store.scenario["app_driver"]  # 使用独立的键获取Appium驱动
    platform = data_store.scenario["platform"]
    
    # 等待登录后页面加载
    time.sleep(1)
    
    home_page = MobileHomePage(driver, platform)
    # Store the home page in the data store for later use
    data_store.scenario["home_page"] = home_page
    assert home_page.is_home_page_displayed(), "Home page is not displayed after login"

@step("The mobile home page should be displayed")
def verify_mobile_home_page_displayed():
    """验证移动端主页显示"""
    if check_mobile_test_skipped("The mobile home page should be displayed"):
        return
        
    logger.info("Verifying mobile home page is displayed")
    home_page = data_store.scenario["home_page"]
    assert home_page.is_home_page_displayed(), "Mobile home page is not displayed"

@step("I should see a mobile error message")
def verify_mobile_error_message_displayed():
    """验证移动端错误信息显示"""
    if check_mobile_test_skipped("I should see a mobile error message"):
        return
        
    logger.info("Verifying mobile error message is displayed")
    login_page = data_store.scenario["login_page"]
    
    # 增加重试逻辑，有时错误消息可能需要时间出现
    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:
        if login_page.is_error_displayed():
            break
        logger.info(f"Error message not displayed yet, retrying ({retry_count+1}/{max_retries})...")
        time.sleep(0.5)
        retry_count += 1
    
    assert login_page.is_error_displayed(), "Error message is not displayed"

@step("The mobile error message should contain <message>")
def verify_mobile_error_message_content(message):
    """验证移动端错误信息内容"""
    if check_mobile_test_skipped("The mobile error message should contain"):
        return
        
    logger.info(f"Verifying mobile error message contains: {message}")
    login_page = data_store.scenario["login_page"]
    error_text = login_page.get_error_message()
    assert message in error_text, f"Error message does not contain: {message}. Actual message: {error_text}" 