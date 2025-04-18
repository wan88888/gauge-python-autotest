import os
import time
import logging
from datetime import datetime
from PIL import Image

def setup_logging():
    """Setup logging configuration for the framework"""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f'test_run_{timestamp}.log')
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()

def take_screenshot(driver, name, error_context=None):
    """Take a screenshot and save it to the screenshots directory
    
    Args:
        driver: Webdriver instance
        name: Screenshot name
        error_context: Optional additional context about the error
    
    Returns:
        Path to the screenshot file or None if failed
    """
    screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'screenshots')
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'{name}_{timestamp}.png'
    screenshot_path = os.path.join(screenshot_dir, filename)
    
    try:
        driver.save_screenshot(screenshot_path)
        # 如果提供了错误上下文，记录到日志中
        logger = logging.getLogger(__name__)
        if error_context:
            logger.error(f"Screenshot taken: {filename} - Error context: {error_context}")
        else:
            logger.info(f"Screenshot taken: {filename}")
            
        # 返回相对路径以便在HTML报告中使用
        return os.path.join('screenshots', filename)
    except Exception as e:
        logging.error(f"Failed to take screenshot: {str(e)}")
        return None

def wait_for_element(driver, locator, timeout=10):
    """Wait for an element to be visible"""
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element
    except Exception as e:
        logging.error(f"Element not found: {str(e)}")
        return None

def retry(func, max_attempts=3, delay=1):
    """通用重试装饰器，适用于不稳定操作
    
    Args:
        func: 要重试的函数
        max_attempts: 最大重试次数
        delay: 重试间隔（秒）
        
    Returns:
        函数的执行结果或最后一次异常
    """
    def wrapper(*args, **kwargs):
        last_exception = None
        for attempt in range(max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                logging.warning(f"Attempt {attempt+1}/{max_attempts} failed: {str(e)}")
                if attempt < max_attempts - 1:
                    time.sleep(delay)
                else:
                    logging.error(f"All {max_attempts} attempts failed for {func.__name__}")
        raise last_exception
    return wrapper 