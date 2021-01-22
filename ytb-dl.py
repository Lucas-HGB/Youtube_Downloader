#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from argparse import ArgumentParser
from youtube_dl import YoutubeDL
from json import dump, load
from os import listdir, system
from platform import system as arc
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC
from mutagen.mp3 import MP3 as open_MP3
from eyed3 import load
from shutil import move 
from wget import download


def find_directories():
    from winreg import HKEY_CURRENT_USER, OpenKey, KEY_READ, QueryValueEx
    try:
        contador = 0
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        for i in range(4):
            contador += 1
            if contador == 1:
                key = "{374DE290-123F-4565-9164-39C4925E467B}"
            elif contador == 2:
                key = "My Music"
            elif contador == 3:
                key = "My Video"
            elif contador == 4:
                key = "Personal"
            reg_key = OpenKey(HKEY_CURRENT_USER, reg_path, 0, KEY_READ)
            directory = QueryValueEx(reg_key, key)[0]
            if contador == 1:
                downloads = directory
            elif contador == 2:
                music = directory
            elif contador == 3:
                video = directory
            elif contador == 4:
                documents = directory
        directories = {"downloads": downloads, "music": music, "video": video, "documents": documents}
    except Exception as excp:
        print(excp)
    return directories

class Txt():
    def __init__(self):
        pass

    def add(self, new):
        data = {}
        data["artists"] = []
        try:
            for artist in self.__str__()["artists"]:
                data["artists"].append(artist)
        except KeyError:
            pass
        for artist in new.split():
            if artist not in data["artists"]:
                data["artists"].append(artist)
            with open("artists.json", "w") as file:
                dump(data, file)

    def __str__(self):
        try:
            with open("artists.json", "r") as json_file:
                try:
                    data = load(json_file)
                except:
                    data = {}
        except FileNotFoundError:
            with open("artists.json", "w") as json:
                pass
            data = {}
        return data

class Youtube():

    def __init__(self, url, title, artist, date, album = False):
        self.url = url
        self.title = title
        self.artist = artist
        self.date = date
        self.album = album
        options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]}
        self.youtube = YoutubeDL(options)

    def __str__(self):
        return f"Title: {self.title}\nArtist: {self.artist}"

    def download_audio(self):
        self.youtube.download([self.url])
  		
    def download_thumb(self):
        thumbnails = self.youtube.extract_info(self.url,download = False)
        thumbnails = thumbnails["thumbnails"]
        count = 0
        for thumb in thumbnails:
            if count == 0:
                download(thumb["url"], out = "thumbnail.jpg")
            count += 1

class MP3():
    
    def __init__(self):
        self.name = [f for f in listdir() if f.endswith("mp3")][0]
          
    def add_tags(self, info):
        self.audio = EasyID3(self.name)
        self.audio["title"] = info.title
        self.audio["artist"] = info.artist
        self.audio["album"] = info.album
    
    def move(self):
        if arc().lower() == "windows":
            directories = find_directories()
            move(f"{self.name}", r"{}/{}".format(directories["music"], self.name))
        else:
            move(f"{self.name}", r"/media/NTFS/Music/{}".format(self.name))

    def add_cover(self):
        self.audio = open_MP3(self.name)
        self.thumb = open("thumbnail.jpg", "rb")
        self.audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=self.thumb.read()))

    def save(self):
        self.audio.save()



#Extrai argumentos passados para o programa
def args():
    parser = ArgumentParser()
    parser.add_argument("-u", "--url", dest="url",
                        help="youtube video URL", metavar="youtube URL")
    parser.add_argument("-t", "--title", dest="title",
                        help="Song title", metavar="Song title")
    parser.add_argument("-add", "--add", dest="add_artist",
                        help="Add artist", metavar="Add artist")
    parser.add_argument("-a", "--album", dest="album",
                        help="specify album", metavar="Song album")
    parser.add_argument("-p", "--producer", dest="producer",
                        help="specify album", metavar="Song artist")
    args = parser.parse_args()
    return args

args = args()
txt = Txt()


if args.add_artist:
    for artist in args.add_artist.split():
        txt.add(artist.lower())

#Le json e retorna os artistas
try:
    artists = txt.__str__()["artists"]
except KeyError:
    artists = []

youtube = YoutubeDL({})
if args.url:
    if not args.producer:
        uploader = youtube.extract_info(url = args.url, download=False)["uploader"]
    elif args.producer:
        uploader = args.producer
    date = youtube.extract_info(url = args.url, download=False)["release_date"]
    #Se titulo n e fornecido
    if not args.title:
        new_title = ""
        count = 0
        title = youtube.extract_info(url = args.url, download=False)["title"]
        for word in title.split():
            if word.lower() in artists:
                title = title.replace(word, "")
        for word in title.split():
            count += 1
            if word != "-":
                if count != 0:
                    new_title = new_title + " " + word
                elif count == 0:
                    new_title = new_title + word
        title = new_title
    elif args.title:
        title = args.title
    if args.album:
        Youtube = Youtube(url = args.url, title = title, artist = uploader, date = date, album = args.album)
    elif not args.album:
        Youtube = Youtube(url = args.url, title = title, artist = uploader, date = date, album = "")
    Youtube.download_audio()
    Youtube.download_thumb()
    mp3 = MP3()
    mp3.add_tags(Youtube)
    mp3.add_cover()
    mp3.save()
    mp3.move()
