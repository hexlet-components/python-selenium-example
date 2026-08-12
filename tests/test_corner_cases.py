from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from .utils import wait_for

FORM_URL = "https://www.selenium.dev/selenium/web/web-form.html"


def test_corner_case_controls(driver):
    driver.get(FORM_URL)

    text_input = wait_for(driver, (By.NAME, "my-text"))
    text_input.send_keys("Hexlet Student")
    text_input.send_keys(Keys.CONTROL, "a")
    text_input.send_keys(Keys.DELETE)
    text_input.send_keys("QA Student")
    assert text_input.get_attribute("value") == "QA Student"

    password = driver.find_element(By.NAME, "my-password")
    textarea = driver.find_element(By.NAME, "my-textarea")
    password.send_keys("SuperSecret123")
    textarea.send_keys("Selenium corner cases demo.")

    disabled = driver.find_element(By.NAME, "my-disabled")
    readonly = driver.find_element(By.NAME, "my-readonly")
    assert not disabled.is_enabled()
    assert readonly.get_attribute("readonly") is not None

    select = driver.find_element(By.NAME, "my-select")
    select.find_element(By.CSS_SELECTOR, "option[value='2']").click()
    selected_text = select.find_element(By.CSS_SELECTOR, "option:checked").text
    assert selected_text == "Two"

    datalist = wait_for(driver, (By.CSS_SELECTOR, "input[list]"))
    datalist.send_keys("Ch")
    WebDriverWait(driver, 5).until(
        lambda drv: drv.find_element(By.CSS_SELECTOR, "input[list]")
        .get_attribute("value")
        .lower()
        .startswith("ch")
    )
    datalist.send_keys(Keys.ARROW_DOWN)
    datalist.send_keys(Keys.TAB)
    datalist_value = driver.find_element(
        By.CSS_SELECTOR, "input[list]"
    ).get_attribute("value")
    assert datalist_value.lower().startswith("ch")

    checkbox = wait_for(driver, (By.NAME, "my-check"))
    if not checkbox.is_selected():
        checkbox.click()
    assert checkbox.is_selected()

    radio = driver.find_elements(By.NAME, "my-radio")[-1]
    if not radio.is_selected():
        radio.click()
    assert radio.is_selected()

    color = driver.find_element(By.NAME, "my-colors")
    color.send_keys("#ff5733")
    date = driver.find_element(By.NAME, "my-date")
    date.clear()
    date.send_keys("2025-01-15")
    slider = driver.find_element(By.NAME, "my-range")
    driver.execute_script(
        "arguments[0].value = arguments[1];"
        "arguments[0].dispatchEvent(new Event('input'));",
        slider,
        "7",
    )
    assert color.get_attribute("value") == "#ff5733"
    assert date.get_attribute("value") == "2025-01-15"
    assert slider.get_attribute("value") == "7"

    submit_button = driver.find_element(
        By.CSS_SELECTOR, "button[type='submit']"
    )
    ActionChains(driver).move_to_element(submit_button).perform()
    submit_button.click()

    heading = wait_for(driver, (By.TAG_NAME, "h1"))
    assert heading.text.strip() == "Form submitted"
