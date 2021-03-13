import tkinter as tk
from ytb_dl import Youtube, MP3
from os import remove
from youtube_dl import YoutubeDL


def download(self, url, title, artist, album):
    Youtube = Youtube(url = url, title = title, artist = artist, album = album)
    mp3 = MP3()
    Youtube.download_audio()
    Youtube.download_thumb()
    mp3.add_tags(Youtube)
    mp3.add_cover()
    mp3.move()
    remove("thumbnail.jpg")

root= tk.Tk()
root.title("Youtube Downloader")

canvas1 = tk.Canvas(root, width = 400, height = 200)
canvas1.pack()


## LABELS
label_url = tk.Label(text="LINK")
canvas1.create_window(50, 30, window=label_url)
label_title = tk.Label(text="TÍTULO")
canvas1.create_window(50, 60, window=label_title)
label_artist = tk.Label(text="ARTISTA")
canvas1.create_window(50, 90, window=label_artist)
label_album = tk.Label(text="ALBUM")
canvas1.create_window(50, 120, window=label_album)



## INPUTS
url_input = tk.Entry(root) 
canvas1.create_window(250, 30, window=url_input, width= 300)
title_input = tk.Entry(root) 
canvas1.create_window(200, 60, window=title_input, width= 200)
artist_input = tk.Entry(root) 
canvas1.create_window(200, 90, window=artist_input, width= 200)
album_input = tk.Entry(root) 
canvas1.create_window(200, 120, window=album_input, width= 200)


def start_download_mp3():  
    url = url_input.get()
    artist = artist_input.get()
    album = album_input.get()
    title = title_input.get()
    ytb = Youtube(url = url, title = title, artist = artist, album= album)
    ytb.download_audio()
    label1 = tk.Label(root, text= "Downloading")
    canvas1.create_window(200, 150, window=label1)
    ytb.download_thumb()
    mp3 = MP3()
    mp3.add_tags(ytb)
    mp3.add_cover()
    remove("thumbnail.jpg")
    label1 = tk.Label(root, text= "Done")
    canvas1.create_window(200, 150, window=label1)

def download_mp4():
    url = url_input.get()
    youtube = YoutubeDL()
    youtube.download([url])


## BUTTONS
button1 = tk.Button(text='Download MP3', command=start_download_mp3)
canvas1.create_window(200, 150, window=button1)
button1 = tk.Button(text='Download MP4', command=download_mp4)
canvas1.create_window(200, 180, window=button1)

root.mainloop()
