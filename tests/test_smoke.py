#!/usr/bin/env python3
"""
Smoke Tests for Synth Riders Discord RPC Tool

This test suite validates the core functionality of the Discord RPC tool
including song status parsing, database queries, Discord presence updates,
and file monitoring capabilities.
"""

import os
import sys
import tempfile
import shutil
import time
import json
import sqlite3
from unittest.mock import Mock, patch, MagicMock
import unittest

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from song_status import SongStatusWatcher
from discordrp import Presence
from utils.synth_db import get_song_details_from_synthdb


class TestSongStatusWatcher(unittest.TestCase):
    """Test the SongStatusWatcher class functionality"""
    
    def setUp(self):
        """Set up test environment with temporary files"""
        self.test_dir = tempfile.mkdtemp()
        self.song_status_path = os.path.join(self.test_dir, "SongStatusOutput.txt")
        self.cover_image_path = os.path.join(self.test_dir, "SongStatusImage.png")
        self.db_path = os.path.join(self.test_dir, "SynthDB")
        
        # Create test config
        self.config = {
            "song_status_path": self.song_status_path,
            "cover_image_path": self.cover_image_path,
            "synth_db_path": self.db_path,
            "image_upload_url": "https://uguu.se/upload"
        }
        
        # Create test SynthDB
        self.create_test_synthdb()
        
    def tearDown(self):
        """Clean up test files"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_test_synthdb(self):
        """Create a test SynthDB with sample data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create TracksCache table
        cursor.execute('''
            CREATE TABLE TracksCache (
                id INTEGER PRIMARY KEY,
                file_name TEXT,
                song_name TEXT,
                author TEXT,
                beatmapper TEXT,
                bpm INTEGER,
                image_file TEXT,
                notes_count TEXT,
                duration INTEGER,
                date_created INTEGER
            )
        ''')
        
        # Insert test data
        cursor.execute('''
            INSERT INTO TracksCache VALUES 
            (1, 'test-song.synth', 'Berzerk', 'Eminem', 'AudioTiZm', 140, 
             'test_image.png', '0,0,0,500,0,0', 180, 1234567890),
            (2, 'test-song2.synth', 'Eden', 'Au5 & Danyka Nadeau', 'OST', 128,
             'test_image2.png', '0,0,0,400,0,0', 200, 1234567891)
        ''')
        
        conn.commit()
        conn.close()
    
    def test_song_status_watcher_initialization(self):
        """Test SongStatusWatcher initializes correctly"""
        watcher = SongStatusWatcher(self.config)
        self.assertEqual(watcher.song_status_path, self.song_status_path)
        self.assertEqual(watcher.cover_image_path, self.cover_image_path)
        self.assertEqual(watcher.db_path, self.db_path)
        self.assertIsNone(watcher.current_song)
        self.assertEqual(watcher.last_modified, 0)
    
    def test_check_for_updates_no_file(self):
        """Test check_for_updates when file doesn't exist"""
        watcher = SongStatusWatcher(self.config)
        result = watcher.check_for_updates()
        self.assertFalse(result)
    
    def test_check_for_updates_file_exists(self):
        """Test check_for_updates when file exists"""
        # Create test file
        with open(self.song_status_path, 'w') as f:
            f.write("Test song by Test Artist\nMaster (mapped by TestMapper)")
        
        watcher = SongStatusWatcher(self.config)
        result = watcher.check_for_updates()
        self.assertTrue(result)  # Should detect new file
    
    def test_parse_song_status_empty_file(self):
        """Test parsing empty song status file"""
        # Create empty file
        with open(self.song_status_path, 'w') as f:
            pass
        
        watcher = SongStatusWatcher(self.config)
        result = watcher.parse_song_status()
        self.assertIsNone(result)
        self.assertIsNone(watcher.current_song)
    
    def test_parse_song_status_valid_content(self):
        """Test parsing valid song status content"""
        # Create test file with valid content
        with open(self.song_status_path, 'w') as f:
            f.write("Berzerk by Eminem\nMaster (mapped by AudioTiZm)")
        
        # Create test cover image
        with open(self.cover_image_path, 'wb') as f:
            f.write(b'fake image data')
        
        watcher = SongStatusWatcher(self.config)
        
        with patch.object(watcher, 'upload_image', return_value="https://example.com/image.png"):
            result = watcher.parse_song_status()
        
        self.assertIsNotNone(result)
        self.assertEqual(result['song_name'], 'Berzerk')
        self.assertEqual(result['artist'], 'Eminem')
        self.assertEqual(result['difficulty'], 'Master')
        self.assertEqual(result['mapper'], 'AudioTiZm')
        self.assertTrue(result['has_cover'])
        self.assertEqual(result['cover_url'], "https://example.com/image.png")
    
    def test_parse_song_status_with_db_lookup(self):
        """Test parsing song status with database lookup"""
        # Create test file
        with open(self.song_status_path, 'w') as f:
            f.write("Berzerk by Eminem\nMaster (mapped by AudioTiZm)")
        
        watcher = SongStatusWatcher(self.config)
        
        with patch.object(watcher, 'upload_image', return_value=None):
            result = watcher.parse_song_status()
        
        self.assertIsNotNone(result)
        # Should have database details
        self.assertEqual(result['bpm'], 140)
        self.assertEqual(result['duration'], 180)
        self.assertEqual(result['is_custom'], True)
    
    def test_get_song_status_no_updates(self):
        """Test get_song_status when no updates detected"""
        watcher = SongStatusWatcher(self.config)
        watcher.current_song = {"song_name": "Test Song"}
        
        result = watcher.get_song_status()
        self.assertEqual(result, watcher.current_song)
    
    def test_get_song_status_with_updates(self):
        """Test get_song_status when updates are detected"""
        # Create test file
        with open(self.song_status_path, 'w') as f:
            f.write("Eden by Au5 & Danyka Nadeau\nExpert (mapped by OST)")
        
        watcher = SongStatusWatcher(self.config)
        
        with patch.object(watcher, 'upload_image', return_value=None):
            result = watcher.get_song_status()
        
        self.assertIsNotNone(result)
        self.assertEqual(result['song_name'], 'Eden')
        self.assertEqual(result['artist'], 'Au5 & Danyka Nadeau')


