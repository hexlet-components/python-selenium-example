from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_WAIT = 10


def wait_for(driver: WebDriver, locator: Tuple[str, str], timeout: int = DEFAULT_WAIT) -> WebElement:
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))

