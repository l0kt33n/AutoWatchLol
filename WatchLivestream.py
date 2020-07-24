from time import sleep
sleep_time = 60*60


def live_checker():
    from twitch import TwitchClient

    client = TwitchClient(client_id='szwbnpgk8onxagzegef9wja3fd5s9r')
    channel_ids = ['124422593', '124420521']

    streams = []
    for channel_id in channel_ids:
        streams.append(client.streams.get_stream_by_user(channel_id))

    for stream in streams:
        if stream is not None:
            return True

    return False


def watch_livestream():
    from pyautogui import hotkey
    import webbrowser
    url = 'https://lolesports.com/live/'
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(chrome_path).open(url)
    sleep(sleep_time)
    hotkey('command', 'w')


def main():

    while True:
        live = live_checker()
        if live is True:
            watch_livestream()
        else:
            sleep(sleep_time)


if __name__ == "__main__":
    main()
