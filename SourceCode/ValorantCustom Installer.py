from tkinter import filedialog
import win32com.client
import requests
import shutil
import glob
import sys
import os


def Setup():
    #Get Folder
    if os.path.exists("C:\\Riot Games\\"):
        RiotPath = "C:\\Riot Games\\"
    else:
        #Autodetection didn't work, ask where is the riot folder
        RiotPath = filedialog.askdirectory(initialdir="/", title="Please select the Riot Games Folder")
        if RiotPath == "":
            #User canceled, exiting
            sys.exit(0)
        RiotPath = RiotPath.replace("/", "\\") + "\\"

    #Ask where to store our files
    ValorantCustom = filedialog.askdirectory(initialdir=os.path.expanduser("~\\Documents"), title="Please select a location for the installation")
    if ValorantCustom == "":
        #User canceled, exiting
        sys.exit(0)
    else:
        ValorantCustom = ValorantCustom + "\\Valorant Custom\\"
        Valorant = RiotPath + "VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\"
        Media = ValorantCustom + "Media\\"
        RiotOriginal = Media + "Riot Original Video"
        os.makedirs(RiotOriginal, exist_ok=True)


    #Writing that for our Core Module as a config file
    with open(ValorantCustom + "config.conf", "w+") as f:
        f.write(RiotPath)


    #Ask wich video will be the new background
    Video = filedialog.askopenfilename(initialdir=os.path.expanduser("~\\Videos"), filetypes=[("Video", "*.mp4")], title=f"Please select the video to be used as your custom wallpaper, you can still change it by replacing it with a new one in {Media}")    
    if Video != "":
        #Not important if user didn't specify as Core will use riot's videos if none of the user are specified
        shutil.copy(Video, Media + os.path.basename(Video))
    

    #Copy olds videos to bypass riot integrity check
    for Vid in glob.glob(f"{Valorant}*.mp4") + glob.glob(f"{Valorant}*.webm"):
        shutil.copy(Vid, RiotOriginal + os.path.basename(Vid))


    #Adding a README to explain how to change the video
    with open(Media + "README.txt", "w+") as f:
        f.write("To change the background video for valorant, put it in this folder, CAUTION, if multiple videos are in the folder, the first one will be used and if none are in the folder, the default one will be used.")


    #Get our Core codes
    response = requests.get("https://github.com/Adastram1/Valorant-Custom/raw/main/Core/Core.exe")
    if response.status_code == 200:
        Core = ValorantCustom + "Core.exe"
        with open(Core, "wb") as f:
            f.write(response.content)
    else:
        raise f"Error while downloading Core.exe file from Github, error code : {response.status_code}"


    #Create our brand new link for desktop
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(os.path.expanduser("~\\Desktop") + "\\Valorant.lnk")
    shortcut.TargetPath = Core
    shortcut.WorkingDirectory = ValorantCustom
    shortcut.IconLocation = f"{os.path.expandvars('%SystemDrive%')}\\ProgramData\\Riot Games\\Metadata\\valorant.live\\valorant.live.ico,0"
    shortcut.Save()
Setup()