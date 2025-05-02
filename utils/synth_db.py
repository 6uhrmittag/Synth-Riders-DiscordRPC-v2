import os
import sqlite3

def get_song_details_from_synthdb(db_path, song_name, artist):
    """
    Query SynthDB to get all available song details based on song name and artist

    Args:
        db_path (str): Path to the SynthDB folder
        song_name (str): Name of the song to look up
        artist (str): Artist name of the song

    Returns:
        dict: A dictionary containing song details or None if not found
    """
    try:
        if not os.path.exists(db_path):
            print(f"SynthDB path does not exist: {db_path}")
            return None

        # Connect to SynthDB SQLite database
        conn = sqlite3.connect(os.path.join(db_path, "SynthDB.sqlite"))
        conn.row_factory = sqlite3.Row  # This enables name-based access to columns
        cursor = conn.cursor()

        # Query for the song with more detailed information
        query = """
        SELECT
            s.id, s.title, s.author, s.bpm, s.duration, s.difficulty,
            s.year, s.mapper, s.songSubName, s.environment,
            s.isCustom, s.path
        FROM song s
        WHERE s.title LIKE ? AND s.author LIKE ?
        """

        # Use wildcards for partial matching
        cursor.execute(query, (f"%{song_name}%", f"%{artist}%"))
        result = cursor.fetchone()

        if not result:
            print(f"Song '{song_name}' by '{artist}' not found in SynthDB")
            return None

        # Convert row to dictionary
        song_details = {
            'id': result['id'],
            'title': result['title'],
            'author': result['author'],
            'bpm': result['bpm'],
            'duration': result['duration'],  # Duration in seconds
            'difficulty': result['difficulty'],
            'year': result['year'],
            'mapper': result['mapper'],
            'song_sub_name': result['songSubName'],
            'environment': result['environment'],
            'is_custom': bool(result['isCustom']),
            'path': result['path']
        }

        conn.close()
        return song_details

    except Exception as e:
        print(f"Error querying SynthDB for song details: {e}")
        return None
