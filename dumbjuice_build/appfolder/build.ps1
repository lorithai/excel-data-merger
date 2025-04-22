# Configuration
$pythonVersion = "3.11.7"



$asciiText = @"
                                                                                                                
88888888ba,                                     88                   88               88                          
88      `"8b                                     88                   88               ""                          
88        `8b                                    88                   88                                           
88         88  88       88  88,dPYba,,adPYba,   88,dPPYba,           88  88       88  88   ,adPPYba,   ,adPPYba,  
88         88  88       88  88P'   "88"    "8a  88P'    "8a          88  88       88  88  a8"     ""  a8P_____88  
88         8P  88       88  88      88      88  88       d8          88  88       88  88  8b          8PP"  
88      .a8P   "8a,   ,a88  88      88      88  88b,   ,a8"  88,   ,d88  "8a,   ,a88  88  "8a,   ,aa  "8b,   ,aa  
 88888888Y"'     `"YbbdP'Y8  88      88      88  8Y"Ybbd8"'    "Y8888P"     `"YbbdP'Y8  88   `"Ybbd8"'    `"Ybbd8"'  
                                                                                                                     
"@
$asciiLogo = @"                                                                              
                                                        #######.           
                                                      ##*:::::::###         
                                                    ##*::%#:-###-%##        
                                                   ##:::=####::-:##         
                                                  ##::###=-*##%-%#*         
                                                  #####--:::-==##           
                                            *##########*==-=*###            
                                        %###+...........######=:=###        
                                     =%##......::..-::......::::::##+       
                                   *##.........::..:::::::::::::::%%*       
                                  ##....::::::::::::::::::::::::::%%        
                                *##......:::::::::==+:::::::::::-%#         
                               %#+......:::::==-::::::::::::::::--##        
                              =#+...:::::=+::::==:::::::::::::::=--#%       
                              ##.....:::::==:::::.-:::::::::::::---%#       
                             =#=....::::::::::::::=-=:::::::::::---##       
                             ##...::::::==:::::::::::::::::::::----##       
                             ##...:::::::=-::::-==::::--::::::-----##       
                             ##...:::::::::---:::===:::::::::------##       
                              %%..::::::::::::::::::::::::::------##        
                              ##..::::::::::::::::::::::::-------###        
                               #%.::::::::::::::::::::::--------*##         
                               .##::::::::::::::::::::---------###          
                               ##:::-:::::::::::::------------##            
                               ##::::-----------------------###             
                               ##::----------------------###+               
                                %#%%%%%####----------#####                  
                                           %#########                                           
"@
Write-Output $asciiLogo
Start-Sleep 1
Write-Output $asciiText
Start-Sleep 1
 

# Get the current user's home directory and extract the drive letter
$homeDirectory = [System.Environment]::GetFolderPath('UserProfile')
$driveLetter = $homeDirectory.Substring(0, 2)  # Get the drive letter (e.g., C: or D:)

# Construct the DumbJuice path dynamically
$dumbJuicePath = Join-Path -Path $driveLetter -ChildPath "DumbJuice"

# Create the directory if it doesn't exist
#New-Item -ItemType Directory -Path $dumbJuicePath -Force | Out-Null

Write-Output "DumbJuice path: $dumbJuicePath"

$pythonInstallPath = "$dumbJuicePath\python\$pythonVersion"
$programName = "excel data merger"
$programPath = "$dumbJuicePath\programs\$programName"
$programAppFolder = "$programPath\appfolder"
$sourceFolder = "$PSScriptRoot"  
$venvPath = "$programPath\venv"
$pythonExe = "$pythonInstallPath\python.exe"
$pythonInstallerPath = "$env:TEMP\python-installer.exe"

# Set paths for the downloaded program files (the ones inside 'appfolder')
$requirementsFile = "$programAppFolder\requirements.txt"
#$scriptToRun = "$sourceFolder\excel_merger_ui.py"

