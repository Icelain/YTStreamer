#usr/bin/python3


import colorama,time
import json
from playsound import playsound
from pyfiglet import Figlet
import sys,os
import multiprocessing
import argparse
__version__="1.1.4"

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

    from youtube_api import YoutubeDataApi

    yt=YoutubeDataApi(FREE_API_KEY)
    searches=yt.search(q=query,max_results=10)

    for i in searches:
        streamableLinks.append(makeStreamable(i["video_id"]))
    return streamableLinks


def del0(lst):
    if lst[0]=="0":
        del lst[0]
    return lst

'''
def timeToInt(tstr):
    components=tstr.split(":")

    hourSubcomponents=list(components[0])
    minSubcomponents=list(components[1])
    secComponents=list(components[2])

    hourSubcomponents=3600 * int(listToString(del0(hourSubcomponents)))
    minSubcomponents=60 * int(listToString(del0(minSubcomponents)))
    secComponents=int(listToString(del0(secComponents)))

    return hourSubcomponents+minSubcomponents+secComponents+2
'''


def runmain():
    import pafy
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

    while res_counter < len(res):
        video=pafy.new(res[res_counter-1])

        bestaudio=video.getbestaudio()
        url=bestaudio.url
        
        glurl=url
        
        #xz=timeToInt(video.duration) not being used currently but is required for later versions where I'll be using a custom gst player instead of playsound
        
        print(colorama.Fore.LIGHTMAGENTA_EX,f"Now playing[{res_counter}]: [{video.title}][{video.duration}][@{bestaudio.quality}]",colorama.Style.RESET_ALL)


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
        if args.lower()=="restart" or args.lower()=="r":
            process.terminate()
            res_counter=1
            continue    
        if args.lower=="previous" or args.lower()=="p":
            process.terminate()
            res_counter-=1
            continue    

    print(colorama.Fore.RED+"\nQueue finished")
    print("Exited")

def main():
    parser=argparse.ArgumentParser()

    parser.add_argument("-v","--version",dest="ver",action="store_true")
    parser.add_argument("-hy","--yelp",dest="hbool",action="store_true")
    
    recv_args=parser.parse_args()

    if recv_args.ver:
        print(__version__)

    elif recv_args.hbool:
        print("Help:\n\n-v or --version- Displays version\n-h or --help - Displays Help\n\nPlayer commands-\n\n1. n or next to get to the next stream\n2. q or quit to quit the script.(Ctrl-C also works)\n3. r or restart to restart the queue\n4. p or previous to go back to previous stream. ")    
    
    else:
        runmain()

'''if __name__=="__main__":
    main()'''

