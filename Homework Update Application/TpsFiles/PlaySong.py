import pygame
import os.path
import os
from random import randint
from mutagen.mp3 import MP3
from playsound import playsound
import winsound
from mutagen import File
import eyed3
from io import BytesIO
import time
from PIL import Image

os.system('cls')

path1 = r"C:\Program Files (x86)\TpsFiles"

def pygamesound(x):
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.init(44100, -16, 2, 2048)
    #pygame.mixer.init(22050, -16, 2, 1024)
    os.system('cls')

    audio = eyed3.load(x)
    artist = audio.tag.artist
    title = audio.tag.title

    file = File(x)
    img = file.tags['APIC:'].data
    pygame.mixer.music.load(x)
    bgm = pygame.mixer.music.play()
    #while pygame.mixer.music.get_busy():  # wait for music to finish playing
        #print('here')
    im = Image.open(BytesIO(img))
    return (im,title,artist)

def playrandsong(lofbgms):
    done = []
    n = len(lofbgms)
    i = randint(0,n-1)
    x = lofbgms[i]
    name = x.split('BGMS')
    name = name[1][1:]
    length = MP3(x).info.length
    #print(length)
    p = pygamesound(x)
    #print(f'\n\tPlaying song: {name.rstrip(".mp3")}\n')
    #time.sleep(0.2)
    return p
    

def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.
    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            if filepath[-4:]==".mp3":
                file_paths.append(filepath)  # Add it to the list.
    return file_paths

def playbgm(debugsong):
    if debugsong is False:
        return
    path= path1 + r'\BGMS'
    #print(path)
    full_file_paths = get_filepaths(path)
    lofbgms = full_file_paths
    p = playrandsong(lofbgms)
    return p

def click():
    sound = path1 + r'\Effects\Click.wav'
    #print(sound)
    winsound.PlaySound(sound, winsound.SND_ASYNC | winsound.SND_ALIAS )
    return