# Set path to the icon file
$iconFile = "$programAppFolder\djicon.ico"  # Make sure you have the .ico file in appfolder

# Ensure DumbJuice folder exists
New-Item -ItemType Directory -Path $dumbJuicePath -Force | Out-Null

# Check if Python version is installed
if (!(Test-Path "$pythonExe")) {
    Write-Output "Python $pythonVersion not found. Downloading..."
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-amd64.exe" -OutFile $pythonInstallerPath

    Write-Output "Installing Python..."
    Start-Process -FilePath $pythonInstallerPath -ArgumentList "/quiet InstallAllUsers=0 PrependPath=0 Include_test=0 TargetDir=$pythonInstallPath" -Wait

    # Remove installer after installation
    Remove-Item $pythonInstallerPath -Force
} else {
    Write-Output "Python $pythonVersion is already installed."
}

# Ensure program directory exists
New-Item -ItemType Directory -Path $programPath -Force | Out-Null

# Ensure appfolder inside the program folder exists
New-Item -ItemType Directory -Path $programAppFolder -Force | Out-Null

# Copy the program files from appfolder (installer folder) to the appfolder inside the program folder
Write-Output "Copying application files to $programAppFolder..."
Copy-Item -Path "$sourceFolder\*" -Recurse -Destination $programAppFolder -Force

# Create virtual environment if not exists
if (!(Test-Path "$venvPath")) {
    Write-Output "Creating virtual environment..."
    & "$pythonExe" -m venv "$venvPath"
}

# Install dependencies
Write-Output "Installing dependencies..."
& "$venvPath\Scripts\python.exe" -m pip install --upgrade pip
& "$venvPath\Scripts\python.exe" -m pip install -r $requirementsFile

# Install addins (if any)


    # read json config
    $DumbJuiceConfigPath = "$programAppFolder\dumbjuice.conf"
    $jsonData = Get-Content -Path $DumbJuiceConfigPath -Raw | ConvertFrom-Json
    $addins_environement_variable_paths = @()
    if (-not $jsonData.PSObject.Properties["addin_paths"]) {
      $jsonData | Add-Member -MemberType NoteProperty -Name "addin_paths" -Value @()
    }
    $jsonData.addin_paths = $addins_environement_variable_paths
    $jsonData | ConvertTo-Json -Depth 10 | Set-Content -Path $DumbJuiceConfigPath



# Create shortcut to run the program
$shortcutPath = "$programPath\$programName.lnk"
$targetPath = "$venvPath\Scripts\pythonw.exe"
$arguments = "`"$programAppFolder\excel_merger_ui.py`""
Write-Output "Creating shortcut..."
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = $targetPath
$Shortcut.Arguments = $arguments
$Shortcut.WorkingDirectory = $programAppFolder
$Shortcut.IconLocation = $iconFile  # Set the icon location for the shortcut
$Shortcut.WindowStyle = 1
$Shortcut.Save()

# Copy the shortcut to the Desktop
$desktopPath = [System.Environment]::GetFolderPath('Desktop')
$desktopShortcutPath = "$desktopPath\$programName.lnk"

Write-Output "Copying shortcut to Desktop..."
Copy-Item -Path $shortcutPath -Destination $desktopShortcutPath
Write-Output "Shortcut copied to Desktop."

$debugShortcutPath = "$programPath\$programName.debug.lnk"
$debugExecutablePath = "$venvPath\Scripts\python.exe"

Write-Output "Creating debug launcher..."
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($debugShortcutPath)
$Shortcut.TargetPath = $debugExecutablePath
$Shortcut.Arguments = "-i $arguments "
$Shortcut.WorkingDirectory = $programAppFolder
$Shortcut.IconLocation = $iconFile  # Set the icon location for the shortcut
$Shortcut.WindowStyle = 1
$Shortcut.Save()



Write-Output "Installation complete. Use the shortcut to run $programName!"
