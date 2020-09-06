import pafy
import colorama,time
import json
from playsound import playsound
from youtube_api import YoutubeDataApi
from pyfiglet import Figlet
import subprocess,sys,os
import multiprocessing
import argparse
__version__="1.1.0"
glurl=""

FREE_API_KEY="AIzaSyA_qsbJMvLaklHfbLKMq4zaoVE-7UTTqcM"


'''Play function'''
def play():
    playsound(glurl)
'''Multiprocessed play function end'''

def checkForGi():
    if sys.platform=="linux":
        try:
            from gi import require_version
        except:
            print(colorama.Fore.RED+"Please install gstreamer bindings for python on linux to run ytstreamer"+colorama.Style.RESET_ALL)
            quit()


def makeStreamable(string):
    return "https://www.youtube.com/watch?v=" + string

def listToString(lst):
    return "".join(lst)

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



def runmain():
    global glurl
    colorama.init()
    checkForGi()
    cs_fig=Figlet(font="jazmine")
    print(colorama.Fore.LIGHTGREEN_EX,cs_fig.renderText("Yt_Streamer"),colorama.Style.RESET_ALL)
    try:
        inp=input(colorama.Fore.CYAN+"Enter video query: "+colorama.Fore.YELLOW)
    except KeyboardInterrupt:
        print(colorama.Fore.RED+"Exited"+colorama.Style.RESET_ALL)
        quit()

    res=getResults(inp)
    res_counter=1
    for re in res:
        video=pafy.new(re)
        bestaudio=video.getbestaudio()
        url=bestaudio.url
        glurl=url
        xz=timeToInt(video.duration)
        print(colorama.Fore.GREEN,f"Now playing[{res_counter}]: [{video.title}][{video.duration}][@{bestaudio.quality}]",colorama.Style.RESET_ALL)


        process=multiprocessing.Process(target=play)
        process.start()
        try:
            args=input("~ ")
        except KeyboardInterrupt:
            process.terminate()
            print(colorama.Fore.RED+"\nStream Stopped"+colorama.Style.RESET_ALL)
            break


        if args.lower()=="quit" or args.lower()=="q":
            process.terminate()
            print(colorama.Fore.RED+"\nStream Stopped"+colorama.Style.RESET_ALL)
            break

        if args.lower()=="next" or args.lower()=="n":
            process.terminate()
            res_counter+=1
            continue

    print(colorama.Fore.RED+"\nQueue finished")
    print("Exited")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("-v","--version",dest="ver",action="store_true")
    recv_args=parser.parse_args()
    if recv_args.ver:
        print(__version__)
    else:
        runmain()
'''if __name__=="__main__":
    runmain()'''
