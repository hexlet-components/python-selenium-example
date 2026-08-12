from collections.abc import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def driver() -> Generator[webdriver.Chrome, None, None]:
    options = Options()
    options.add_argument("--window-size=1440,900")
    # options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
