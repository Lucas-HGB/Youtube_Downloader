#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from argparse import ArgumentParser
from youtube_dl import YoutubeDL
from json import dump, load
from os import listdir, remove
from platform import system as arc
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC
from mutagen.mp3 import MP3 as open_MP3
from shutil import move
from wget import download
from ctypes.wintypes import  MAX_PATH
from ctypes import create_unicode_buffer
from ctypes import windll

class Youtube():

    def __init__(self, url, title, artist, album = False):
        self.url = url
        self.title = title
        self.artist = artist
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

    def __init__(self, file):
        self.name = [f for f in listdir() if f[0:3] == file[0:3]][0]

    def add_tags(self, info):
        self.audio = EasyID3(self.name)
        self.audio["title"] = info.title
        self.audio["artist"] = info.artist
        self.audio["album"] = info.album
        self.audio.save()

    def move(self):
        if arc().lower() == "windows":
            SHGFP_TYPE_CURRENT = 0
            CSIDL_PERSONAL = 13
            buf= create_unicode_buffer(MAX_PATH)
            windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
            musicsDir = buf.value
            move(f"{self.name}", r"{}/{}".format(musicsDir, self.name))
        else:
            move(f"{self.name}", r"/media/NTFS/Music/{}".format(self.name))

    def add_cover(self):
        self.audio = open_MP3(self.name)
        self.thumb = open("thumbnail.jpg", "rb")
        self.audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=self.thumb.read()))
        print("Changed art cover")
        self.audio.save()
        self.thumb.close()
