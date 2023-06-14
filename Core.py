from tkinter import filedialog
import subprocess
import requests
import shutil
import psutil
import glob
import time
import sys
import os



Media = os.getcwd() + "\\Media\\"
if os.path.exists(Media) != True:
    os.mkdir(Media)

    with open(Media + "README.txt") as f:
        f.write("To change the background video for valorant, put it in this folder, CAUTION, if multiple videos are in the folder, the first one will be used and if none are in the folder, the default one will be used.")



if os.path.exists("config.conf"):
    with open("config.conf", "r") as f:
        RiotPath = f.read()
else:
    if os.path.exists("C:\\Riot Games\\"):
        RiotPath = "C:\\Riot Games\\"
    else:
        RiotPath = filedialog.askdirectory(initialdir="/", title="Please select the Riot Games Folder")
        if RiotPath == "":
            RiotPath = RiotPath + "\\"
            sys.exit(0)

        with open("config.conf", "w+") as f:
            f.write(RiotPath)



#Restore old video to avoid riot launcher download
OldVids = glob.glob(Media + "\\Riot Original Video\\*", include_hidden=False)
for Vid in OldVids:
    shutil.copy2(Vid, f"{RiotPath}VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\{os.path.basename(Vid)}")


os.chdir(f"{RiotPath}Riot Client")
subprocess.Popen(RiotPath + "Riot Client\\RiotClientServices.exe --launch-product=valorant --launch-patchline=live")


Update = False
Found = False
while True:
    if Found:
        break
    else:
        Actives = psutil.process_iter()
        for Process in Actives:

            if Process.name() == "RiotClientUx.exe":
                Update = True

            elif Process.name() == "VALORANT-Win64-Shipping.exe":
                Found = True
                break

        time.sleep(1)


#We're in the Loading Screen
if Update:
    OldVids = glob.glob(f"{Media}\\Riot Original Video\\*.mp4") + glob.glob(f"{Media}\\Riot Original Video\\*.webm")
    for Vid in OldVids:
        os.remove(Vid)

    #Get new downloaded video
    NewVids = glob.glob(f"{RiotPath}VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\*.mp4") + glob.glob(f"{RiotPath}VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\*.webm")
    for Vid in NewVids:
        shutil.copy2(Vid, f"{Media}\\Riot Original Video\\{os.path.basename(Vid)}")


Medias = glob.glob(Media + "*.mp4")
Videos = glob.glob(f"{Media}\\Riot Original Video\\*.mp4") + glob.glob(f"{Media}\\Riot Original Video\\*webm")
if len(Medias) == 0:
    for Vid in Videos:
        shutil.copy2(Vid, f"{RiotPath}VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\{os.path.basename(Vid)}")
else:
    Video = Medias[0]
    for Vid in Videos:
        shutil.copy2(Video, f"{RiotPath}VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\{os.path.basename(Vid)}")
    

