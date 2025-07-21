; Synth Riders Discord RPC Installer
; NSIS Script for Windows Setup Wizard

!define APP_NAME "Synth Riders Discord RPC"
!define APP_VERSION "2.0.0"
!define APP_PUBLISHER "Synth Riders Community"
!define APP_EXE "main.exe"
!define APP_ID "SynthRidersDiscordRPC"

; Include modern UI
!include "MUI2.nsh"
!include "FileFunc.nsh"

; Request application privileges
RequestExecutionLevel admin

; Set compression
SetCompressor /SOLID lzma

; Set version info
VIProductVersion "${APP_VERSION}.0"
VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductName" "${APP_NAME}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "CompanyName" "${APP_PUBLISHER}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalCopyright" "Copyright (c) 2024"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileDescription" "Synth Riders Discord RPC Tool"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileVersion" "${APP_VERSION}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductVersion" "${APP_VERSION}"

; Default installation directory
InstallDir "$PROGRAMFILES\${APP_NAME}"

; Get installation directory from registry if available
InstallDirRegKey HKCU "Software\${APP_NAME}" ""

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "assets\logo.ico"
!define MUI_UNICON "assets\logo.ico"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Language
!insertmacro MUI_LANGUAGE "English"

; Installer
Name "${APP_NAME}"
OutFile "SynthRidersDiscordRPC-Setup-v${APP_VERSION}.exe"

Section "Main Application" SecMain
    SectionIn RO
    
    ; Check if this is an update
    ${If} ${FileExists} "$INSTDIR\settings\config.json"
        StrCpy $R0 "update"
        DetailPrint "Update detected - preserving user configuration"
    ${Else}
        StrCpy $R0 "fresh"
        DetailPrint "Fresh installation detected"
    ${EndIf}
    
    ; Set output path to the installation directory
    SetOutPath $INSTDIR
    
    ; Copy main executable
    File "dist\main.exe"
    
    ; Copy settings directory with smart config handling
    SetOutPath "$INSTDIR\settings"
    File "dist\settings\appinfo.ini"
    
    ; Handle config.json based on installation type
    ${If} $R0 == "update"
        ; Copy config merger script
        File "dist\config_merger.ps1"
        
        ; Copy default config to temp location
        CopyFiles "dist\settings\config.json" "$TEMP\default_config.json"
        
        ; Run config merger using PowerShell
        DetailPrint "Merging configuration files..."
        ExecWait 'powershell.exe -ExecutionPolicy Bypass -File "$INSTDIR\settings\config_merger.ps1" -DefaultConfigPath "$TEMP\default_config.json" -TargetConfigPath "$INSTDIR\settings\config.json"'
        
        ; Clean up temp file
        Delete "$TEMP\default_config.json"
        
        ; Remove config merger script (not needed after installation)
        Delete "$INSTDIR\settings\config_merger.ps1"
    ${Else}
        ; Fresh installation - copy config directly
        File "dist\settings\config.json"
    ${EndIf}
    
    ; Copy assets directory
    SetOutPath "$INSTDIR\assets"
    File "dist\assets\*.*"
    
    ; Copy utils directory
    SetOutPath "$INSTDIR\utils"
    File "dist\utils\*.*"
    
    ; Write the installation path into the registry
    WriteRegStr HKCU "Software\${APP_NAME}" "" $INSTDIR
    
    ; Write the uninstall information to the registry
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayIcon" "$\"$INSTDIR\${APP_EXE}$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Create start menu shortcut
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
    
    ; Create desktop shortcut
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
    
    ; Create autorun entry
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "${APP_NAME}" "$\"$INSTDIR\${APP_EXE}$\""
    
SectionEnd

Section "Uninstall"
    ; Remove start menu shortcuts
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"
    
    ; Remove desktop shortcut
    Delete "$DESKTOP\${APP_NAME}.lnk"
    
    ; Remove autorun entry
    DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "${APP_NAME}"
    
    ; Remove files and uninstaller
    Delete "$INSTDIR\${APP_EXE}"
    Delete "$INSTDIR\settings\appinfo.ini"
    Delete "$INSTDIR\settings\config.json"
    Delete "$INSTDIR\assets\*.*"
    Delete "$INSTDIR\utils\*.*"
    Delete "$INSTDIR\Uninstall.exe"
    
    ; Remove directories
    RMDir "$INSTDIR\settings"
    RMDir "$INSTDIR\assets"
    RMDir "$INSTDIR\utils"
    RMDir "$INSTDIR"
    
    ; Remove registry keys
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
    DeleteRegKey HKCU "Software\${APP_NAME}"
    
SectionEnd 