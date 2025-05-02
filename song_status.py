import os
import time
import re

class SongStatusWatcher:
    """
    Watches the SongStatusOutput.txt file for changes and parses song information
    """
    def __init__(self, config):
        self.config = config
        self.song_status_path = config.get("song_status_path",
                                         "C:\\Program Files (x86)\\Steam\\steamapps\\common\\SynthRiders\\SynthRidersUC\\SongStatusOutput.txt")
        self.cover_image_path = config.get("cover_image_path",
                                         "C:\\Program Files (x86)\\Steam\\steamapps\\common\\SynthRiders\\SynthRidersUC\\SongStatusImage.png")
        self.last_modified = 0
        self.current_song = None
        self.has_cover_image = False

    def check_for_updates(self):
        """
        Check if the song status file has been updated
        """
        try:
            if not os.path.exists(self.song_status_path):
                return False

            current_modified = os.path.getmtime(self.song_status_path)

            # Check if file has been modified
            if current_modified != self.last_modified:
                self.last_modified = current_modified
                return True

            return False
        except Exception as e:
            print(f"Error checking song status file: {e}")
            return False

    def parse_song_status(self):
        """
        Parse the song status file and extract information
        """
        try:
            if not os.path.exists(self.song_status_path):
                return None

            # Check if file is empty (no active song)
            if os.path.getsize(self.song_status_path) == 0:
                self.current_song = None
                self.has_cover_image = False
                return None

            with open(self.song_status_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()

            if not content:
                self.current_song = None
                self.has_cover_image = False
                return None

            # Parse song information from content
            lines = content.split('\n')

            # Basic parsing - extract song and artist from first line
            song_info = {}

            if lines and ' by ' in lines[0]:
                song_name, artist = lines[0].split(' by ', 1)
                song_info['song_name'] = song_name.strip()
                song_info['artist'] = artist.strip()
            else:
                song_info['song_name'] = lines[0].strip() if lines else "Unknown"
                song_info['artist'] = "Unknown"

            # Extract difficulty and mapper from second line
            if len(lines) > 1 and '(mapped by ' in lines[1]:
                difficulty, mapper_part = lines[1].split('(mapped by ', 1)
                song_info['difficulty'] = difficulty.strip()
                song_info['mapper'] = mapper_part.strip().rstrip(')')
            else:
                song_info['difficulty'] = lines[1].strip() if len(lines) > 1 else "Unknown"
                song_info['mapper'] = "Unknown"

            # Check if cover image exists
            self.has_cover_image = os.path.exists(self.cover_image_path) and os.path.getsize(self.cover_image_path) > 0
            song_info['has_cover'] = self.has_cover_image
            song_info['cover_path'] = self.cover_image_path if self.has_cover_image else None

            self.current_song = song_info
            return song_info

        except Exception as e:
            print(f"Error parsing song status: {e}")
            return None

    def get_song_status(self):
        """
        Check for updates and return the current song status
        """
        if self.check_for_updates():
            return self.parse_song_status()
        return self.current_song