class TestSynthDB(unittest.TestCase):
    """Test the SynthDB utility functions"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "SynthDB")
        self.create_test_synthdb()
    
    def tearDown(self):
        """Clean up test files"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_test_synthdb(self):
        """Create a test SynthDB"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE TracksCache (
                id INTEGER PRIMARY KEY,
                file_name TEXT,
                song_name TEXT,
                author TEXT,
                beatmapper TEXT,
                bpm INTEGER,
                image_file TEXT,
                notes_count TEXT,
                duration INTEGER,
                date_created INTEGER
            )
        ''')
        
        # Insert test data
        cursor.execute('''
            INSERT INTO TracksCache VALUES 
            (1, 'test-song.synth', 'Berzerk', 'Eminem', 'AudioTiZm', 140, 
             'test_image.png', '0,0,0,500,0,0', 180, 1234567890),
            (2, 'test-song2.synth', 'Eden', 'Au5 & Danyka Nadeau', 'OST', 128,
             'test_image2.png', '0,0,0,400,0,0', 200, 1234567891)
        ''')
        
        conn.commit()
        conn.close()
    
    def test_get_song_details_existing_song(self):
        """Test getting song details for existing song"""
        result = get_song_details_from_synthdb(self.db_path, "Berzerk", "Eminem")
        
        self.assertIsNotNone(result)
        self.assertEqual(result['title'], 'Berzerk')
        self.assertEqual(result['author'], 'Eminem')
        self.assertEqual(result['mapper'], 'AudioTiZm')
        self.assertEqual(result['bpm'], 140)
        self.assertEqual(result['duration'], 180)
    
    def test_get_song_details_nonexistent_song(self):
        """Test getting song details for non-existent song"""
        result = get_song_details_from_synthdb(self.db_path, "Nonexistent", "Artist")
        self.assertIsNone(result)
    
    def test_get_song_details_nonexistent_db(self):
        """Test getting song details when database doesn't exist"""
        result = get_song_details_from_synthdb("/nonexistent/path", "Song", "Artist")
        self.assertIsNone(result)


