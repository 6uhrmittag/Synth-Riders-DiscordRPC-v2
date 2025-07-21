#!/usr/bin/env python3
"""
Config Merger for Synth Riders Discord RPC
Intelligently merges new default config with existing user config
"""

import json
import os
import sys
import shutil
from datetime import datetime

def load_json_file(file_path):
    """Load JSON file with error handling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
        print(f"Warning: Could not load {file_path}: {e}")
        return None

def save_json_file(file_path, data):
    """Save JSON file with error handling"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error: Could not save {file_path}: {e}")
        return False

def merge_configs(default_config, existing_config):
    """
    Intelligently merge default config with existing user config
    Preserves user changes while adding new settings
    """
    if not existing_config:
        print("No existing config found, using default config")
        return default_config
    
    if not default_config:
        print("No default config found, keeping existing config")
        return existing_config
    
    merged_config = existing_config.copy()
    changes_made = False
    
    # Add new settings from default config
    for key, value in default_config.items():
        if key not in merged_config:
            print(f"Adding new setting: {key} = {value}")
            merged_config[key] = value
            changes_made = True
    
    # Check for deprecated settings in existing config
    deprecated_keys = []
    for key in merged_config.keys():
        if key not in default_config:
            deprecated_keys.append(key)
    
    if deprecated_keys:
        print(f"Warning: Found deprecated settings: {', '.join(deprecated_keys)}")
        print("These settings will be preserved but may not be used by the application")
    
    return merged_config, changes_made

def backup_config(config_path):
    """Create a backup of the existing config file"""
    if not os.path.exists(config_path):
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{config_path}.backup_{timestamp}"
    
    try:
        shutil.copy2(config_path, backup_path)
        print(f"Created backup: {backup_path}")
        return backup_path
    except IOError as e:
        print(f"Warning: Could not create backup: {e}")
        return None

def main():
    """Main function to merge config files"""
    if len(sys.argv) != 3:
        print("Usage: config_merger.py <default_config_path> <target_config_path>")
        sys.exit(1)
    
    default_config_path = sys.argv[1]
    target_config_path = sys.argv[2]
    
    print("Synth Riders Discord RPC - Config Merger")
    print("=" * 50)
    
    # Load configs
    print(f"Loading default config: {default_config_path}")
    default_config = load_json_file(default_config_path)
    
    print(f"Loading existing config: {target_config_path}")
    existing_config = load_json_file(target_config_path)
    
    # Check if this is an update (existing config exists)
    is_update = existing_config is not None
    
    if is_update:
        print("\nUpdate detected - merging configurations...")
        
        # Create backup of existing config
        backup_path = backup_config(target_config_path)
        
        # Merge configs
        merged_config, changes_made = merge_configs(default_config, existing_config)
        
        if changes_made:
            print(f"\nChanges made to config:")
            print(f"- New settings added: {len(default_config) - len(existing_config)}")
            print(f"- Total settings: {len(merged_config)}")
            
            # Save merged config
            if save_json_file(target_config_path, merged_config):
                print(f"\n✅ Successfully updated config: {target_config_path}")
                if backup_path:
                    print(f"📁 Backup created: {backup_path}")
            else:
                print(f"\n❌ Failed to save updated config")
                sys.exit(1)
        else:
            print("\n✅ No changes needed - existing config is up to date")
            
    else:
        print("\nFresh installation - using default config")
        if default_config and save_json_file(target_config_path, default_config):
            print(f"✅ Created new config: {target_config_path}")
        else:
            print(f"❌ Failed to create config")
            sys.exit(1)
    
    print("\nConfig merger completed successfully!")

if __name__ == "__main__":
    main() 