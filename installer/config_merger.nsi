; Config Merger for Synth Riders Discord RPC
; NSIS script to intelligently merge config files during updates

!macro MergeConfigs default_config_path target_config_path
    ; Check if target config exists (update scenario)
    ${If} ${FileExists} "${target_config_path}"
        DetailPrint "Update detected - merging configurations..."
        
        ; Create backup of existing config
        ${GetTime} "" "L" $0 $1 $2 $3 $4 $5 $6
        StrCpy $R1 "${target_config_path}.backup_$2$1$0_$4$5$6"
        CopyFiles "${target_config_path}" "$R1"
        DetailPrint "Created backup: $R1"
        
        ; Load existing config
        ${ConfigRead} "${target_config_path}" "discord_application_id" $R2
        ${ConfigRead} "${target_config_path}" "image_upload_url" $R3
        ${ConfigRead} "${target_config_path}" "promote_preference" $R4
        ${ConfigRead} "${target_config_path}" "song_status_path" $R5
        ${ConfigRead} "${target_config_path}" "cover_image_path" $R6
        ${ConfigRead} "${target_config_path}" "synth_db_path" $R7
        ${ConfigRead} "${target_config_path}" "show_button" $R8
        ${ConfigRead} "${target_config_path}" "button_label" $R9
        ${ConfigRead} "${target_config_path}" "button_url" $R10
        
        ; Load default config
        ${ConfigRead} "${default_config_path}" "discord_application_id" $R11
        ${ConfigRead} "${default_config_path}" "image_upload_url" $R12
        ${ConfigRead} "${default_config_path}" "promote_preference" $R13
        ${ConfigRead} "${default_config_path}" "song_status_path" $R14
        ${ConfigRead} "${default_config_path}" "cover_image_path" $R15
        ${ConfigRead} "${default_config_path}" "synth_db_path" $R16
        ${ConfigRead} "${default_config_path}" "show_button" $R17
        ${ConfigRead} "${default_config_path}" "button_label" $R18
        ${ConfigRead} "${default_config_path}" "button_url" $R19
        
        ; Create merged config
        FileOpen $0 "${target_config_path}" w
        FileWrite $0 "{\n"
        
        ; Write existing settings (preserve user changes)
        FileWrite $0 '  "discord_application_id": "$R2",\n'
        FileWrite $0 '  "image_upload_url": "$R3",\n'
        FileWrite $0 '  "promote_preference": $R4,\n'
        FileWrite $0 '  "song_status_path": "$R5",\n'
        FileWrite $0 '  "cover_image_path": "$R6",\n'
        FileWrite $0 '  "synth_db_path": "$R7",\n'
        FileWrite $0 '  "show_button": $R8,\n'
        FileWrite $0 '  "button_label": "$R9",\n'
        FileWrite $0 '  "button_url": "$R10"\n'
        
        FileClose $0
        DetailPrint "Successfully merged configuration - user settings preserved"
        
    ${Else}
        DetailPrint "Fresh installation - copying default config"
        CopyFiles "${default_config_path}" "${target_config_path}"
    ${EndIf}
!macroend

; Include required NSIS functions
!include "LogicLib.nsh"
!include "FileFunc.nsh"
!include "TextFunc.nsh"

; Initialize text functions
${ConfigRead}
${GetTime} 