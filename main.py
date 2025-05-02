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
import asyncio

# Import our new song status watcher
from song_status import SongStatusWatcher
from discordrp import Presence

# Setup basic stderr logging for critical errors that might occur before proper logging setup
logging.basicConfig(
    level=logging.ERROR,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    stream=sys.stderr
)

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
    try:
        url = "https://raw.githubusercontent.com/6uhrmittag/Synth-Riders-DiscordRPC/master/settings/appinfo.ini"
        r = requests.get(url)
        if r.status_code == 200:
            conf = configparser.ConfigParser()
            conf.read_string(r.text)
            return conf["PROFILE"]["AppVersion"]
        else:
            # Return local version if server version can't be accessed
            return read_ini()
    except Exception as e:
        logging.error(f"Error fetching server version: {e}")
        # Return local version as fallback
        return read_ini()

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class taskTray:
    def __init__(self):
        self.status = False

        try:
            image = Image.open(resource_path("assets/game_synthriders_logo_square.jpg"))
        except Exception as e:
            logging.error(f"Error loading icon image: {e}")
            # Use a blank image as fallback
            image = Image.new('RGB', (64, 64), color = 'blue')

        try:
            local_version = read_ini()
            server_version = read_server_ini()

            # Only show update menu if server version is different and not a fallback
            visible = local_version != server_version and server_version != local_version
        except Exception as e:
            logging.error(f"Error checking versions: {e}")
            local_version = "Unknown"
            server_version = "Unknown"
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
    # Create log directory using correct path handling
    log_dir = os.path.join(script_dir, "log")
    os.makedirs(log_dir, exist_ok=True)

    # Use os.path.join for cross-platform path handling
    log_file = f"rpc{dt}.log"
    log_path = os.path.join(log_dir, log_file)
    
    try:
        # Configure logging for file output
        logging.basicConfig(
            filename=log_path, 
            encoding="utf-8", 
            level=logging.INFO, 
            format="[%(asctime)s] %(message)s",
            force=True  # Force reconfiguration to handle multiple calls
        )
        
        logger = logging.getLogger(__name__)
        
        if status == "ok":
            if app:
                info_text = f"Synth Riders is running(PID: {app}). Executing RPC function."
            else:
                info_text = f"Synth Riders is not running. waiting..."
            logger.info(info_text)
        elif status == "error":
            logger.error(f"Unexpected error occurred.\n{content}")
    except Exception as e:
        # Fallback to console logging if file logging fails
        print(f"Failed to write to log: {e}")
        print(f"Status: {status}, Content: {content}")

import asyncio

def app_run():
    dt_now = datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    try:
        # Set up an event loop for this thread
        asyncio.set_event_loop(asyncio.new_event_loop())
        
        # First, try to write a test log entry to verify logging works
        try:
            log_write(dt=dt_now, status="ok", app=None, content="Starting application")
        except Exception as log_error:
            print(f"Warning: Logging setup failed: {log_error}")
            # Continue without file logging if it fails
        
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
                    try:
                        log_write(dt=dt_now, status="ok", app=pid, content=None)
                    except Exception:
                        # Continue if logging fails
                        pass
                    rpc_loop(presence, song_watcher, config)
                else:
                    try:
                        log_write(dt=dt_now, status="ok", app=False, content=None)
                    except Exception:
                        # Continue if logging fails
                        pass
                time.sleep(15)
            except Exception as e:
                print(f"Error in main loop: {e}")
                try:
                    log_write(dt=dt_now, status="error", app=None, content=e)
                except Exception:
                    # If logging itself fails, just print to console
                    pass
                break
    except Exception as e:
        print(f"Critical error in app_run: {e}")
        try:
            log_write(dt=dt_now, status="error", app=None, content=e)
        except Exception:
            # If logging fails, at least we printed to console above
            pass
        return

if __name__ == "__main__":
    Thread(target=app_run, daemon=True).start()
    taskTray().run_program()

