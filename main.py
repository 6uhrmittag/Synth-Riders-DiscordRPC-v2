import os
import time
import psutil
import logging
import json
from pystray import Icon, Menu, MenuItem
from PIL import Image
from threading import Thread
import sys
from datetime import datetime
import configparser
import requests
import webbrowser

# Import our new song status watcher
from song_status import SongStatusWatcher
from discordrp import Presence

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

def read_ini():
    conf = configparser.ConfigParser()
    path = "./settings/appinfo.ini"
    if os.path.isfile(path):
        conf.read(path, encoding="UTF-8")
    else:
        conf.read(rf"{script_dir}\settings\appinfo.ini", encoding="UTF-8")
    return conf["PROFILE"]["AppVersion"]

def read_server_ini():
    url = "https://raw.githubusercontent.com/6uhrmittag/Synth-Riders-DiscordRPC/refs/heads/master/settings/appinfo.ini"
    r = requests.get(url)
    conf = configparser.ConfigParser()
    conf.read_string(r.text)
    return conf["PROFILE"]["AppVersion"]

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class taskTray:
    def __init__(self):
        self.status = False

        image = Image.open(resource_path("assets/game_synthriders_logo_square.jpg"))

        local_version = read_ini()
        server_version = read_server_ini()

        if local_version != server_version:
            visible = True
        else:
            visible = False

        menu = Menu(
            MenuItem(f"Update is available! (->v{server_version})", self.open_gitpage, visible=visible),
            MenuItem(f"Version: {local_version}", enabled=False, action=None),
            MenuItem("Exit", self.stop_program),
        )

        self.icon = Icon(name="SynthRidersRPC", title="Synth Riders Discord RPC", icon=image, menu=menu)

    def open_gitpage(self):
        url = "https://github.com/6uhrmittag/Synth-Riders-DiscordRPC/releases"
        webbrowser.open(url)

    def stop_program(self, icon):
        self.status = False
        icon.stop()

    def run_program(self):
        self.status = True
        self.icon.run()

def get_config():
    try:
        with open("./settings/config.json", "r", encoding="UTF-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        with open(rf"{script_dir}\settings\config.json", "r", encoding="UTF-8") as f:
            data = json.load(f)

    return data

def process_check():
    for proc in psutil.process_iter():
        try:
            get_proc = proc.exe()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
        else:
            if "SynthRiders.exe" in get_proc:
                return proc.pid
    return False

def rpc_loop(presence, song_watcher, config):
    while True:
        if process_check():
            # Game is running, check for song updates
            song_info = song_watcher.get_song_status()
            presence.update_song_status(song_info, config)
            time.sleep(5)  # Check for updates every 5 seconds
        else:
            # Game is not running
            presence.update_song_status(None, config)
            time.sleep(15)  # Check less frequently when game is not running

            # If game was closed and restarted, we should check again sooner
            if process_check():
                continue

            # Game still not running after waiting
            break

    # Disconnect when done
    presence.disconnect()

def log_write(dt, status, app, content):
    os.makedirs("log", exist_ok=True)

    logger = logging.getLogger(__name__)
    log_path = rf"{script_dir}\log\rpc{dt}.log"
    logging.basicConfig(filename=log_path, encoding="utf-8", level=logging.INFO, format="[%(asctime)s] %(message)s")
    if status == "ok":
        if app:
            info_text = f"Synth Riders is running(PID: {app}). Executing RPC function."
        else:
            info_text = f"Synth Riders is not running. waiting..."
        logger.info(info_text)
    elif status == "error":
        logger.error(f"Unexpected error occurred.\n{content}")

def app_run():
    dt_now = datetime.now().strftime("%Y%m%d%H%M%S%f")
    try:
        config = get_config()

        # Initialize Discord Rich Presence
        discord_app_id = config.get("discord_application_id", "1124356298578870333")
        presence = Presence(discord_app_id)

        # Initialize Song Status Watcher
        song_watcher = SongStatusWatcher(config)

        while True:
            try:
                pid = process_check()
                if pid:
                    log_write(dt=dt_now, status="ok", app=pid, content=None)
                    rpc_loop(presence, song_watcher, config)
                else:
                    log_write(dt=dt_now, status="ok", app=False, content=None)
                time.sleep(15)
            except Exception as e:
                log_write(dt=dt_now, status="error", app=None, content=e)
                break
    except Exception as e:
        log_write(dt=dt_now, status="error", app=None, content=e)
        return

if __name__ == "__main__":
    Thread(target=app_run, daemon=True).start()
    taskTray().run_program()

