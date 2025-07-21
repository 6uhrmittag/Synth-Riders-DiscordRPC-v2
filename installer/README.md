# Windows Installer for Synth Riders Discord RPC

This directory contains the Windows installer setup for the Synth Riders Discord RPC tool.

## Files

- `setup.nsi` - NSIS installer script
- `build_installer.bat` - Build script for the installer
- `README.md` - This documentation

## Prerequisites

### For Building the Installer

1. **NSIS (Nullsoft Scriptable Install System)**
   - Download from: https://nsis.sourceforge.io/
   - Install and add to PATH
   - Required for building the installer

2. **Built Application**
   - Run `build.bat` first to create the `dist` directory
   - Ensure `dist/main.exe` and `dist/settings/` exist

## Building the Installer

### Option 1: Using the Build Script
```batch
cd installer
build_installer.bat
```

### Option 2: Manual Build
```batch
makensis /DAPP_VERSION=2.0.0 setup.nsi
```

## Installer Features

### Professional Setup Wizard
- Welcome page with application information
- License agreement page
- Installation directory selection
- Progress indicator during installation
- Completion page with options

### Installation Components
- **Main Executable**: `main.exe`
- **Settings**: `appinfo.ini` and `config.json`
- **Assets**: All application assets
- **Utils**: Utility modules

### Smart Update Process
- **Configuration Preservation**: User changes in `config.json` are preserved during updates
- **New Settings**: New settings from the default config are automatically added
- **Deprecated Settings**: Old settings are preserved but marked as deprecated
- **Automatic Backup**: Existing config is backed up before merging
- **Update Detection**: Installer automatically detects if this is an update or fresh installation

### System Integration
- **Start Menu**: Creates shortcuts in Programs menu
- **Desktop Shortcut**: Easy access from desktop
- **Autorun**: Automatically starts with Windows
- **Registry**: Proper installation tracking
- **Uninstaller**: Clean removal from Control Panel

### Installation Directory
- Default: `C:\Program Files\Synth Riders Discord RPC\`
- User can change during installation
- Registry remembers previous location

## Installer Output

The installer creates:
```
SynthRidersDiscordRPC-Setup-v2.0.0.exe
```

## Installation Process

1. **Welcome Screen**
   - Application name and version
   - Brief description

2. **License Agreement**
   - Shows LICENSE file content
   - User must accept to continue

3. **Installation Directory**
   - Default: `C:\Program Files\Synth Riders Discord RPC\`
   - User can browse and change location

4. **Installation Progress**
   - Shows files being copied
   - Progress bar and status

5. **Completion**
   - Success message
   - Option to run application immediately
   - Option to view README

### Update Process

When updating an existing installation:

1. **Update Detection**
   - Installer detects existing installation
   - Shows "Update detected - preserving user configuration"

2. **Configuration Backup**
   - Creates timestamped backup of existing config
   - Format: `config.json.backup_YYYYMMDD_HHMMSS`

3. **Smart Configuration Merge**
   - Preserves all user customizations
   - Adds new settings from default config
   - Keeps deprecated settings (with warning)

4. **File Updates**
   - Updates executable and other files
   - Preserves user configuration
   - Maintains system integration

## Uninstallation

The installer creates a proper uninstaller that:
- Removes all installed files
- Removes start menu shortcuts
- Removes desktop shortcut
- Removes autorun entry
- Cleans registry entries
- Removes installation directory

## Registry Entries

### Installation Information
```
HKCU\Software\Synth Riders Discord RPC\
```

### Uninstall Information
```
HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\Synth Riders Discord RPC\
```

### Autorun Entry
```
HKCU\Software\Microsoft\Windows\CurrentVersion\Run\Synth Riders Discord RPC
```

## Troubleshooting

### Build Issues

**NSIS not found**
```
ERROR: NSIS (makensis) not found in PATH
```
**Solution**: Install NSIS and add to PATH

**Missing dist directory**
```
ERROR: main.exe not found in dist directory
```
**Solution**: Run `build.bat` first

**Missing settings**
```
ERROR: settings directory not found in dist
```
**Solution**: Ensure settings are copied during build

### Installation Issues

**Permission Denied**
- Run installer as Administrator
- Check antivirus software

**Missing Dependencies**
- Install Visual C++ Redistributable
- Check Windows version compatibility

## Customization

### Version Number
Edit `setup.nsi`:
```nsi
!define APP_VERSION "2.0.0"
```

### Application Name
```nsi
!define APP_NAME "Synth Riders Discord RPC"
```

### Publisher
```nsi
!define APP_PUBLISHER "Synth Riders Community"
```

### Icon
Replace `assets\logo.ico` with your custom icon

### License
Replace `LICENSE` file with your license

## Integration with CI/CD

The installer is automatically built in GitHub Actions when:
- NSIS is available on the runner
- Build artifacts are successfully created
- Release is being created

The installer is included in releases as:
```
SynthRidersDiscordRPC-Setup-v{version}.exe
```

## Best Practices

1. **Version Management**
   - Update version in `appinfo.ini`
   - Update version in `setup.nsi`
   - Use semantic versioning

2. **Testing**
   - Test installer on clean Windows VM
   - Test uninstallation process
   - Verify autorun functionality

3. **Distribution**
   - Include installer in GitHub releases
   - Provide both installer and portable versions
   - Document installation instructions

4. **Security**
   - Sign installer with code signing certificate
   - Verify file integrity
   - Scan for malware before distribution 