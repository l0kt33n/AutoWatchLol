from getpass import getpass
from sys import stdout, argv
from time import sleep
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

watch_time = 60 * 60


def watch_livestream(driver):
    """ Watches the livestream

    Args:
        driver: Selenium webdriver object
    """
    driver.set_window_size(200, 400)
    url = 'https://lolesports.com/live/'
    driver.get(url)
    league = driver.current_url.split("/live/")[-1].split('/')[0]
    if league == 'msi':
        url = url + league + '/' + 'riotgames'
    else:
        url = url + league + '/' + league
    driver.get(url)
    sleep(30)
    driver.set_network_conditions(
        offline=False,
        latency=0,  # additional latency (ms)
        download_throughput=500 * 1024,  # maximal throughput
        upload_throughput=500 * 1024)  # maximal throughput
    sleep(watch_time)


def login(driver, username, password):
    """ Logs into the website

    Args:
        driver: Selenium webdriver object
        username (str): Username
        password (str): Password
    """
    wait = WebDriverWait(driver, 10)
    driver.maximize_window()

    driver.get('https://lolesports.com/')

    login_button = driver.find_element(
        By.CSS_SELECTOR, "#riotbar-right-content > div.undefined.riotbar-account-reset._2f9sdDMZUGg63xLkFmv-9O.riotbar-account-container > div > a")
    login_button.click()
    sleep(1)

    if driver.current_url == 'https://lolesports.com/':
        return
    try:
        element = WebDriverWait(driver, 90).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="btn-signin-submit"]'))
        )
    except Exception as e:
        driver.quit()
    username_box = driver.find_element(By.NAME, 'username')
    username_box.send_keys(username)
    password_box = driver.find_element(By.NAME, 'password')
    password_box.send_keys(password)
    stay_signed_in = driver.find_element(
        By.CSS_SELECTOR, '[data-testid="checkbox-remember-me"]')
    stay_signed_in.click()
    driver.find_element(
        By.CSS_SELECTOR, '[data-testid="btn-signin-submit"]').click()
    try:
        element = WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.ID, 'riotbar-account-bar'))
        )
    except Exception as e:
        driver.quit()
    return


def init_webdriver(username):
    from os import path, getcwd
    from webdriver_manager.chrome import ChromeDriverManager

    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=' +
                         path.join(getcwd(), 'chrome_data', username,))
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=options)

    return driver


def main():
    logged_in = False
    driver = None

    filename = input("Credential Filename: ") if len(argv) == 1 else argv[1]
    f = open(filename)
    credentials = json.load(f)

    if credentials['username'] == '':
        username = input("Username: ")
    else:
        username = credentials['username']

    if credentials['password'] == '':
        password = getpass()
    else:
        password = credentials['password']

    while True:
        try:
            if driver is None:
                driver = init_webdriver(username)
            if not logged_in:
                login(driver, username, password)
                logged_in = True
            watch_livestream(driver)
        except BaseException as e:
            print("Exiting because of error: " + str(e))
            if driver:
                driver.close()
            break


if __name__ == "__main__":
    main()
