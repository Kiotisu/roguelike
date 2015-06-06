"""
music control
"""

import os
import pygame
from aux import Aux

class Music(object):
    """ music control """
    def __init__(self):
        self.song_num = None
        self.songs = None
        self.volume = None

    def load_music(self):
        """load music from /music"""
        #https://freemusicarchive.org/music/Sycamore_Drive/Sycamore_Drive/
        self.song_num = 0
        self.songs = Aux.files("music")
        self.volume = 0.00
        song_ended = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(song_ended)
        pygame.mixer.pre_init(44100, -16, 2, 2048)

        path = r"./music/"
        uni_path = path.replace('/', os.sep).replace('\\', os.sep)
        for song in xrange(len(self.songs)):
            pygame.mixer.music.load(uni_path + self.songs[song])

    def play_music(self):
        """ play music """
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        self.song_num = (self.song_num+1) % len(self.songs)
