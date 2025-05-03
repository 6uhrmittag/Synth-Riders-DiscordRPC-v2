import time
import os
from pypresence import Presence as PyPresence

class Presence:
    """
    Discord Rich Presence integration for Synth Riders
    """
    def __init__(self, client_id):
        self.client_id = client_id
        self.rpc = PyPresence(client_id)
        self.connected = False
        self.start_time = int(time.time())

    def connect(self):
        """
        Connect to Discord Rich Presence
        """
        try:
            self.rpc.connect()
            self.connected = True
            return True
        except Exception as e:
            print(f"Failed to connect to Discord: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """
        Disconnect from Discord Rich Presence
        """
        if self.connected:
            try:
                self.rpc.close()
            except:
                pass
            self.connected = False

    def set(self, data):
        """
        Set the Discord Rich Presence status
        """
        if not self.connected:
            self.connect()

        try:
            self.rpc.update(**data)
            return True
        except Exception as e:
            print(f"Failed to update Discord presence: {e}")
            self.connected = False
            return False

    def update_song_status(self, song_info, config):
        """
        Update Discord Rich Presence with song information
        """
        if not self.connected:
            self.connect()

        try:
            if not song_info:
                # No active song, set idle status
                self.rpc.update(
                    state="Idle",
                    details="looking for a song to play",
                    large_image="game_synthriders_logo",
                    large_text="Synth Riders",
                    start=self.start_time
                )
            else:
                # Format song information for Discord
                song_name = song_info.get("song_name", "Unknown")
                artist = song_info.get("artist", "Unknown")
                difficulty = song_info.get("difficulty", "Unknown")
                mapper = song_info.get("mapper", "Unknown")
                cover_url = song_info.get("cover_url")
                bpm = song_info.get("bpm") or "Unknown"
                year = song_info.get("year", "")

                # Get song duration and start time for progress bar
                duration = song_info.get("duration")  # Duration in seconds
                song_start_time = song_info.get("start_time")  # When the song started

                # Build the update data
                update_data = {
                    "details": f"{song_name} by {artist}",
                    "state": f"{difficulty} | {bpm} BPM | mapped by {mapper})",
                }

                # Add progress bar if we have song duration
                if duration and song_start_time:
                    # Use song start time for the progress bar
                    update_data["start"] = song_start_time
                    update_data["end"] = song_start_time + duration
                else:
                    # Fall back to just showing start time
                    update_data["start"] = self.start_time

                # Use the uploaded cover URL if available, otherwise use default logo
                if cover_url:
                    update_data["large_image"] = cover_url
                    update_data["large_text"] = f"{song_name} by {artist}"
                    # Add small logo as game icon
                    update_data["small_image"] = "game_synthriders_logo"
                    update_data["small_text"] = "Synth Riders"
                else:
                    update_data["large_image"] = "game_synthriders_logo"
                    update_data["large_text"] = "Synth Riders"

                # Add button if configured
                if config.get("show_button", True):
                    button_label = config.get("button_label", "Synth Riders")
                    button_url = config.get("button_url", "https://synthridersvr.com")
                    update_data["buttons"] = [{
                        "label": button_label,
                        "url": button_url
                    }]

                self.rpc.update(**update_data)
            return True
        except Exception as e:
            print(f"Failed to update Discord presence: {e}")
            self.connected = False
            return False

