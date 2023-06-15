from tkinter import filedialog
import subprocess
import shutil
import psutil
import glob
import time
import sys
import os



Media = os.getcwd() + "\\Media\\"
RiotOriginal = Media + "Riot Original Video\\"

#Rebuild directory in case they got deleted
os.makedirs(RiotOriginal, exist_ok=True)

#Check for readme file and restore it if deleted
if os.path.exists(Media + "README.txt") != True:
    with open(Media + "README.txt") as f:
        f.write("To change the background video for valorant, put it in this folder, CAUTION, if multiple videos are in the folder, the first one will be used and if none are in the folder, the default one will be used.")

#Read config file to get Riot Path and create a new one if not foud
Build = False
if os.path.exists("config.conf"):
    with open("config.conf", "r") as f:
        RiotPath = f.read()
        if RiotPath == "":
            Build = True
else:
    Build = True

if Build:
    #Build new config file
    if os.path.exists("C:\\Riot Games\\"):
        RiotPath = "C:\\Riot Games\\"
    else:
        RiotPath = filedialog.askdirectory(initialdir="/", title="Please select the Riot Games Folder")
        if RiotPath == "":
            sys.exit(0)

        #Reformat Path and write it in our config file
        RiotPath = RiotPath.replace("/", "\\") + "\\"
        with open("config.conf", "w+") as f:
            f.write(RiotPath)


Valorant = RiotPath + "VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\"


def GetVideos(From: str):
    """Returns the path list of all videos with .mp4 and .webm extensions"""
    Videos = glob.glob(From + "*.mp4", include_hidden=False) + glob.glob(From + "*.webm", include_hidden=False)
    return Videos
    
def MoveTo(From: str, To: str):
    """Move all videos with .mp4 and .webm extensions from one folder to another and overwrite existing videos"""
    Videos = GetVideos(From)
    for Vid in Videos:
        shutil.copy2(Vid, To + os.path.basename(Vid))


#Restore old video to avoid riot launcher download
MoveTo(RiotOriginal, Valorant)

#Start Valorant with defaults arguments
os.chdir(f"{RiotPath}Riot Client\\")
subprocess.Popen(RiotPath + "Riot Client\\RiotClientServices.exe --launch-product=valorant --launch-patchline=live")


#Look for Valorant to start, and track riot launcher for updates wich would require us to replace riot's original videos
Update = False
Found = False
while True:
    if Found:
        break
    else:
        for Process in psutil.process_iter():
            Name = Process.name()
            if Name == "RiotClientUx.exe":
                Update = True

            elif Name == "VALORANT-Win64-Shipping.exe":
                Found = True
                break

        time.sleep(1)


#We're in the Loading Screen
if Update:
    #Delete Old Videos that are no longer used 
    for Vid in GetVideos(RiotOriginal):
        os.remove(Vid)

    #Get new downloaded video
    MoveTo(Valorant, RiotOriginal)


#Get user's custom video and if none are found use riot's original videos
UserVideos = GetVideos(Media)
if UserVideos:
    #Duplicate user's video with riot's videos name
    for Vid in GetVideos(RiotOriginal):
        shutil.copy2(UserVideos[0], Valorant + os.path.basename(Vid))
else:
    #Use riot's original videos
    MoveTo(RiotOriginal, Valorant)