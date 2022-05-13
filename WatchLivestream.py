from getpass import getpass
from sys import stdout, argv
from time import sleep
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

watch_time = 60 * 60
live_check_time = 60 * 30


def live_checker(client):
    """ Checks if the stream is live

    Args:
        client: TwitchHelix object

    Returns:
        boolean: True if the stream is live, False otherwise
    """
    print("Checking for live streams....")
    channels = {
        'lec': '124422593',
        'lcs': '124420521',
        'lpl': '124425627',
        'lck': '124425501',
        'cblol-brazil': '36511475',
        'lla': '142055874',
        'riotgames': '36029255'}

    try:
        if streams := client.get_streams(user_ids=channels.values()):
            for stream in streams:
                if 'REBROADCAST' not in stream['title'] and 'Rebroadcast' not in stream['title']:
                    print('{l} is live!'.format(l=stream['user_name']))
                    return True
    except Exception as e:
        print(e)
        print("Error checking for live streams, trying again in 30 minutes.")
        return False

    print("\nNo live streams found.")
    return False


def watch_livestream(driver):
    """ Watches the livestream

    Args:
        driver: Selenium webdriver object
    """
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
    try:
        element = WebDriverWait(driver, 90).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="btn-signin-submit"]'))
        )
    finally:
        driver.quit
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
    finally:
        driver.quit
    driver.set_window_size(200, 400)
    return


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

    if credentials['client_id'] == '':
        client_id = input("client_id: ")
    else:
        client_id = credentials['client_id']

    if credentials['client_secret'] == '':
        client_secret = getpass()
    else:
        client_secret = credentials['client_secret']

    from twitch import TwitchHelix
    client = TwitchHelix(client_id=client_id, client_secret=client_secret)
    client.get_oauth()

    while True:
        try:
            if driver is None:
                options = webdriver.ChromeOptions()
                options.add_experimental_option(
                    'excludeSwitches', ['enable-logging'])
                driver = webdriver.Chrome(options=options)
            if not logged_in:
                login(driver, username, password)
                logged_in = True
            if live := live_checker(client):
                watch_livestream(driver)
            else:
                for remaining in range(live_check_time, 0, -60 * 10):
                    stdout.write(str(int(remaining / 60)) + ' ')
                    stdout.flush()
                    sleep(60 * 10)
        except KeyboardInterrupt:
            print("Exiting....")
            if logged_in:
                driver.close()
            break


if __name__ == "__main__":
    main()
