from selenium.webdriver.common.by import By

from .utils import wait_for

BASE_URL = "https://the-internet.herokuapp.com"


def test_login_flow(driver):
    driver.get(f"{BASE_URL}/login")

    username = wait_for(driver, (By.ID, "username"))
    username.send_keys("tomsmith")

    password = driver.find_element(By.ID, "password")
    password.send_keys("SuperSecretPassword!")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    flash = wait_for(driver, (By.ID, "flash"))
    assert "You logged into a secure area!" in flash.text


def test_checkboxes_and_dropdown(driver):
    driver.get(f"{BASE_URL}/checkboxes")

    checkbox1 = driver.find_element(By.CSS_SELECTOR, "#checkboxes input:nth-child(1)")
    checkbox2 = driver.find_element(By.CSS_SELECTOR, "#checkboxes input:nth-child(3)")

    if not checkbox1.is_selected():
        checkbox1.click()

    assert checkbox1.is_selected()
    assert checkbox2.is_selected()

    driver.get(f"{BASE_URL}/dropdown")
    dropdown = wait_for(driver, (By.ID, "dropdown"))
    dropdown.click()
    dropdown.find_element(By.CSS_SELECTOR, "option[value='2']").click()

    selected_text = dropdown.find_element(By.CSS_SELECTOR, "option:checked").text
    assert selected_text == "Option 2"

