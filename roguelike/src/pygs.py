# -*- coding: utf-8 -*-
"""
main app
"""

import pygame
import pygame.locals as LOC
import os
import characters
from maps import Map
from collections import deque
from aux1 import Aux
from music import Music

Hero = characters.Hero
Enemy = characters.Enemy


class App(object):
    """ doc """
    def execute(self):
        """ s """
        self.init()

        while self._running:
            for event in pygame.event.get():
                self.event(event)
            self.turn()
            self.render()
        # self.cleanup()

    def __init__(self):
        """ s """
        self._running = True
        self._surface = None
        self._size = self.weight, self.height = 810, 650
        self._map = Map(50, (10, 10))  #rmnum, rsize
        self._posx = 250
        self._posy = 250

        self._horizon = 3
        # zasieg wzroku w kazda strone  if == 3 => [][][] postac [][][]
        #trochę to głupie, horyzont powinien być okrągły. I większy @SMN
        self._myturn = True

        # gosc czasem rodzi sie w pustce
        # XDDDDDDDDDDDDDD @WJ
        while self._map[self._posx, self._posy][0] == '_':
            self._posx += 1

        self._hero = None
        self._enemy1 = None
        self._display_surf = None

        self._image_library = None
        # self.hero_image = None
        # self.wall = None
        # self.terrain = None
        # self.enemy1 = None

    #Dorzucam deklaracje tych wszystkich self.cos do __init__
    #ale jesli serio ma byc tego tak duzo to bedzie to trzeba niestety przeniesc
    #do innej klasy pewnie... @WJ

    #Dobra, niektóre nawet nie są potrzebne

        self._action = None
        self._marked = (None, None)

        self.aux = Aux()
        self.mus = Music()

    def init(self):
        """ s """
        pygame.init()
        pygame.display.set_caption('Rogal')
        self._surface = pygame.display.set_mode(self._size)
        self._running = True
        self._display_surf = pygame.display.set_mode(self._size,
                                                     pygame.HWSURFACE)
        self.load_images()
        self.mus.load_music()
        self.mus.play_music()

        #Create Hero
        self._hero = Hero(0, 0, 1, 1, 1, 0, 100, self._posx, self._posx)
        #Create Enemy
        self._enemy1 = Enemy(1, 1, 1, 0, 100, 260, 260)
        # attack, defense, damage, armor, hp, x, y

        self.aux.do_nice_outlines(self._surface)
        pygame.key.set_repeat(5, 100)  #(delay, interval) in milisec

        #napisy
        self.aux.write(self._surface, "EQ", 22, 700, 0)
        self.aux.write(self._surface, "Stats:", 14, 615, 6*40+20)
        self.aux.write(self._surface, "HP", 14, 615, 6*40+35)  # +15 pix pionowo
        self.aux.write(self._surface, "Attack", 14, 615, 6*40+50)
        self.aux.write(self._surface, "Defense", 14, 615, 6*40+65)
        self.aux.write(self._surface, "Armor", 14, 615, 6*40+80)

        self.aux.write(self._surface, str(self._hero._hp), 14, 675, 6*40+35)
        self.aux.write(self._surface, str(self._hero._attack), 14, 675, 6*40+50)
        self.aux.write(self._surface, str(self._hero._defense), 14, 675, 240+65)
        self.aux.write(self._surface, str(self._hero._armor), 14, 675, 6*40+80)

    def event(self, event):
        """ to do, soon"""
        #alternative?
        # pressedkeys = pygame.key.get_pressed()
        # if pressedkeys[pygame.K_x]:

        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if self._myturn: # == TRUE zbędne
                if event.key == LOC.K_UP or event.key == LOC.K_w:
                    if self._posy > 0\
                            and self._map[self._posx, self._posy-1][0] != '_':
                        self._posy -= 1
                        self._action.append('w')
                        self._myturn = False
                if event.key == LOC.K_DOWN or event.key == LOC.K_s:
                    if self._posy < self._map.size[1]-1\
                            and self._map[self._posx, self._posy+1][0] != '_':
                        self._posy += 1
                        self._action.append('s')
                        self._myturn = False
                if event.key == LOC.K_LEFT or event.key == LOC.K_a:
                    if self._posx > 0\
                            and self._map[self._posx-1, self._posy][0] != '_':
                        self._posx -= 1
                        self._action.append('a')
                        self._myturn = False
                if event.key == LOC.K_RIGHT or event.key == LOC.K_d:
                    if self._posx < self._map.size[0]-1\
                            and self._map[self._posx+1, self._posy][0] != '_':
                        self._posx += 1
                        self._action.append('d')
                        self._myturn = False

            if event.key == LOC.K_ESCAPE:  #quit
                self._running = False
            if event.key == LOC.K_m:  #volume up
                if self.mus.volume <= 1:
                    self.mus.volume += 0.05
                    pygame.mixer.music.set_volume(self.mus.volume)
            if event.key == LOC.K_n:  #volume down
                if self.mus.volume >= 0:
                    self.mus.volume -= 0.05
                    pygame.mixer.music.set_volume(self.mus.volume)

        if event.type == pygame.USEREVENT + 1:
            print(self.aux.song_num, "song ended")
            self.aux.play_music()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                (po_x, po_y) = pygame.mouse.get_pos()
                #mouse pointer in the equipment zone
                if po_x >= 610 and po_y >= 20 and po_y <= 20+6*40:
                    (square_x, square_y) = ((po_x-610)/40, (po_y-20)/40)
                    self._marked = (square_x, square_y)

    def render(self):
        """ in prog """
        _boczne_pola = (19-1)/2  # powinno byc 9
        if self._posx < _boczne_pola:
            x_o = 0
        elif self._posx > self._map.size[0]-_boczne_pola-1:
            x_o = self._map.size[0] - (2*_boczne_pola+1)  #2*_boczne_pola+1 = 19
        else:
            x_o = self._posx-_boczne_pola
        if self._posy < _boczne_pola:
            y_o = 0
        elif self._posy > self._map.size[1]-_boczne_pola-1:
            y_o = self._map.size[1] - (2*_boczne_pola+1)
        else:
            y_o = self._posy-_boczne_pola
        for y in xrange(19):
            for x in xrange(19):
                if self._map[(x_o+x), (y_o+y)][0] != '_':  # podloga
                    pygame.draw.rect(self._surface,
                                     ((self._map[(x_o+x), (y_o+y)][0]*64)%256,
                                      100,
                                      (self._map[(x_o+x), (y_o+y)][0]*32)%256),
                                     (x * 32, y * 32, 32, 32))
                    self._display_surf.blit(self._image_library["texture18.png"],
                                            (x * 32, y * 32))
                #elif (x_o+x) % 5 == 0 or (y_o+y) % 5 == 0:
                #    pygame.draw.rect(self._surface,
                #                     (0, 255, 0),
                #                     (x * 32, y * 32, 32, 32))
                else:  # pustka - nie sciana
                    # self._display_surf.blit(self.wall, (x * 32, y * 32))
                    pygame.draw.rect(self._surface, (0, 0, 0),
                                     (x * 32, y * 32, 32, 32))
                #hero
                if (x_o+x, y_o+y) == (self._posx, self._posy):
                    self._display_surf.blit(self._image_library["ball.png"],
                                            (x * 32, y * 32))
                #enemy
                # if self._map[(x_o+x),(y_o+y)][2] != None:
                    # self._display_surf.blit(self._image_library["enemy1.png"],
                                            # (x * 32, y * 32))

                #vision
                if not (abs(x_o+x - self._posx) <= self._horizon
                        and abs(y_o+y - self._posy) <= self._horizon):
                    self._display_surf.blit(self._image_library["black.png"],
                                            (x * 32, y * 32))

        #volume visual
        self._display_surf.blit(self._image_library["speaker.png"], (0, 612))
        light_straps = (0, 96, 0)
        dark_straps = (0, 32, 0)
        wid = 5

        for strap in xrange(20):
            if strap < self.mus.volume*20:
                pygame.draw.rect(self._surface, light_straps,
                                 (20+strap*wid, 650-strap*2, wid-1, strap*2))
            else:
                pygame.draw.rect(self._surface, dark_straps,
                                 (20+strap*wid, 650-strap*2, wid-1, strap*2))
        pygame.display.update()


    def load_images(self):
        """ load images from /items """
        path = r"./items/"
        lista = self.aux.files("items")
        self._image_library = {}

        for item in lista:
            uni_path = path.replace('/', os.sep).replace('\\', os.sep)
            #universal path, also works: os.path.join('','')
            self._image_library[item] = pygame.image.load(uni_path + item)\
                .convert_alpha()

        #define short names
        # self.hero_image = self._image_library["ball.png"]
        # self.wall = self._image_library["texture9.png"]
        # self.terrain = self._image_library["texture18.png"]  # 12 lub 18
        # self.enemy1 = self._image_library["enemy1.png"]


    def turn(self):
        """ who moves """
        if self._myturn:
            self._action = deque([])  # kolejka dwukierunkowa
        else:
            self.player_action()
            self.enemy_turn()

    def player_action(self):
        """ execute what player did in his turn """
        while len(self._action) > 0:
            act = self._action.popleft()  # zwroc akcje
            # print act  #na razie nie wiem co z tym zrobic, bo nie mamy ataku

    def enemy_turn(self):
        """ move enemies """
        #przeciwnicy w zasiegu wzroku
        _enemy_list = []
        for i in xrange(-self._horizon, self._horizon):  #from -3 to 3
            for j in xrange(-self._horizon, self._horizon):
                # nie puste pole
                if self._map[(self._posx+i), (self._posy+j)][2] is not None:
                    _enemy_list.append(self._map[(self._posx+i),
                                                 (self._posy+j)][2])

        # for en in _enemy_list:
            # en.move()  # not implemented

        self._myturn = True


if __name__ == '__main__':
    __TheApp__ = App()
    __TheApp__.execute()