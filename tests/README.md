# Synth Riders Discord RPC - Smoke Tests

This directory contains comprehensive smoke tests for the Synth Riders Discord RPC tool. These tests validate the core functionality and ensure the tool works correctly under various conditions.

## Overview

The smoke tests cover the following major components:

### 1. SongStatusWatcher Tests
- **Purpose**: Tests the song status file monitoring and parsing functionality
- **Key Features Tested**:
  - File change detection
  - Song information parsing (artist, song name, difficulty, mapper)
  - Cover image handling
  - Database integration
  - Error handling for malformed files

### 2. SynthDB Tests
- **Purpose**: Tests the SQLite database query functionality
- **Key Features Tested**:
  - Database connection and queries
  - Song metadata retrieval (BPM, duration, mapper)
  - Error handling for missing databases/songs
  - Data mapping and validation

### 3. Discord Presence Tests
- **Purpose**: Tests the Discord Rich Presence integration
- **Key Features Tested**:
  - Discord connection management
  - Presence status updates (idle vs. playing)
  - Song information display
  - Error handling for connection failures
  - Button configuration

### 4. Integration Tests
- **Purpose**: Tests the complete workflow from file monitoring to Discord updates
- **Key Features Tested**:
  - End-to-end song status processing
  - File monitoring workflow
  - Complete data flow validation

### 5. Error Handling Tests
- **Purpose**: Tests robustness and error recovery
- **Key Features Tested**:
  - Malformed file handling
  - Network connection failures
  - Missing file/database scenarios
  - Graceful degradation

## Test Data

The tests use sample data from the `testdata/` directory:

### SongStatus Test Data
- `demosong-1/`: Contains "Berzerk by Eminem" song data
- `demosong-2/`: Contains "Eden by Au5 & Danyka Nadeau" song data
- Each directory includes:
  - `SongStatusOutput.txt`: Song status information
  - `SongStatusImage.png`: Cover image file

### SynthDB Test Data
- `SynthDB`: SQLite database with sample song metadata
- Contains test songs with BPM, duration, mapper information

## Running the Tests

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt
```

### Running All Tests
```bash
# From the project root
python tests/run_smoke_tests.py

# Or directly
python tests/test_smoke.py
```

### Running Specific Test Classes
```bash
# Test only song status functionality
python -m unittest tests.test_smoke.TestSongStatusWatcher

# Test only Discord presence
python -m unittest tests.test_smoke.TestDiscordPresence

# Test only database functionality
python -m unittest tests.test_smoke.TestSynthDB
```

### Running Individual Tests
```bash
# Test specific functionality
python -m unittest tests.test_smoke.TestSongStatusWatcher.test_parse_song_status_valid_content
```

## Test Configuration

The tests use a test configuration file (`test_config.json`) that points to the test data:

```json
{
  "discord_application_id": "test_client_id",
  "song_status_path": "./tests/testdata/SongStatus/demosong-1/SongStatusOutput.txt",
  "cover_image_path": "./tests/testdata/SongStatus/demosong-1/SongStatusImage.png",
  "synth_db_path": "./tests/testdata/SynthDB/SynthDB"
}
```

## Test Coverage

### Core Functionality
- ✅ Song status file monitoring
- ✅ Song information parsing
- ✅ Database queries and metadata retrieval
- ✅ Discord Rich Presence updates
- ✅ Image upload functionality
- ✅ Error handling and recovery

### Edge Cases
- ✅ Empty or malformed files
- ✅ Missing databases
- ✅ Network connection failures
- ✅ File permission issues
- ✅ Invalid song data

### Integration Scenarios
- ✅ Complete workflow from file change to Discord update
- ✅ Multiple song changes
- ✅ Idle state handling
- ✅ Configuration changes

## Expected Test Results

When all tests pass, you should see output like:

```
Running Synth Riders Discord RPC Smoke Tests...
==================================================
test_check_for_updates_file_exists (__main__.TestSongStatusWatcher) ... ok
test_check_for_updates_no_file (__main__.TestSongStatusWatcher) ... ok
test_get_song_status_no_updates (__main__.TestSongStatusWatcher) ... ok
test_get_song_status_with_updates (__main__.TestSongStatusWatcher) ... ok
test_parse_song_status_empty_file (__main__.TestSongStatusWatcher) ... ok
test_parse_song_status_valid_content (__main__.TestSongStatusWatcher) ... ok
test_parse_song_status_with_db_lookup (__main__.TestSongStatusWatcher) ... ok
test_song_status_watcher_initialization (__main__.TestSongStatusWatcher) ... ok
...

==================================================
Tests run: 25
Failures: 0
Errors: 0
✅ All smoke tests passed!
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure you're running from the project root
   - Check that all dependencies are installed
   - Verify Python path includes the project directory

2. **Database Errors**
   - Ensure test data files exist in `testdata/` directory
   - Check file permissions for test directories
   - Verify SQLite is available

3. **Mock Errors**
   - Tests use mocking for external dependencies
   - Ensure mock patches are correctly applied
   - Check that mocked objects have expected methods

### Debug Mode

To run tests with more verbose output:

```bash
python -m unittest tests.test_smoke -v
```

## Adding New Tests

When adding new functionality, follow these guidelines:

1. **Test Structure**: Use the existing test class structure
2. **Mocking**: Mock external dependencies (Discord, file system, network)
3. **Isolation**: Each test should be independent
4. **Cleanup**: Use `setUp()` and `tearDown()` for test isolation
5. **Documentation**: Add clear docstrings explaining test purpose

### Example Test Template

```python
def test_new_functionality(self):
    """Test description of what this test validates"""
    # Arrange
    test_data = "test input"
    
    # Act
    with patch('module.external_dependency') as mock_dep:
        mock_dep.return_value = "mocked result"
        result = function_under_test(test_data)
    
    # Assert
    self.assertEqual(result, "expected output")
    mock_dep.assert_called_once_with(test_data)
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

- **Fast Execution**: Tests complete in under 30 seconds
- **No External Dependencies**: All external services are mocked
- **Deterministic**: Tests produce consistent results
- **Isolated**: Tests don't interfere with each other

## Performance Considerations

- Tests use temporary directories that are cleaned up automatically
- Database operations are isolated to test databases
- File operations use temporary files
- Network calls are mocked to avoid external dependencies 