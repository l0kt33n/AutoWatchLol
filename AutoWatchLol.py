import argparse
import pickle
import re
import time

import pyautogui
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def vod_list_retriever(league_url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(100)
    driver.get(league_url)
    time.sleep(10)
    page = BeautifulSoup(driver.page_source, 'html.parser')
    links = []
    for link in page.findAll('a', attrs={'href': re.compile("/vod/")}):
        links.append(link.get('href')[5:])

    driver.quit()
    return links


def new_tab():
    pyautogui.hotkey('command', 't')
    time.sleep(1)


def close_tab():
    pyautogui.hotkey('command', 'w')
    time.sleep(1)


def next_tab():
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(1)


def close_and_open_new():
    new_tab()
    next_tab()
    close_tab()


def go_to_address_bar():
    pyautogui.hotkey('command', 'l')
    time.sleep(1)


def vod_link_maker(vod_num):
    return 'watch.lolesports.com/vod/' + vod_num


def auto_watch(vod_list):
    pyautogui.PAUSE = 3
    pyautogui.FAILSAFE = True

    for vod in vod_list:
        go_to_address_bar()
        pyautogui.write(vod_link_maker(vod))
        pyautogui.press('enter')
        watch_time = 660
        time.sleep(watch_time)
        close_and_open_new()

    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--f", default=0, type=str, help="Fetching new Vod lists and save it locally.")
    parser.add_argument("--s", default=0, type=str, help="Execute the script to watch Lol automatically.")

    args = parser.parse_args()
    if args.f:
        print("Retrieving VOD List, please wait.....")
        links = vod_list_retriever(args.f)
        print("VOD List retrieving, saving to 'links.p'.....")
        pickle.dump(links, open("links.p", "wb"))
        print("Links saved, exiting......")

    if args.s:
        print("Opening saved VOD list.....")
        links = pickle.load(open(args.s, "rb"))
        print("VOD list opened. Please switch to Safari Window. Script will execute in")
        for i in [5, 4, 3, 2, 1, 0]:
            print(i)
            time.sleep(1)
        auto_watch(links)


if __name__ == "__main__":
    main()
