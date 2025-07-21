# Test script for Config Merger
# Demonstrates how the config merger works during updates

Write-Host "Synth Riders Discord RPC - Config Merger Test"
Write-Host "=" * 50

# Create test directories
$testDir = "test_config_merger"
if (Test-Path $testDir) {
    Remove-Item $testDir -Recurse -Force
}
New-Item -ItemType Directory -Path $testDir | Out-Null

# Create default config (new version)
$defaultConfig = @{
    "discord_application_id" = "1124356298578870333"
    "image_upload_url" = "https://uguu.se/upload"
    "promote_preference" = $true
    "song_status_path" = "C:\Program Files (x86)\Steam\steamapps\common\SynthRiders\SynthRidersUC\SongStatusOutput.txt"
    "cover_image_path" = "C:\Program Files (x86)\Steam\steamapps\common\SynthRiders\SynthRidersUC\SongStatusImage.png"
    "synth_db_path" = "C:\Program Files (x86)\Steam\steamapps\common\SynthRiders\SynthDB"
    "show_button" = $true
    "button_label" = "Play Synth Riders"
    "button_url" = "https://synthridersvr.com"
    "new_setting" = "This is a new setting added in v2.1.0"
    "another_new_setting" = $false
}

$defaultConfigPath = "$testDir\default_config.json"
$defaultConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath $defaultConfigPath -Encoding UTF8

# Create existing config (user's modified version)
$existingConfig = @{
    "discord_application_id" = "1124356298578870333"
    "image_upload_url" = "https://uguu.se/upload"
    "promote_preference" = $false  # User changed this
    "song_status_path" = "D:\Games\SynthRiders\SynthRidersUC\SongStatusOutput.txt"  # User changed path
    "cover_image_path" = "D:\Games\SynthRiders\SynthRidersUC\SongStatusImage.png"  # User changed path
    "synth_db_path" = "D:\Games\SynthRiders\SynthDB"  # User changed path
    "show_button" = $true
    "button_label" = "My Custom Button"  # User changed this
    "button_url" = "https://synthridersvr.com"
    "deprecated_setting" = "This setting is no longer used"  # Old setting
}

$existingConfigPath = "$testDir\existing_config.json"
$existingConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath $existingConfigPath -Encoding UTF8

Write-Host "`nTest Scenario:"
Write-Host "- Default config has new settings: 'new_setting', 'another_new_setting'"
Write-Host "- Existing config has user changes and deprecated setting"
Write-Host "- Expected: User changes preserved, new settings added, deprecated setting kept"

Write-Host "`nDefault Config (v2.1.0):"
Get-Content $defaultConfigPath | Write-Host

Write-Host "`nExisting Config (User's v2.0.0):"
Get-Content $existingConfigPath | Write-Host

# Run the config merger
Write-Host "`nRunning config merger..."
& ".\config_merger.ps1" -DefaultConfigPath $defaultConfigPath -TargetConfigPath $existingConfigPath

Write-Host "`nResult (Merged Config):"
Get-Content $existingConfigPath | Write-Host

# Verify the result
$mergedConfig = Get-Content $existingConfigPath -Raw | ConvertFrom-Json

Write-Host "`nVerification:"
Write-Host "- User changes preserved:"
Write-Host "  * promote_preference: $($mergedConfig.promote_preference) (should be false)"
Write-Host "  * song_status_path: $($mergedConfig.song_status_path) (should be user's path)"
Write-Host "  * button_label: $($mergedConfig.button_label) (should be 'My Custom Button')"

Write-Host "`n- New settings added:"
Write-Host "  * new_setting: $($mergedConfig.new_setting) (should be 'This is a new setting added in v2.1.0')"
Write-Host "  * another_new_setting: $($mergedConfig.another_new_setting) (should be false)"

Write-Host "`n- Deprecated setting preserved:"
Write-Host "  * deprecated_setting: $($mergedConfig.deprecated_setting) (should be preserved)"

# Clean up
Write-Host "`nCleaning up test files..."
Remove-Item $testDir -Recurse -Force

Write-Host "`nTest completed!" 