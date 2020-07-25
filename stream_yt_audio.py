import pafy
import vlc
import colorama,time
import json
from youtube_api import YoutubeDataApi
from pyfiglet import Figlet
import subprocess,sys,os
from yt_audio_streamer.checks import checkForVlc
from shc import listToString

FREE_API_KEY="AIzaSyA_qsbJMvLaklHfbLKMq4zaoVE-7UTTqcM"


def makeStreamable(string):
    return "https://www.youtube.com/watch?v=" + string

def getResults(query):
    streamableLinks=[]

    yt=YoutubeDataApi(FREE_API_KEY)
    searches=yt.search(q=query,max_results=10)

    for i in searches:
        streamableLinks.append(makeStreamable(i["video_id"]))
    return streamableLinks


def del0(lst):
    if lst[0]=="0":
        del lst[0]
    return lst


def timeToInt(tstr):
    components=tstr.split(":")
    hourSubcomponents=list(components[0])
    minSubcomponents=list(components[1])
    secComponents=list(components[2])

    hourSubcomponents=3600 * int(listToString(del0(hourSubcomponents)))
    minSubcomponents=60 * int(listToString(del0(minSubcomponents)))
    secComponents=int(listToString(del0(secComponents)))
    return hourSubcomponents+minSubcomponents+secComponents+2

def runAllchecks():
    if not checkForVlc():
        print(colorama.Fore.RED+"Since vlc media player not installed, exiting...",colorama.Style.RESET_ALL)
        quit()


def main():
    runAllchecks()

    colorama.init()
    cs_fig=Figlet(font="jazmine")
    print(colorama.Fore.LIGHTGREEN_EX,cs_fig.renderText("Yt_Streamer"),colorama.Style.RESET_ALL)

    inp=input(colorama.Fore.CYAN+"Enter video query: "+colorama.Fore.YELLOW)
    res=getResults(inp)
    res_counter=1
    for re in res:
        video=pafy.new(re)
        bestaudio=video.getbestaudio()
        url=bestaudio.url
        xz=timeToInt(video.duration)
        Instance = vlc.Instance()
        player = Instance.media_player_new()
        Media = Instance.media_new(url)
        Media.get_mrl()
        player.set_media(Media)
        player.play()
        print(colorama.Fore.GREEN,f"Now playing[{res_counter}]: [{video.title}][{video.duration}][@{bestaudio.quality}]",colorama.Style.RESET_ALL)
        end_time=time.time()+xz
        try:
            while time.time()!=end_time:
                pass
        except KeyboardInterrupt:
            print(colorama.Fore.RED+"\nStream Stopped"+colorama.Style.RESET_ALL)
            break
        res_counter+=1
    print(colorama.Fore.RED+"\nQueue finished")
