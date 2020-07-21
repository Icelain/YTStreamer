import pafy
import vlc
import colorama,time
import shc
import json
from youtube_api import YoutubeDataApi

API_KEY="AIzaSyA_qsbJMvLaklHfbLKMq4zaoVE-7UTTqcM"

def getMaxResults():
    with open("msrs.json","r") as fileObj:
        return int(json.loads(fileObj.read())["max_res"])

def makeStreamable(string):
    return "https://www.youtube.com/watch?v=" + string

def getResults(query):
    streamableLinks=[]

    yt=YoutubeDataApi(API_KEY)
    searches=yt.search(q=query,max_results=getMaxResults())

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

    hourSubcomponents=3600 * int(shc.listToString(del0(hourSubcomponents)))
    minSubcomponents=60 * int(shc.listToString(del0(minSubcomponents)))
    secComponents=int(shc.listToString(del0(secComponents)))
    return hourSubcomponents+minSubcomponents+secComponents+2




colorama.init()
inp=input(colorama.Fore.CYAN+"Enter video query: "+colorama.Fore.YELLOW)
res=getResults(inp)
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
    print(colorama.Fore.GREEN,f"Now playing: [{video.title}][{video.duration}][@{bestaudio.quality}]",colorama.Style.RESET_ALL)
    end_time=time.time()+xz
    try:
        while time.time()!=end_time:
            pass
    except KeyboardInterrupt:
        print(colorama.Fore.RED+"\nStream Stopped"+colorama.Style.RESET_ALL)
        break
print(colorama.Fore.RED+"\nQueue finished")
