# -*- coding: utf-8 -*-
"""
main app
"""

import pygame
import pygame.locals as LOC
import os
import math
from random import randint
from characters import *
from equipment import Item, Weapon, Suit
from maps import Map
from aux import Aux
from music import Music

HORIZON = 4  # stała zasięgu
MUSIC = Music()


class App(object):
    """ doc """

    def __init__(self):
        """ s """
        self._running = None
        self._surface = None
        self._size = self.weight, self.height = 810, 650
        self._map = Map(50, (10, 10))  #rmnum, rsize
        self._player_turn = None
        self._display_surf = None
        self._image_library = None
        self._action = None
        self._marked = (None, None)

        pos_x, pos_y = self.get_start_position()
        self._hero = Hero(0, 0, 10, 10,
                          Damage(1.0, 1.0, 15, 10),
                          Armor(0.0, 0),
                          100, pos_x, pos_y)

    def init(self):
        """ s """
        pygame.init()
        pygame.display.set_caption('Rogal')
        self._surface = pygame.display.set_mode(self._size)
        self._running = True
        self._display_surf = pygame.display.set_mode(self._size,
                                                     pygame.HWSURFACE)
        self.load_images()
        MUSIC.load_music()
        MUSIC.play_music()

        Aux.do_nice_outlines(self._surface)
        pygame.key.set_repeat(5, 50)  #(delay, interval) in milisec

        Aux.write(self._surface, "EQ", 22, 700, 0)
        Aux.write(self._surface, "Stats:", 14, 615, 240+20)
        Aux.write(self._surface, "HP", 14, 615, 240+35)  # +15 pix pionowo
        Aux.write(self._surface, "Attack", 14, 615, 240+50)
        Aux.write(self._surface, "Defense", 14, 615, 240+65)
        Aux.write(self._surface, "Armor", 14, 615, 240+80)

    def execute(self):
        """ s """

        self.init()
        self._player_turn = True

        while self._running:

            for event in pygame.event.get():
                self.event(event)

            # wykonaj przechwycona akcje
            if not self._player_turn:
                self.player_action()
                self.enemy_turn()

            self.render()

    def event(self, event):
        """Obsługa eventów:
            -wciśniętych klawiszy
            -muzyki
            -wyjścia z gry
        """
        #alternative?
        # pressedkeys = pygame.key.get_pressed()
        # if pressedkeys[pygame.K_x]:

        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            if self._player_turn:

                if event.key == LOC.K_UP or event.key == LOC.K_w:
                    if self._hero.get_y() > 0\
                            and self._map[self._hero.get_x(), self._hero.get_y()-1][0] != '_'\
                            and self._map[self._hero.get_x(), self._hero.get_y()-1][0] != 'w':
                        self._action = 'w'
                        self._player_turn = False

                if event.key == LOC.K_DOWN or event.key == LOC.K_s:
                    if self._hero.get_y() < self._map.size[1]-1\
                            and self._map[self._hero.get_x(), self._hero.get_y()+1][0] != '_'\
                            and self._map[self._hero.get_x(), self._hero.get_y()+1][0] != 'w':
                        self._action = 's'
                        self._player_turn = False

                if event.key == LOC.K_LEFT or event.key == LOC.K_a:
                    if self._hero.get_x() > 0\
                            and self._map[self._hero.get_x()-1, self._hero.get_y()][0] != '_'\
                            and self._map[self._hero.get_x()-1, self._hero.get_y()][0] != 'w':
                        self._action = 'a'
                        self._player_turn = False

                if event.key == LOC.K_RIGHT or event.key == LOC.K_d:
                    if self._hero.get_x() < self._map.size[0]-1\
                            and self._map[self._hero.get_x()+1, self._hero.get_y()][0] != '_'\
                            and self._map[self._hero.get_x()+1, self._hero.get_y()][0] != 'w':
                        self._action = 'd'
                        self._player_turn = False

            if event.key == LOC.K_ESCAPE:  #quit
                self._running = False

            if event.key == LOC.K_m:  #volume up
                if MUSIC.volume <= 1:
                    MUSIC.volume += 0.05
                    pygame.mixer.music.set_volume(MUSIC.volume)

            if event.key == LOC.K_n:  #volume down
                if MUSIC.volume >= 0:
                    MUSIC.volume -= 0.05
                    pygame.mixer.music.set_volume(MUSIC.volume)

        if event.type == pygame.USEREVENT + 1:
            print(MUSIC.song_num, "song ended")
            MUSIC.play_music()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                po_x, po_y = pygame.mouse.get_pos()
                # mouse pointer in the equipment zone
                if po_x >= 610 and po_y >= 20 and po_y <= 20+6*40:
                    (square_x, square_y) = ((po_x-610)/40, (po_y-20)/40)
                    if not self._marked == (square_x, square_y): 
                        # if not already marked
                        self._marked = (square_x, square_y)
                    else:
                        # swap item with wearing
                        pass

    def render(self):
        """ in prog """

        side_box = 9

        if self._hero.get_x() < side_box:
            x_o = 0

        elif self._hero.get_x() > self._map.size[0]-side_box-1:
            x_o = self._map.size[0] - (2*side_box+1)

        else:
            x_o = self._hero.get_x() - side_box

        if self._hero.get_y() < side_box:
            y_o = 0

        elif self._hero.get_y() > self._map.size[1]-side_box-1:
            y_o = self._map.size[1] - (2*side_box+1)

        else:
            y_o = self._hero.get_y() - side_box

        floor_list = [self._image_library["texture18.png"],
                      self._image_library["texture16.png"],
                      self._image_library["texture15.png"]]
            
        for y in xrange(19):
            for x in xrange(19):

                # ściana
                if self._map[(x_o+x), (y_o+y)][0] == 'w':
                    self._display_surf.blit(self._image_library["texture17.png"],
                                            (x * 32, y * 32))

                # podloga
                elif self._map[(x_o+x), (y_o+y)][0] != '_':
                    i = self._map[(x_o+x), (y_o+y)][0]
                    self._display_surf.blit(floor_list[i % 3],
                                            (x * 32, y * 32))

                # pustka
                else:
                    # self._display_surf.blit(self.wall, (x * 32, y * 32))
                    pygame.draw.rect(self._surface, (0, 0, 0),
                                     (x * 32, y * 32, 32, 32))
                
                # item
                if self._map[(x_o+x), (y_o+y)][1] is not None:

                    for item in self._map[(x_o+x), (y_o+y)][1]:

                        if type(item) is Weapon:
                            self._display_surf.blit(
                                self._image_library["weapon3.png"],
                                (x * 32, y * 32)
                            )

                        elif type(item) is Suit:
                            self._display_surf.blit(
                                self._image_library["ar2.png"],
                                (x * 32, y * 32)
                            )

                        else:
                            self._display_surf.blit(
                                self._image_library["weapon6.png"],
                                (x * 32, y * 32)
                            )
                
                # hero
                if (x_o+x, y_o+y) == self._hero.get_position():
                    self._display_surf.blit(self._image_library["photo.jpg"],
                                            (x * 32, y * 32))

                # enemy
                if self._map[(x_o+x), (y_o+y)][2] is not None:
                    self._display_surf.blit(self._image_library["enemy1.png"],
                                            (x * 32, y * 32))

                # vision
                if not self.check_horizon(x_o+x, y_o+y):
                    # (abs(x_o+x - self._posx) <= self._horizon
                    # and abs(y_o+y - self._posy) <= self._horizon):
                    self._display_surf.blit(self._image_library["black.png"],
                                            (x * 32, y * 32))

        # volume visual
        self._display_surf.blit(self._image_library["speaker.png"], (0, 612))
        light_straps = (0, 96, 0)
        dark_straps = (0, 32, 0)
        wid = 5

        for strap in xrange(20):

            if strap < MUSIC.volume*20:
                pygame.draw.rect(self._surface, light_straps,
                                 (20+strap*wid, 650-strap*2, wid-1, strap*2))

            else:
                pygame.draw.rect(self._surface, dark_straps,
                                 (20+strap*wid, 650-strap*2, wid-1, strap*2))

        pygame.display.update()

        Aux.write(self._surface, str(self._hero.get_hp()), 14, 675, 240+35)
        Aux.write(self._surface, str(self._hero.get_attack()), 14, 675, 240+50)
        Aux.write(self._surface, str(self._hero.get_defense()), 14, 675, 240+65)
        Aux.write(self._surface, str(self._hero.get_armor()), 14, 675, 240+80)

    def check_horizon(self, x, y):
        """sprawdza choryzont?! XD"""
        d = math.ceil(math.sqrt((self._hero.get_x()-x)**2 + (self._hero.get_y()-y)**2))
        return d <= HORIZON

    def load_images(self):
        """
         Chciałem to wydzielić do innego pliku, ale mi nie wyszło,
         dobrze jakby ktoś to ogarnął ~WuJo
         load images from /items """
        path = r"./items/"
        item_list = Aux.files("items")
        self._image_library = {}

        for item in item_list:
            uni_path = path.replace('/', os.sep).replace('\\', os.sep)
            #universal path, also works: os.path.join('','')
            self._image_library[item] = pygame.image.load(uni_path + item)\
                .convert_alpha()

    def player_action(self):
        """Sprawdza ostatnią akcję gracza i w zależności od tego czy nachodzimy na wroga atakuje
        lub po prostu się przemieszcza"""

        if self._action == 'w':

            # brak wroga
            if self._map[self._hero.get_x(), self._hero.get_y()-1][2] is None:
                self._hero.change_y(-1)

            # atak
            else:
                print "gracz atakuje"
                result = self._hero.attack(self._map[self._hero.get_x(), self._hero.get_y()-1][2])

                if result:
                    loot = self._map[self._hero.get_x(), self._hero.get_y()-1][2].leave_items()

                    if loot is not None:
                        if self._map[self._hero.get_x(), self._hero.get_y()-1][1] is None:
                            self._map[self._hero.get_x(), self._hero.get_y()-1][1] = [loot]

                        else:
                            self._map[self._hero.get_x(), self._hero.get_y()-1][1].append(loot)

                    self._map[self._hero.get_x(), self._hero.get_y()-1][2] = None

        if self._action == 's':

            if self._map[self._hero.get_x(), self._hero.get_y()+1][2] is None:
                self._hero.change_y(1)

            else:
                print "gracz atakuje"
                result = self._hero.attack(self._map[self._hero.get_x(), self._hero.get_y()+1][2])

                if result:
                    loot = self._map[self._hero.get_x(), self._hero.get_y()+1][2].leave_items()

                    if loot is not None:
                        if self._map[self._hero.get_x(), self._hero.get_y()+1][1] is None:
                            self._map[self._hero.get_x(), self._hero.get_y()+1][1] = [loot]

                        else:
                            self._map[self._hero.get_x(), self._hero.get_y()+1][1].append(loot)

                    self._map[self._hero.get_x(), self._hero.get_y()+1][2] = None

        if self._action == 'a':

            if self._map[self._hero.get_x()-1, self._hero.get_y()][2] is None:
                self._hero.change_x(-1)

            else:
                print "gracz atakuje"
                result = self._hero.attack(self._map[self._hero.get_x()-1, self._hero.get_y()][2])

                if result:
                    loot = self._map[self._hero.get_x()-1, self._hero.get_y()][2].leave_items()
                    if loot is not None:
                        if self._map[self._hero.get_x()-1, self._hero.get_y()][1] is None:
                            self._map[self._hero.get_x()-1, self._hero.get_y()][1] = [loot]

                        else:
                            self._map[self._hero.get_x()-1, self._hero.get_y()][1].append(loot)

                    self._map[self._hero.get_x()-1, self._hero.get_y()][2] = None

        if self._action == 'd':

            if self._map[self._hero.get_x()+1, self._hero.get_y()][2] is None:
                self._hero.change_x(1)

            else:
                print "gracz atakuje"
                result = self._hero.attack(self._map[self._hero.get_x()+1, self._hero.get_y()][2])

                if result:
                    loot = self._map[self._hero.get_x()+1, self._hero.get_y()][2].leave_items()

                    if loot is not None:

                        if self._map[self._hero.get_x()+1, self._hero.get_y()][1] is None:
                            self._map[self._hero.get_x()+1, self._hero.get_y()][1] = [loot]

                        else:
                            self._map[self._hero.get_x()+1, self._hero.get_y()][1].append(loot)

                    self._map[self._hero.get_x()+1, self._hero.get_y()][2] = None

    def enemy_turn(self):
        """symulacja tury przeciwników, w praktyce poruszają się tylko ci w zasięgu naszego wzroku"""

        enemy_list = []

        # szukamy przeciwników w zasięgu wzroku
        for i in xrange(-HORIZON, HORIZON):
            for j in xrange(-HORIZON, HORIZON):
                if not (not (self._hero.get_x() + i >= 0)
                        or not (self._hero.get_x() + j >= 0)
                        or not (self._hero.get_x() + i < self._map.size[0])
                        or not (self._hero.get_y() + j < self._map.size[1])
                        or not (self._map[(self._hero.get_x() + i),
                                          (self._hero.get_y() + j)][2] is not None)):
                    enemy_list.append(self._map[(self._hero.get_x()+i),
                                                (self._hero.get_y()+j)][2])

        # to tylko tymczasowo do debugu:
        print "w poblizu mamy: ", enemy_list

        # ruszamy enemy
        for enemy in enemy_list:

            x_enemy, y_enemy = enemy.get_position()

            x_distance = self._hero.get_x() - x_enemy
            y_distance = self._hero.get_y() - y_enemy

            # ruszamy się po manhatanie, próbujemy po dłuższej odległości

            if abs(x_distance) > abs(y_distance):

                if (x_distance > 1 or (x_distance == 1 and abs(y_distance) == 1))\
                        and self._map[x_enemy+1, y_enemy][2] is None\
                        and self._map[x_enemy+1, y_enemy][0] != 'w'\
                        and self._map[x_enemy+1, y_enemy][0] != '_':
                    enemy.change_position((x_enemy+1, y_enemy))
                    self._map[x_enemy, y_enemy][2] = None
                    self._map[x_enemy+1, y_enemy][2] = enemy

                elif (x_distance < -1 or (x_distance == -1 and abs(y_distance) == 1))\
                        and self._map[x_enemy-1, y_enemy][2] is None\
                        and self._map[x_enemy-1, y_enemy][0] != 'w'\
                        and self._map[x_enemy-1, y_enemy][0] != '_':
                    enemy.change_position((x_enemy-1, y_enemy))
                    self._map[x_enemy, y_enemy][2] = None
                    self._map[x_enemy-1, y_enemy][2] = enemy

            else:

                if (y_distance > 1 or (y_distance == 1 and abs(x_distance) == 1))\
                        and self._map[x_enemy, y_enemy+1][2] is None\
                        and self._map[x_enemy, y_enemy+1][0] != 'w'\
                        and self._map[x_enemy, y_enemy+1][0] != '_':
                    enemy.change_position((x_enemy, y_enemy+1))
                    self._map[x_enemy, y_enemy][2] = None
                    self._map[x_enemy, y_enemy+1][2] = enemy

                elif (y_distance < -1 or (y_distance == -1 and abs(x_distance) == 1))\
                        and self._map[x_enemy, y_enemy-1][2] is None\
                        and self._map[x_enemy, y_enemy-1][0] != 'w'\
                        and self._map[x_enemy, y_enemy-1][0] != '_':
                    enemy.change_position((x_enemy, y_enemy-1))
                    self._map[x_enemy, y_enemy][2] = None
                    self._map[x_enemy, y_enemy-1][2] = enemy

            # sprawdzamy czy można zaatakować i ewentualnie atakujemy:
            x_distance = self._hero.get_x() - enemy.get_x()
            y_distance = self._hero.get_y() - enemy.get_y()

            if abs(x_distance) == 1 and y_distance == 0 \
                    or x_distance == 0 and abs(y_distance) == 1:
                print "potworek atakuje gracza"
                enemy.attack(self._hero)

        self._player_turn = True

    def get_start_position(self):
        """Zwraca prawidłową, losową pozycję startową dla naszego bohatera"""

        map_size = self._map.get_size()
        x = randint(0, map_size[0]-1)
        y = randint(0, map_size[1]-1)

        while self._map[x, y][0] == 'w' \
                or self._map[x, y][0] == '_' \
                or self._map[x, y][2] is not None:
            x = randint(0, map_size[0]-1)
            y = randint(0, map_size[1]-1)

        return x, y


if __name__ == '__main__':
    __TheApp__ = App()
    __TheApp__.execute()
