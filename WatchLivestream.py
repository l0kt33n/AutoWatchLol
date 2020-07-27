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
    channels = {'lec': '124422593', 'lcs': '124420521'}

    for channel in channels:
        if client.streams.get_stream_by_user(channels[channel]) is not None:
            return channel
        else:
            continue

    return None



def watch_livestream(driver, league):
    url = 'https://lolesports.com/live/{l}/{l}'.format(l=league)
    driver.get(url)
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
        league = live_checker()
        if league is not None:
            if driver is None:
                driver = webdriver.Chrome(ChromeDriverManager().install())
            if logged_in is False:
                login(driver)
                logged_in = True
            watch_livestream(driver, league)
        else:
            sleep(live_check_time)


if __name__ == "__main__":
    main()
