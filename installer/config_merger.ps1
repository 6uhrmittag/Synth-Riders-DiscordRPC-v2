# Config Merger for Synth Riders Discord RPC
# PowerShell script to intelligently merge config files during updates

param(
    [string]$DefaultConfigPath,
    [string]$TargetConfigPath
)

function Load-JsonFile {
    param([string]$FilePath)
    
    try {
        if (Test-Path $FilePath) {
            $content = Get-Content $FilePath -Raw -Encoding UTF8
            return $content | ConvertFrom-Json
        }
        return $null
    }
    catch {
        Write-Host "Warning: Could not load $FilePath - $($_.Exception.Message)"
        return $null
    }
}

function Save-JsonFile {
    param([string]$FilePath, [object]$Data)
    
    try {
        $json = $Data | ConvertTo-Json -Depth 10 -Compress:$false
        $json | Out-File -FilePath $FilePath -Encoding UTF8
        return $true
    }
    catch {
        Write-Host "Error: Could not save $FilePath - $($_.Exception.Message)"
        return $false
    }
}

function Backup-ConfigFile {
    param([string]$ConfigPath)
    
    if (Test-Path $ConfigPath) {
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $backupPath = "$ConfigPath.backup_$timestamp"
        
        try {
            Copy-Item $ConfigPath $backupPath
            Write-Host "Created backup: $backupPath"
            return $backupPath
        }
        catch {
            Write-Host "Warning: Could not create backup - $($_.Exception.Message)"
            return $null
        }
    }
    return $null
}

function Merge-Configs {
    param([object]$DefaultConfig, [object]$ExistingConfig)
    
    if (-not $ExistingConfig) {
        Write-Host "No existing config found, using default config"
        return $DefaultConfig
    }
    
    if (-not $DefaultConfig) {
        Write-Host "No default config found, keeping existing config"
        return $ExistingConfig
    }
    
    $mergedConfig = $ExistingConfig | ConvertTo-Json -Depth 10 | ConvertFrom-Json
    $changesMade = $false
    
    # Add new settings from default config
    $defaultProps = $DefaultConfig | Get-Member -MemberType NoteProperty | Select-Object -ExpandProperty Name
    $existingProps = $ExistingConfig | Get-Member -MemberType NoteProperty | Select-Object -ExpandProperty Name
    
    foreach ($prop in $defaultProps) {
        if ($prop -notin $existingProps) {
            Write-Host "Adding new setting: $prop = $($DefaultConfig.$prop)"
            $mergedConfig | Add-Member -MemberType NoteProperty -Name $prop -Value $DefaultConfig.$prop -Force
            $changesMade = $true
        }
    }
    
    # Check for deprecated settings
    $deprecatedKeys = @()
    foreach ($prop in $existingProps) {
        if ($prop -notin $defaultProps) {
            $deprecatedKeys += $prop
        }
    }
    
    if ($deprecatedKeys.Count -gt 0) {
        Write-Host "Warning: Found deprecated settings: $($deprecatedKeys -join ', ')"
        Write-Host "These settings will be preserved but may not be used by the application"
    }
    
    return $mergedConfig, $changesMade
}

# Main execution
Write-Host "Synth Riders Discord RPC - Config Merger"
Write-Host "=" * 50

# Load configs
Write-Host "Loading default config: $DefaultConfigPath"
$defaultConfig = Load-JsonFile $DefaultConfigPath

Write-Host "Loading existing config: $TargetConfigPath"
$existingConfig = Load-JsonFile $TargetConfigPath

# Check if this is an update
$isUpdate = $existingConfig -ne $null

if ($isUpdate) {
    Write-Host "`nUpdate detected - merging configurations..."
    
    # Create backup of existing config
    $backupPath = Backup-ConfigFile $TargetConfigPath
    
    # Merge configs
    $mergedConfig, $changesMade = Merge-Configs $defaultConfig $existingConfig
    
    if ($changesMade) {
        Write-Host "`nChanges made to config:"
        $defaultProps = $defaultConfig | Get-Member -MemberType NoteProperty | Select-Object -ExpandProperty Name
        $existingProps = $existingConfig | Get-Member -MemberType NoteProperty | Select-Object -ExpandProperty Name
        $newSettings = ($defaultProps | Where-Object { $_ -notin $existingProps }).Count
        Write-Host "- New settings added: $newSettings"
        Write-Host "- Total settings: $($mergedConfig | Get-Member -MemberType NoteProperty).Count"
        
        # Save merged config
        if (Save-JsonFile $TargetConfigPath $mergedConfig) {
            Write-Host "`n✅ Successfully updated config: $TargetConfigPath"
            if ($backupPath) {
                Write-Host "📁 Backup created: $backupPath"
            }
        }
        else {
            Write-Host "`n❌ Failed to save updated config"
            exit 1
        }
    }
    else {
        Write-Host "`n✅ No changes needed - existing config is up to date"
    }
}
else {
    Write-Host "`nFresh installation - using default config"
    if ($defaultConfig -and (Save-JsonFile $TargetConfigPath $defaultConfig)) {
        Write-Host "✅ Created new config: $TargetConfigPath"
    }
    else {
        Write-Host "❌ Failed to create config"
        exit 1
    }
}

Write-Host "`nConfig merger completed successfully!" 