class TestDiscordPresence(unittest.TestCase):
    """Test the Discord Presence functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.client_id = "test_client_id"
    
    def test_presence_initialization(self):
        """Test Presence class initialization"""
        with patch('discordrp.PyPresence') as mock_pypresence:
            presence = Presence(self.client_id)
            
            self.assertEqual(presence.client_id, self.client_id)
            self.assertFalse(presence.connected)
            self.assertIsInstance(presence.start_time, int)
    
    def test_presence_connect_success(self):
        """Test successful connection to Discord"""
        with patch('discordrp.PyPresence') as mock_pypresence:
            mock_rpc = Mock()
            mock_pypresence.return_value = mock_rpc
            
            presence = Presence(self.client_id)
            result = presence.connect()
            
            self.assertTrue(result)
            self.assertTrue(presence.connected)
            mock_rpc.connect.assert_called_once()
    
    def test_presence_connect_failure(self):
        """Test failed connection to Discord"""
        with patch('discordrp.PyPresence') as mock_pypresence:
            mock_rpc = Mock()
            mock_rpc.connect.side_effect = Exception("Connection failed")
            mock_pypresence.return_value = mock_rpc
            
            presence = Presence(self.client_id)
            result = presence.connect()
            
            self.assertFalse(result)
            self.assertFalse(presence.connected)
    
    def test_presence_disconnect(self):
        """Test disconnection from Discord"""
        with patch('discordrp.PyPresence') as mock_pypresence:
            mock_rpc = Mock()
            mock_pypresence.return_value = mock_rpc
            
            presence = Presence(self.client_id)
            presence.connected = True
            presence.disconnect()
            
            self.assertFalse(presence.connected)
            mock_rpc.close.assert_called_once()
    
    def test_update_song_status_idle(self):
        """Test updating Discord presence with idle status"""
        with patch('discordrp.PyPresence') as mock_pypresence:
            mock_rpc = Mock()
            mock_pypresence.return_value = mock_rpc
            
            presence = Presence(self.client_id)
            presence.connected = True
            
            config = {"show_button": True}
            result = presence.update_song_status(None, config)
            
            self.assertTrue(result)
            mock_rpc.update.assert_called_once()
            call_args = mock_rpc.update.call_args[1]
            self.assertEqual(call_args['state'], "Idle")
            self.assertEqual(call_args['details'], "looking for a song to play")
    
    def test_update_song_status_with_song(self):
        """Test updating Discord presence with song information"""
        with patch('discordrp.PyPresence') as mock_pypresence:
            mock_rpc = Mock()
            mock_pypresence.return_value = mock_rpc
            
            presence = Presence(self.client_id)
            presence.connected = True
            
            song_info = {
                'song_name': 'Test Song',
                'artist': 'Test Artist',
                'difficulty': 'Master',
                'mapper': 'TestMapper',
                'bpm': 140,
                'cover_url': 'https://example.com/image.png',
                'start_time': 1234567890
            }
            
            config = {"show_button": True, "button_label": "Test", "button_url": "https://test.com"}
            result = presence.update_song_status(song_info, config)
            
            self.assertTrue(result)
            mock_rpc.update.assert_called_once()
            call_args = mock_rpc.update.call_args[1]
            self.assertIn('Test Song by Test Artist', call_args['details'])
            self.assertIn('Master', call_args['state'])


class TestIntegrationSmoke(unittest.TestCase):
    """Integration smoke tests for the complete workflow"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.song_status_path = os.path.join(self.test_dir, "SongStatusOutput.txt")
        self.cover_image_path = os.path.join(self.test_dir, "SongStatusImage.png")
        self.db_path = os.path.join(self.test_dir, "SynthDB")
        
        # Create test SynthDB
        self.create_test_synthdb()
        
        # Create test config
        self.config = {
            "discord_application_id": "test_client_id",
            "song_status_path": self.song_status_path,
            "cover_image_path": self.cover_image_path,
            "synth_db_path": self.db_path,
            "show_button": True,
            "button_label": "Test",
            "button_url": "https://test.com"
        }
    
    def tearDown(self):
        """Clean up test files"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_test_synthdb(self):
        """Create a test SynthDB"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE TracksCache (
                id INTEGER PRIMARY KEY,
                file_name TEXT,
                song_name TEXT,
                author TEXT,
                beatmapper TEXT,
                bpm INTEGER,
                image_file TEXT,
                notes_count TEXT,
                duration INTEGER,
                date_created INTEGER
            )
        ''')
        
        cursor.execute('''
            INSERT INTO TracksCache VALUES 
            (1, 'test-song.synth', 'Berzerk', 'Eminem', 'AudioTiZm', 140, 
             'test_image.png', '0,0,0,500,0,0', 180, 1234567890)
        ''')
        
        conn.commit()
        conn.close()
    
    def test_complete_workflow_smoke(self):
        """Test the complete workflow from song status to Discord presence"""
        # Create test song status file
        with open(self.song_status_path, 'w') as f:
            f.write("Berzerk by Eminem\nMaster (mapped by AudioTiZm)")
        
        # Create test cover image
        with open(self.cover_image_path, 'wb') as f:
            f.write(b'fake image data')
        
        # Test song status watcher
        with patch('song_status.SongStatusWatcher.upload_image', return_value="https://example.com/image.png"):
            watcher = SongStatusWatcher(self.config)
            song_info = watcher.get_song_status()
        
        self.assertIsNotNone(song_info)
        self.assertEqual(song_info['song_name'], 'Berzerk')
        self.assertEqual(song_info['artist'], 'Eminem')
        self.assertEqual(song_info['bpm'], 140)
        self.assertEqual(song_info['duration'], 180)
        
        # Test Discord presence update
        with patch('discordrp.PyPresence') as mock_pypresence:
            mock_rpc = Mock()
            mock_pypresence.return_value = mock_rpc
            
            presence = Presence(self.config['discord_application_id'])
            result = presence.update_song_status(song_info, self.config)
        
        self.assertTrue(result)
        mock_rpc.update.assert_called_once()
    
    def test_file_monitoring_smoke(self):
        """Test file monitoring functionality"""
        watcher = SongStatusWatcher(self.config)
        
        # Initially no file
        self.assertFalse(watcher.check_for_updates())
        
        # Create file
        with open(self.song_status_path, 'w') as f:
            f.write("Test song by Test artist")
        
        # Should detect update
        self.assertTrue(watcher.check_for_updates())
        
        # No change (file already exists, no modification)
        self.assertFalse(watcher.check_for_updates())
        
        # Wait a bit and modify file
        import time
        time.sleep(0.1)  # Small delay to ensure file modification time changes
        
        with open(self.song_status_path, 'w') as f:
            f.write("Different song by Different artist")
        
        # Should detect update
        self.assertTrue(watcher.check_for_updates())


class TestErrorHandlingSmoke(unittest.TestCase):
    """Test error handling and edge cases"""
    
    def test_song_status_watcher_malformed_file(self):
        """Test handling of malformed song status file"""
        test_dir = tempfile.mkdtemp()
        song_status_path = os.path.join(test_dir, "SongStatusOutput.txt")
        
        config = {
            "song_status_path": song_status_path,
            "cover_image_path": os.path.join(test_dir, "SongStatusImage.png"),
            "synth_db_path": os.path.join(test_dir, "SynthDB")
        }
        
        # Create malformed file
        with open(song_status_path, 'w') as f:
            f.write("Malformed content without proper format")
        
        watcher = SongStatusWatcher(config)
        
        with patch.object(watcher, 'upload_image', return_value=None):
            result = watcher.parse_song_status()
        
        # Should handle gracefully - the parser should still return a result even for malformed content
        self.assertIsNotNone(result)
        self.assertEqual(result['song_name'], 'Malformed content without proper format')
        self.assertEqual(result['artist'], 'Unknown')
        self.assertEqual(result['difficulty'], 'Unknown')
        self.assertEqual(result['mapper'], 'Unknown')
        
        shutil.rmtree(test_dir)
    
    def test_discord_presence_connection_failure(self):
        """Test Discord presence with connection failure"""
        with patch('discordrp.PyPresence') as mock_pypresence:
            mock_rpc = Mock()
            mock_rpc.connect.side_effect = Exception("Connection failed")
            mock_rpc.update.side_effect = Exception("Update failed")
            mock_pypresence.return_value = mock_rpc
            
            presence = Presence("test_client_id")
            
            # Should handle connection failure gracefully
            result = presence.connect()
            self.assertFalse(result)
            
            # Should handle update failure gracefully
            result = presence.update_song_status({"song_name": "Test"}, {})
            self.assertFalse(result)
    
    def test_synthdb_nonexistent_database(self):
        """Test SynthDB query with non-existent database"""
        result = get_song_details_from_synthdb("/nonexistent/path", "Song", "Artist")
        self.assertIsNone(result)


def run_smoke_tests():
    """Run all smoke tests"""
    print("Running Synth Riders Discord RPC Smoke Tests...")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestSongStatusWatcher,
        TestSynthDB,
        TestDiscordPresence,
        TestIntegrationSmoke,
        TestErrorHandlingSmoke
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ All smoke tests passed!")
        return True
    else:
        print("❌ Some smoke tests failed!")
        return False


if __name__ == "__main__":
    success = run_smoke_tests()
    sys.exit(0 if success else 1) 