"""
Продвинутый скрипт для corner-case действий на публичной странице.

Используем официальный демо-сайт Selenium:
https://www.selenium.dev/selenium/web/web-form.html

Пошагово демонстрируем:
* очистку поля сочетанием Ctrl+A + Delete;
* заполнение пароля и textarea;
* проверку disabled/readonly полей;
* выбор из select и datalist стрелками клавиатуры;
* работу с чекбоксом/радиокнопкой;
* установку цвета, даты и значения range-слайдера;
* hover-эффект и отправку формы.

Запуск:
    uv venv --python 3.14
    uv sync --python 3.14
    uv add selenium
    uv run examples/selenium_corner_cases_demo.py
"""

from __future__ import annotations

import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

FORM_URL = "https://www.selenium.dev/selenium/web/web-form.html"
WAIT_SECONDS = 10


def wait_for(
    driver: webdriver.Chrome, locator: tuple[str, str]
) -> webdriver.remote.webelement.WebElement:
    return WebDriverWait(driver, WAIT_SECONDS).until(
        EC.visibility_of_element_located(locator)
    )


def run_demo(driver: webdriver.Chrome) -> None:
    print("=== СТАРТ CORNER-CASE ДЕМО ===")
    driver.get(FORM_URL)

    # Текстовое поле
    text_input = wait_for(driver, (By.NAME, "my-text"))
    print("\n[ШАГ 1] Работаем с текстовым полем.")
    text_input.send_keys("Hexlet Student")
    text_input.send_keys(
        Keys.CONTROL, "a"
    )  # Ctrl+A обязательно, потому что .clear() в подобных формах не работает
    text_input.send_keys(Keys.DELETE)
    text_input.send_keys("QA Student")
    print(
        "  -> Значение после очистки и ввода: "
        f"{text_input.get_attribute('value')}"
    )

    # Пароль и textarea
    password = driver.find_element(By.NAME, "my-password")
    textarea = driver.find_element(By.NAME, "my-textarea")
    print("\n[ШАГ 2] Пароль + textarea.")
    password.send_keys("SuperSecret123")
    textarea.send_keys("Selenium corner cases demo.")
    print("  -> Поля заполнены.")

    # Disabled и readonly
    disabled = driver.find_element(By.NAME, "my-disabled")
    readonly = driver.find_element(By.NAME, "my-readonly")
    print("\n[ШАГ 3] Проверяем состояние disabled/readonly.")
    print(f"  -> disabled? {not disabled.is_enabled()}")
    print(f"  -> readonly? {readonly.get_attribute('readonly') is not None}")

    # Select
    print("\n[ШАГ 4] Работаем с select.")
    select = Select(driver.find_element(By.NAME, "my-select"))
    select.select_by_visible_text("Two")
    print(f"  -> Выбрали: {select.first_selected_option.text}")

    # Datalist
    print("\n[ШАГ 5] Datalist + клавиатура.")
    datalist = wait_for(driver, (By.CSS_SELECTOR, "input[list]"))
    datalist.send_keys("Ch")
    time.sleep(0.5)
    datalist.send_keys(Keys.ARROW_DOWN)
    datalist.send_keys(Keys.TAB)
    datalist_value = driver.find_element(
        By.CSS_SELECTOR, "input[list]"
    ).get_attribute("value")
    print(f"  -> Значение в datalist: {datalist_value}")

    # Checkbox и radio
    print("\n[ШАГ 6] Чекбокс и радиокнопка.")
    wait_for(driver, (By.NAME, "my-check"))
    checkboxes = driver.find_elements(By.NAME, "my-check")
    primary_checkbox = checkboxes[1] if len(checkboxes) > 1 else checkboxes[0]
    radios = driver.find_elements(By.NAME, "my-radio")
    primary_radio = radios[-1]

    if not primary_checkbox.is_selected():
        primary_checkbox.click()
    if not primary_radio.is_selected():
        primary_radio.click()
    print(
        f"  -> Чекбокс #{primary_checkbox.get_attribute('id')} "
        f"выбран? {primary_checkbox.is_selected()}; "
        f"Радио #{primary_radio.get_attribute('id')}? "
        f"{primary_radio.is_selected()}"
    )

    # Color + date + range
    print("\n[ШАГ 7] Цвет, дата и range.")
    color = driver.find_element(By.NAME, "my-colors")
    color.send_keys("#ff5733")
    date = driver.find_element(By.NAME, "my-date")
    date.clear()
    date.send_keys("2025-01-15")
    slider = driver.find_element(By.NAME, "my-range")
    # Используем JavaScript: стандартный send_keys для range
    # срабатывает не всегда.
    driver.execute_script(
        "arguments[0].value = arguments[1];"
        "arguments[0].dispatchEvent(new Event('input'));",
        slider,
        "7",
    )
    print(
        f"  -> Цвет: {color.get_attribute('value')}, "
        f"Дата: {date.get_attribute('value')}, "
        f"Range: {slider.get_attribute('value')}"
    )

    # Hover
    print("\n[ШАГ 8] Hover по кнопке Submit.")
    submit_button = driver.find_element(
        By.CSS_SELECTOR, "button[type='submit']"
    )
    ActionChains(driver).move_to_element(submit_button).perform()
    print("  -> Навели курсор на кнопку отправки.")

    # Отправка формы
    print("\n[ШАГ 9] Отправляем форму.")
    submit_button.click()
    try:
        confirmation = wait_for(driver, (By.TAG_NAME, "h1"))
        print(f"  -> Ответ страницы: {confirmation.text}")
    except TimeoutException:
        print(
            "  -> Ответ страницы появился без заголовка h1. Проверьте вручную."
        )


def main() -> None:
    options = Options()
    options.add_argument("--window-size=1440,900")
    # options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    try:
        run_demo(driver)
        print(
            "\nВсе шаги выполнены. Для закрытия окна используйте "
            "Debug/Step Over, "
            "чтобы проследить логику, или вызовите driver.quit() вручную."
        )
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
