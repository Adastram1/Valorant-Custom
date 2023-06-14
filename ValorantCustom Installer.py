from tkinter import filedialog
import win32com.client
import requests
import shutil
import glob
import sys
import os


def Setup():
    def Error(Content: str):
        print(Content)
        input()
        sys.exit(1)

    #Get Folder
    if os.path.exists("C:\\Riot Games\\"):
        RiotPath = "C:\\Riot Games\\"
    else:
        RiotPath = filedialog.askdirectory(initialdir="/", title="Please select the Riot Games Folder")
        if RiotPath == "":
            sys.exit(0)
        RiotPath = RiotPath.replace("/", "\\") + "\\"
        print(RiotPath)

    #Ask where to store our files
    ValorantCustom = filedialog.askdirectory(initialdir=os.path.expanduser("~\\Documents"), title="Please select a location for the installation")
    if ValorantCustom == "":
        sys.exit(0)
    else:
        ValorantCustom = ValorantCustom + "\\Valorant Custom\\"
        os.mkdir(ValorantCustom)
        Media = ValorantCustom + "Media\\"
        os.mkdir(Media)
        os.mkdir(Media + "Riot Original Video")


    #Writing that for our Core Module as a config file
    try:
        with open(ValorantCustom + "config.conf", "w+") as f:
            f.write(RiotPath)
    except:
        Error("Can't create a configuration file")


    #Ask wich video will be the new background
    Video = filedialog.askopenfilename(initialdir=os.path.expanduser("~\\Videos"), filetypes=[("Video", "*.mp4")], title=f"Please select the video to be used as your custom wallpaper, you can still change it by replacing it with a new one in {Media}")    
    if Video != "":
        shutil.copy(Video, Media + os.path.basename(Video))
    

    #Copy olds videos to bypass riot integrity check
    try:
        Olds = glob.glob(f"{RiotPath}VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\*.mp4") + glob.glob(f"{RiotPath}VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\*.webm")
        for Vid in Olds:
            print(Vid)
            shutil.copy(Vid, f"{Media}\\Riot Original Video\\{os.path.basename(Vid)}")
    except:
        Error("Can't move videos")


    #Adding a README to explain how to change the video
    try:
        with open(Media + "README.txt", "w+") as f:
            f.write("To change the background video for valorant, put it in this folder, CAUTION, if multiple videos are in the folder, the first one will be used and if none are in the folder, the default one will be used.")
    except:
        Error("Can't write README")


    #Get our core code
    response = requests.get("https://github.com/Adastram1/Valorant-Custom/blob/main/Core.exe")
    if response.status_code == 200:
        with open(ValorantCustom + "Core.exe", "wb") as f:
            f.write(response.content)
        Core = ValorantCustom + "Core.exe"
    else:
        Error("Can't Download Core Module")


    #Create our brand new link for desktop
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(os.path.expanduser("~\\Desktop") + "\\Valorant.lnk")
        shortcut.TargetPath = Core
        shortcut.WorkingDirectory = ValorantCustom
        shortcut.IconLocation = f"{os.path.expandvars('%SystemDrive%')}\\ProgramData\\Riot Games\\Metadata\\valorant.live\\valorant.live.ico,0"
        shortcut.Save()
    except:
        Error("Can't create a link in desktop")


Setup()    