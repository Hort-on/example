from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def test_login(driver, username, password):
    print("Перехід на сторінку лоігну...")
    driver.get("http://127.0.0.1:8000/home/login/")

    print("Ввід електронної пошти і паролю...")
    username_field = driver.find_element(By.NAME, "email")
    username_field.send_keys(username)
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)
    time.sleep(3)

    print("Пдітвердження логіну...")
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(3)
    print("Перенаправлення на домашню сторінку...")


def test_logout(driver):
    logout_link = driver.find_element(By.XPATH, "//a[text()='Logout']")
    logout_link.click()

    print("Користувач успішно вийшов із системи!")
    time.sleep(3)


def test_login_process(driver, valid_username, valid_password, invalid_username, invalid_password):
    print("Ввід валідних даних...")
    test_login(driver, valid_username, valid_password)
    time.sleep(3)

    def is_user_logged_in(driver):
        try:
            driver.find_element(By.LINK_TEXT, "Logout")
            print("Користувач успішно увійшов!")
            time.sleep(3)
            return True
        except:
            print("Користувач не увійшов!")
            return False

    assert is_user_logged_in(driver)

    print("Вихід зі системи")
    test_logout(driver)
    assert not is_user_logged_in(driver)
    time.sleep(3)

    print("Ввід фейкових даних...")
    test_login(driver, invalid_username, invalid_password)
    assert not is_user_logged_in(driver)


def main():
    driver = webdriver.Chrome()
    valid_username = ""
    valid_password = ""
    invalid_username = ""
    invalid_password = ""

    test_login_process(driver, valid_username, valid_password, invalid_username, invalid_password)

    driver.close()


if __name__ == "__main__":
    main()
