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
            
        # For debugging
        print(f"Querying SynthDB at {db_path} for song: '{song_name}' by '{artist}'")

        # Connect to SynthDB SQLite database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # This enables name-based access to columns
        cursor = conn.cursor()

        # Query for the song with more detailed information based on SynthDB schema
        query = """
        SELECT
            id, file_name, song_name, author, beatmapper, 
            bpm, image_file, notes_count, duration, date_created
        FROM TracksCache
        WHERE song_name LIKE ? AND author LIKE ?
        """
        
        # Use wildcards for partial matching
        cursor.execute(query, (f"%{song_name}%", f"%{artist}%"))
        result = cursor.fetchone()
        
        if not result:
            print(f"Song '{song_name}' by '{artist}' not found in SynthDB")
            return None
        
        # Convert row to dictionary with corrected field names
        song_details = {
            'id': result['id'],
            'file_name': result['file_name'],
            'title': result['song_name'],  # Map to expected name
            'author': result['author'],
            'mapper': result['beatmapper'],
            'bpm': result['bpm'],
            'image_file': result['image_file'],
            'notes_count': result['notes_count'],
            'duration': result['duration'],  # Duration in seconds
            'date_created': result['date_created'],
            # Set defaults for fields that aren't in the schema but used in the app
            'year': '',
            'environment': '',
            'is_custom': True  # Default to custom song
        }

        conn.close()
        return song_details

    except sqlite3.Error as e:
        print(f"SQLite error querying SynthDB: {e}")
        # Try to list available tables for debugging
        try:
            if conn and conn.cursor():
                tables_cursor = conn.cursor()
                tables_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = tables_cursor.fetchall()
                print(f"Available tables in database: {[t[0] for t in tables]}")
        except:
            pass
        return None
    except Exception as e:
        print(f"Error querying SynthDB for song details: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        if conn:
            conn.close()
