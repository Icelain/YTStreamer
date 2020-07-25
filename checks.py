import subprocess,sys,os

def checkForVlc():
    returnvar=False

    if sys.platform=="linux":
        try:
            subprocess.call(["vlc","-h"],shell=False,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
            returnvar=True
        except:
            print("Please install vlc media player to run yt_streamer")

    elif sys.platform=="win32":
        if os.path.exists(r"C:\Program Files\VideoLAN\VLC\vlc.exe"):
            returnvar=True
        else:
            print("Please install vlc media player to run yt_streamer")

    elif sys.platform=="darwin":
        if os.path.exists("/Applications/VLC.app/Contents/MacOS/VLC"):
            returnvar=True
        else:
            print("Please install vlc media player to run yt_streamer")
    return returnvar
