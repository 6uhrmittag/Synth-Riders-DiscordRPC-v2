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
import srt
from datetime import timedelta

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

def log_song_event(dt, event_type, song_info):
    """
    Log song start/stop events with all available song info.
    event_type: 'start' or 'stop'
    song_info: dict with song details or None
    """
    log_dir = os.path.join(script_dir, "log")
    os.makedirs(log_dir, exist_ok=True)
    log_file = f"rpc{dt}.log"
    log_path = os.path.join(log_dir, log_file)
    try:
        logging.basicConfig(
            filename=log_path,
            encoding="utf-8",
            level=logging.INFO,
            format="[%(asctime)s] %(message)s",
            force=True
        )
        logger = logging.getLogger("song_event")
        if event_type == 'start' and song_info:
            logger.info(f"SONG START: {json.dumps(song_info, ensure_ascii=False)}")
        elif event_type == 'stop' and song_info:
            logger.info(f"SONG STOP: {json.dumps(song_info, ensure_ascii=False)}")
        elif event_type == 'stop' and not song_info:
            logger.info("SONG STOP: No song info available.")
    except Exception as e:
        print(f"Failed to write song event to log: {e}")

def write_srt_event(dt, event_type, song_info, srt_state):
    """
    Write an SRT file with a 5 second subtitle block for song start/stop or idle.
    event_type: 'start', 'stop', or 'idle'
    song_info: dict with song details or None
    srt_state: dict to keep track of subtitle index and last end time
    """
    log_dir = os.path.join(script_dir, "log")
    os.makedirs(log_dir, exist_ok=True)
    srt_file = f"rpc{dt}.srt"
    srt_path = os.path.join(log_dir, srt_file)

    # Determine subtitle text
    if event_type == 'start' and song_info:
        text = f"START: {song_info.get('artist', 'Unknown')} - {song_info.get('song_name', 'Unknown')}"
    elif event_type == 'stop' and song_info:
        text = f"STOP: {song_info.get('artist', 'Unknown')} - {song_info.get('song_name', 'Unknown')}"
    else:
        text = "ideingling"

    # Determine start and end time for the subtitle
    # Use last end time if available, else start at 0
    start_td = srt_state.get('last_end', timedelta(seconds=0))
    end_td = start_td + timedelta(seconds=5)
    srt_state['last_end'] = end_td

    # Increment subtitle index
    srt_state['index'] = srt_state.get('index', 0) + 1
    subtitle = srt.Subtitle(index=srt_state['index'], start=start_td, end=end_td, content=text)

    # Append to SRT file (read existing, add, write back)
    subtitles = []
    if os.path.exists(srt_path):
        with open(srt_path, 'r', encoding='utf-8') as f:
            try:
                subtitles = list(srt.parse(f.read()))
            except Exception:
                subtitles = []
    subtitles.append(subtitle)
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(srt.compose(subtitles))

def rpc_loop(presence, song_watcher, config, dt_now=None, srt_state=None):
    prev_song_id = None
    prev_song_info = None
    if dt_now is None:
        dt_now = datetime.now().strftime("%Y%m%d%H%M%S%f")
    if srt_state is None:
        srt_state = {'index': 0, 'last_end': timedelta(seconds=0)}
    while True:
        if process_check():
            song_info = song_watcher.get_song_status()
            song_id = song_info.get('song_id') if song_info else None
            if song_id and song_id != prev_song_id:
                log_song_event(dt_now, 'start', song_info)
                write_srt_event(dt_now, 'start', song_info, srt_state)
            if prev_song_id and not song_id:
                log_song_event(dt_now, 'stop', prev_song_info)
                write_srt_event(dt_now, 'stop', prev_song_info, srt_state)
            prev_song_id = song_id
            prev_song_info = song_info if song_id else None
            presence.update_song_status(song_info, config)
            time.sleep(5)
        else:
            break
    presence.update_song_status(None, config)
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
    last_seen_running = time.time()
    not_running_since = None
    idle_timeout = 10 * 60  # 10 minutes in seconds
    rpc_active = False
    srt_state = None
    while True:
        try:
            pid = process_check()
            if pid:
                # If game is running again after being stopped, start new log/SRT
                if not rpc_active:
                    dt_now = datetime.now().strftime("%Y%m%d%H%M%S%f")
                    srt_state = {'index': 0, 'last_end': timedelta(seconds=0)}
                    try:
                        log_write(dt=dt_now, status="ok", app=pid, content=None)
                    except Exception:
                        pass
                    rpc_active = True
                last_seen_running = time.time()
                not_running_since = None
                rpc_loop(presence, song_watcher, config, dt_now=dt_now, srt_state=srt_state)
            else:
                if rpc_active:
                    # Mark the time when the process stopped
                    if not not_running_since:
                        not_running_since = time.time()
                    # Write idle SRT event
                    if srt_state is None:
                        srt_state = {'index': 0, 'last_end': timedelta(seconds=0)}
                    write_srt_event(dt_now, 'idle', None, srt_state)
                    try:
                        log_write(dt=dt_now, status="ok", app=False, content=None)
                    except Exception:
                        pass
                    # If not running for more than 10 minutes, finish log/SRT and reset
                    if time.time() - not_running_since > idle_timeout:
                        # Optionally, write a closing entry to log/SRT
                        try:
                            log_write(dt=dt_now, status="ok", app=None, content="Session ended after 10 minutes idle.")
                        except Exception:
                            pass
                        write_srt_event(dt_now, 'idle', None, srt_state)
                        rpc_active = False
                        dt_now = None
                        srt_state = None
                else:
                    # Not running and not active, just idle
                    pass
            time.sleep(5)
        except Exception as e:
            print(f"Error in main loop: {e}")
            try:
                if dt_now:
                    log_write(dt=dt_now, status="error", app=None, content=e)
            except Exception:
                pass
            break

if __name__ == "__main__":
    Thread(target=app_run, daemon=True).start()
    taskTray().run_program()
