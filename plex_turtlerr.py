import time
import requests
from plex_turtlerr_cfg import *

plex_headers = {
    "Accept": "application/json",
    "X-Plex-Token": PLEX_TOKEN
}

def plex_sessions():
    url = f"{PLEX_URL}/status/sessions"
    response = requests.get(url, headers=plex_headers)
    if __debug__:
        print(f"Plex response: {response}")
    response.raise_for_status()
    return response.json()

def qb_login(session):
    login_url = f'{QBITTORRENT_URL}/api/v2/auth/login'
    response = session.post(login_url, data={'username': QBITTORRENT_USERNAME, 'password': QBITTORRENT_PASSWORD})
    if response.text != 'Ok.':
        raise Exception(f"qBittorrent login failed: {response.text}")

def qb_toggle_alt_speed_limits(session, enable=True):
    toggle_url = f'{QBITTORRENT_URL}/api/v2/transfer/toggleSpeedLimitsMode'
    check_url = f'{QBITTORRENT_URL}/api/v2/transfer/speedLimitsMode'
    response = session.get(check_url)
    if __debug__:
        print(f"qBittorrent check turtle output: {response.text}")
    turtle_enabled = response.text
    if ("0" in turtle_enabled) and enable:
        print("Enabling turtle")
        response = session.post(toggle_url)
        if __debug__:
            print(f"qBittorrent toggle turtle output: {response.text}")
    if ("1" in turtle_enabled) and enable==False:
        print("Disabling turtle")
        response = session.post(toggle_url)
        if __debug__:
            print(f"qBittorrent toggle turtle output: {response.text}")


def main():
    print("Starting Plex Turtlerr")
    currently_streaming = False
    was_streaming = False

    while True:
        try:
            data = plex_sessions()
            if __debug__:
                print(f"Data: {data}")
            streamers = data.get('MediaContainer', {}).get('size', {})
            if __debug__:
                print(f"Number of streamers: {streamers}")

            if streamers > 0:
                currently_streaming = True
            else:
                currently_streaming = False

            if __debug__:
                print(f"Currently streaming: {currently_streaming}")

            if currently_streaming != was_streaming:
                if currently_streaming:
                   print("Streaming started")
                   with requests.Session() as session:
                       try:
                           qb_login(session)
                           qb_toggle_alt_speed_limits(session, enable=True)
                       except Exception as e:
                           print(f"Error: {e}")

                else:
                    print("Streaming stopped")
                    with requests.Session() as session:
                       try:
                           qb_login(session)
                           qb_toggle_alt_speed_limits(session, enable=False)
                       except Exception as e:
                           print(f"Error: {e}")

                was_streaming = currently_streaming

        except Exception as e:
            print("Error checking sessions: {e}")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()

