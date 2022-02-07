from getpass import getpass
from sys import stdout, argv
from time import sleep
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

watch_time = 60 * 60
live_check_time = 60 * 30


def live_checker():
    from twitch import TwitchClient

    client = TwitchClient(client_id="szwbnpgk8onxagzegef9wja3fd5s9r")
    channels = {
        'lec': '124422593',
        'lcs': '124420521',
        'lpl': '124425627',
        'lck': '124425501',
        'cblol': '36511475',
        'lla': '142055874',
        'riotgames': '36029255'}

    for channel in channels:
        stream = client.streams.get_stream_by_user(channels[channel])
        if stream is not None:
            print(stream.channel.status)
            if 'REBROADCAST' not in stream.channel.status and 'Rebroadcast' not in stream.channel.status:
                return channel

    return None


def watch_livestream(driver, league):
    if league == 'riotgames':
        url = 'https://lolesports.com/live/worlds/riotgames'
    else:
        url = 'https://lolesports.com/live/{l}/{l}'.format(l=league)
    driver.get(url)
    sleep(watch_time)


def login(driver, username, password):
    wait = WebDriverWait(driver, 10)
    driver.get('https://lolesports.com/')
    driver.maximize_window()

    login_button = driver.find_element(By.XPATH, '//*[@id="riotbar-right-content"]/div[3]/div/a')
    login_button.click()
    try:
        element = WebDriverWait(driver,90).until(
            EC.presence_of_element_located((By.NAME,'username'))
        )
    finally:
        driver.quit
    username_box = driver.find_element(By.NAME, 'username')
    username_box.send_keys(username)
    password_box = driver.find_element(By.NAME, 'password')
    password_box.send_keys(password)
    stay_signed_in = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/div/div[2]/div/div/div/div[4]/div[1]/label/input')
    stay_signed_in.click()
    driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/div/button').click()
    try:
        element = WebDriverWait(driver,90).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="riotbar-right-content"]/div[3]'))
            )
    finally:
        driver.quit
    driver.set_window_size(200,400)
    return


def main():
    logged_in = False
    driver = None
    if len(argv) == 1:
        filename = input("Credential Filename: ")
    else:
        filename = argv[1]
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
                driver = webdriver.Chrome(executable_path='/home/pi/AutoWatchLol/chromedriver')
            if logged_in is False:
                login(driver, username, password)
                logged_in = True
            league = live_checker()
            if league is not None:
                print('{l} is live, opening chrome.....'.format(l=league.upper()))
                watch_livestream(driver, league)
            else:
                print("No channel is live, checking in 30 minutes.")
                for remaining in range(live_check_time, 0, -60 * 10):
                    stdout.write(str(int(remaining / 60)) + ' ')
                    stdout.flush()
                    sleep(60 * 10)
        except KeyboardInterrupt:
            print("Exiting....")
            if logged_in is True:
                driver.close()
            break


if __name__ == "__main__":
    main()
