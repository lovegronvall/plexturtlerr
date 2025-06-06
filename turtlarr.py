#!/usr/bin/env python3

import os
import time
import requests
import configparser
import logging

# Read config using configparser
config = configparser.ConfigParser()
if os.path.exists("/config/turtlarr.conf"):
    config.read("/config/turtlarr.conf")
elif os.path.exists("config/turtlarr.conf"):
    config.read("config/turtlarr.conf")
elif os.path.exists("turtlarr.conf"):
    config.read("turtlarr.conf")
else:
    logging.error("No config file found!")
    exit()

DEBUG = config.get("settings", "DEBUG").lower() in ['true', 'yes', 'y', '1']
if DEBUG:
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO

# Set logging config
logging.basicConfig(
    format = '%(asctime)s %(levelname)s: %(message)s',
    level = loglevel
)

PLEX_URL = config.get("plex", "PLEX_URL")
PLEX_TOKEN = config.get("plex", "PLEX_TOKEN")
POLL_INTERVAL = int(config.get("plex", "POLL_INTERVAL"))

QBITTORRENT_URL = config.get("qbittorrent", "QBITTORRENT_URL")
QBITTORRENT_USERNAME = config.get("qbittorrent", "QBITTORRENT_USERNAME")
QBITTORRENT_PASSWORD = config.get("qbittorrent", "QBITTORRENT_PASSWORD")

# Returns the number of current streams from the plex server
def plex_sessions():
    url = f"{PLEX_URL}/status/sessions"
    response = requests.get(url, headers={"Accept": "application/json", "X-Plex-Token": PLEX_TOKEN})
    logging.debug(f"Plex response: {response}")
    response.raise_for_status()
    streamers = response.json().get('MediaContainer', {}).get('size', {})
    return streamers

# Log in to qBittorrent
def qb_login(session):
    login_url = f'{QBITTORRENT_URL}/api/v2/auth/login'
    response = session.post(login_url, data={'username': QBITTORRENT_USERNAME, 'password': QBITTORRENT_PASSWORD})
    if response.text != 'Ok.':
        raise Exception(f"qBittorrent login failed: {response.text}")

# Enable or disable turtle mode in qBittorrent
def qb_turtle(session, enable=True):
    toggle_url = f'{QBITTORRENT_URL}/api/v2/transfer/toggleSpeedLimitsMode'
    check_url = f'{QBITTORRENT_URL}/api/v2/transfer/speedLimitsMode'
    response = session.get(check_url)
    logging.debug(f"qBittorrent check turtle output: {response.text}")
    turtle_enabled = bool(int(response.text))
    logging.info(f"qBittorrent turtle enabled: {turtle_enabled}")
    if turtle_enabled != enable:
        logging.info("Toggle turtle mode")
        response = session.post(toggle_url)
        logging.debug(f"qBittorrent toggle turtle output: {response.text}")


def main():
    logging.info("Starting turtlarr")
    currently_streaming = False
    was_streaming = False

    while True:
        try:
            streamers = plex_sessions()
            logging.debug(f"Number of streamers: {streamers}")

            if streamers > 0:
                currently_streaming = True
            else:
                currently_streaming = False

            logging.debug(f"Currently streaming: {currently_streaming}")

            # We only need to take action when we change streaming state
            if currently_streaming != was_streaming:
                if currently_streaming:
                    logging.info("Streaming started")
                else:
                    logging.info("Streaming stopped")
                with requests.Session() as session:
                   try:
                       qb_login(session)
                       # Turtle mode should be enabled when we're streaming
                       qb_turtle(session, enable=currently_streaming)
                   except Exception as e:
                       logging.error(f"qbittorrent speed toggle error: {e}")
                # Remember if we are streaming or not
                was_streaming = currently_streaming

        except Exception as e:
            logging.error(f"Error checking sessions: {e}")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()

