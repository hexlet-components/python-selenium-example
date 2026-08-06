"""
Быстрый intro-скрипт для студентов.

Мы специально показываем только базовые сценарии на площадке
https://the-internet.herokuapp.com/. Каждый шаг подробно объясняется
в консоли — просто читайте текст, видите, что происходит, и повторяйте.

Что делает скрипт:
1. Логинится на тестовой форме и проверяет сообщение.
2. Включает чекбоксы и рассказывает, включён ли каждый из них.
3. Выбирает вариант из выпадающего списка.

Команды для запуска:
    make install
    make run-basic-selenium-demo

Chrome откроется в обычном режиме. Если хотите без окна браузера,
раскомментируйте строку с `--headless=new`.
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = "https://the-internet.herokuapp.com"


def run_form_auth(driver: webdriver.Chrome) -> None:
    """Открываем форму логина и проверяем, что сообщение стало зелёным."""
    print("\n[ШАГ 1] Заходим на страницу логина и вводим тестовые данные.")
    driver.get(f"{BASE_URL}/login")
    print("  -> Вписываем логин tomsmith")
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    print("  -> Вписываем пароль SuperSecretPassword!")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    print("  -> Нажимаем кнопку входа")
    driver.find_element(By.CSS_SELECTOR, "button.radius").click()

    flash = driver.find_element(By.ID, "flash").text
    print(f"  -> Сообщение на странице: {flash.strip()}")


def run_checkboxes(driver: webdriver.Chrome) -> None:
    """Находим два чекбокса и включаем каждый, проговаривая состояние."""
    print("\n[ШАГ 2] Работаем с чекбоксами.")
    driver.get(f"{BASE_URL}/checkboxes")
    boxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    for idx, box in enumerate(boxes, start=1):
        if not box.is_selected():
            print(f"  -> Чекбокс #{idx} был выключен. Включаем его.")
            box.click()
        else:
            print(f"  -> Чекбокс #{idx} уже был включён.")
        print(f"     Состояние чекбокса #{idx}: {box.is_selected()}")


def run_dropdown(driver: webdriver.Chrome) -> None:
    """Выбираем вторую опцию из dropdown и проговариваем результат."""
    print("\n[ШАГ 3] Переключаемся на выпадающий список (dropdown).")
    driver.get(f"{BASE_URL}/dropdown")
    dropdown = driver.find_element(By.ID, "dropdown")
    print("  -> Открываем список.")
    dropdown.click()
    print("  -> Выбираем вариант 'Option 2'.")
    dropdown.find_element(By.CSS_SELECTOR, "option[value='2']").click()
    selected = dropdown.find_element(By.CSS_SELECTOR, "option:checked").text
    print(f"  -> Сейчас выбрано: {selected}")


def main() -> None:
    options = Options()
    options.add_argument("--window-size=1280,960")
    # options.add_argument("--headless=new")

    print("=== СТАРТ ДЕМО ===")
    driver = webdriver.Chrome(options=options)
    run_form_auth(driver)
    run_checkboxes(driver)
    run_dropdown(driver)
    driver.quit()
    print("Хотите больше практики — посмотрите selenium_corner_cases_demo.py.")
    print(
        "Совет: попробуйте прогнать сценарий в режиме отладки, шаг за "
        "шагом — легче понять, как работают команды."
    )


if __name__ == "__main__":
    main()

