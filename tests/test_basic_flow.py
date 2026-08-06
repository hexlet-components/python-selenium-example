from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .utils import wait_for

BASE_URL = "https://the-internet.herokuapp.com"


def enable_checkbox(driver, checkbox) -> None:
    """Включает чекбокс, если он выключен.

    На внешних сайтах синтетический клик в headed-режиме иногда
    «теряется» (не доходит до элемента), поэтому проверяем состояние
    после клика и при необходимости повторяем. Если обычные клики
    не помогают — используем JS-клик как запасной вариант.
    """
    for _ in range(3):
        if checkbox.is_selected():
            return
        checkbox.click()
        try:
            WebDriverWait(driver, 2).until(
                lambda d: checkbox.is_selected()
            )
            return
        except TimeoutException:
            continue
    driver.execute_script("arguments[0].click()", checkbox)


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

    checkboxes = driver.find_elements(
        By.CSS_SELECTOR, "#checkboxes input[type='checkbox']"
    )
    assert len(checkboxes) == 2
    checkbox1, checkbox2 = checkboxes

    for checkbox in (checkbox1, checkbox2):
        enable_checkbox(driver, checkbox)
        assert checkbox.is_selected()

    driver.get(f"{BASE_URL}/dropdown")
    dropdown = wait_for(driver, (By.ID, "dropdown"))
    dropdown.click()
    dropdown.find_element(By.CSS_SELECTOR, "option[value='2']").click()

    selected_text = dropdown.find_element(
        By.CSS_SELECTOR, "option:checked"
    ).text
    assert selected_text == "Option 2"

