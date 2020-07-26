from time import sleep

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

watch_time = 60 * 60
live_check_time = 60 * 30


def live_checker():
    from twitch import TwitchClient

    client = TwitchClient(client_id='szwbnpgk8onxagzegef9wja3fd5s9r')
    # channel_ids = ['124422593', '124420521', '36029255', '46273272', '36511475', '36513760', '72977645', '107870305',
    #               '124425627', '104833324']
    channel_ids = ['124422593', '124420521']

    streams = []
    for channel_id in channel_ids:
        streams.append(client.streams.get_stream_by_user(channel_id))

    for stream in streams:
        if stream is not None:
            return True

    return False


def watch_livestream(driver):
    url = 'https://lolesports.com/live/'
    driver.get(url)
    driver.implicitly_wait(5)
    try:
        driver.find_element_by_class_name('options-button').click()
        driver.find_element_by_class_name('option').click()
        driver.find_element_by_css_selector(
                'body > div:nth-child(12) > main > main > div > div.lower > div.nav-details > div > div.stream-selector > div > div.watch-options > div > div.options-section.provider-selection > ul > li.option.twitch').click()
    except (ElementNotInteractableException, NoSuchElementException):
        pass
    sleep(watch_time)


def login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get('https://lolesports.com/')
    login_button = wait.until(EC.element_to_be_clickable((By.ID, 'riotbar-account')))
    login_button.click()
    driver.implicitly_wait(5)
    username = driver.find_element_by_css_selector(
        'body > div > div > div > div.grid.grid-direction__row.grid-page-web__content > div.grid.grid-direction__column.grid-page-web__wrapper > div > div.grid.grid-align-center.grid-justify-space-between.grid-fill.grid-direction__column.grid-panel-web__content.grid-panel__content > div > div > div > div.field.field--focus.field--animate > div > input')
    username.send_keys("singlevelNA")
    password = driver.find_element_by_css_selector(
        'body > div > div > div > div.grid.grid-direction__row.grid-page-web__content > div.grid.grid-direction__column.grid-page-web__wrapper > div > div.grid.grid-align-center.grid-justify-space-between.grid-fill.grid-direction__column.grid-panel-web__content.grid-panel__content > div > div > div > div.field.password-field.field--animate > div > input')
    password.send_keys("Yjl3414458")
    stay_signed_in = driver.find_element_by_css_selector(
        'body > div > div > div > div.grid.grid-direction__row.grid-page-web__content > div.grid.grid-direction__column.grid-page-web__wrapper > div > div.grid.grid-align-center.grid-justify-space-between.grid-fill.grid-direction__column.grid-panel-web__content.grid-panel__content > div > div > div > div.grid.grid-justify-space-between.grid-direction__row > div.mobile-checkbox.signin-checkbox > label > input[type=checkbox]')
    stay_signed_in.click()
    driver.find_element_by_css_selector(
        'body > div > div > div > div.grid.grid-direction__row.grid-page-web__content > div.grid.grid-direction__column.grid-page-web__wrapper > div > button').click()
    wait.until(EC.element_to_be_clickable((By.ID, 'riotbar-account')))
    return


def main():
    logged_in = False
    driver = None
    while True:
        live = live_checker()
        if live is True:
            if driver is None:
                driver = webdriver.Chrome(ChromeDriverManager().install())
            if logged_in is False:
                login(driver)
                logged_in = True
            watch_livestream(driver)
        else:
            sleep(live_check_time)


if __name__ == "__main__":
    main()
