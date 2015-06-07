# -*- coding: utf-8 -*-
"""
main app
"""

import pygame
import pygame.locals as LOC
import os
from math import ceil, floor, sqrt
from random import randint
from characters import Hero
from equipment import Item, Weapon, Suit, Consumable
from maps import Map
from auxil import *
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
        self._marked = None
        self._lost  = None

        pos_x, pos_y = self.get_start_position()
        self._hero = Hero(10, 5, 10, 10, 200, pos_x, pos_y)

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

        pygame.key.set_repeat(5, 50)  #(delay, interval) in milisec
        self._lost = False

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
            if not self._lost:
                self.render()
            else:
                pygame.draw.rect(self._display_surf, (0, 0, 0), (0, 0, 810, 650))
                Auxil.write(self._display_surf, "GAME OVER", 34, 300, 240)
                pygame.display.update()

    def event(self, event):
        """
        Obsługa eventów:
            -wciśniętych klawiszy
            -muzyki
            -wyjścia z gry
        """

        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            if self._player_turn:

                if event.key == LOC.K_UP or event.key == LOC.K_w:
                    if self._hero.get_y() > 0\
                            and self._map[self._hero.get_x(),
                                          self._hero.get_y()-1][0] != '_'\
                            and self._map[self._hero.get_x(),
                                          self._hero.get_y()-1][0] != 'w':
                        self._action = 'w'
                        self._player_turn = False

                if event.key == LOC.K_DOWN or event.key == LOC.K_s:
                    if self._hero.get_y() < self._map.size[1]-1\
                            and self._map[self._hero.get_x(),
                                          self._hero.get_y()+1][0] != '_'\
                            and self._map[self._hero.get_x(),
                                          self._hero.get_y()+1][0] != 'w':
                        self._action = 's'
                        self._player_turn = False

                if event.key == LOC.K_LEFT or event.key == LOC.K_a:
                    if self._hero.get_x() > 0\
                            and self._map[self._hero.get_x()-1,
                                          self._hero.get_y()][0] != '_'\
                            and self._map[self._hero.get_x()-1,
                                          self._hero.get_y()][0] != 'w':
                        self._action = 'a'
                        self._player_turn = False

                if event.key == LOC.K_RIGHT or event.key == LOC.K_d:
                    if self._hero.get_x() < self._map.size[0]-1\
                            and self._map[self._hero.get_x()+1,
                                          self._hero.get_y()][0] != '_'\
                            and self._map[self._hero.get_x()+1,
                                          self._hero.get_y()][0] != 'w':
                        self._action = 'd'
                        self._player_turn = False

                #added picking up items
                if event.key == LOC.K_RCTRL or event.key == LOC.K_e:
                    if self._map[self._hero.get_position()][1] is not None:
                        # pick up - add to backpack
                        for item in self._map[self._hero.get_position()][1]:
                            self._hero.get_equip().add_to_backpack(item)
                        # delete item from the floor
                        self._map[self._hero.get_position()][1] = None
                        print self._hero.get_equip().get_backpack()  # debug

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
                if po_x >= 610 and po_y >= 100 and po_y <= 100+4*40:
                    (square_x, square_y) = ((po_x-610)/40, (po_y-100)/40)
                    if not self._marked == (square_x, square_y):
                        # if not already marked
                        self._marked = (square_x, square_y)
                    else:
                        # swap item with wearing
                        bp_place = square_y*5+square_x
                        if bp_place < self._hero.get_equip().backpack_len():
                            self._hero.get_equip().use_item(bp_place)
                            self._marked = None

                # mouse on lvl buttons
                if self._hero._skill_points != 0\
                    and po_x >= 780 and po_x <= 780 + 16\
                    and po_y >= 275 and po_y <= 275 + 5*16:
                    num = (po_y-275)/16
                    if num == 0:
                        self._hero.add_hp()
                    elif num == 1:
                        self._hero.add_attack()
                    elif num == 2:
                        self._hero.add_defense()
                    elif num == 3:
                        self._hero.add_strength()
                    elif num == 4:
                        self._hero.add_dexterity()

    def render(self):
        """ in prog """

        if self._hero.get_x() < 9:
            x_o = 0

        elif self._hero.get_x() > self._map.size[0]-9-1:
            x_o = self._map.size[0] - 19

        else:
            x_o = self._hero.get_x() - 9

        if self._hero.get_y() < 9:
            y_o = 0

        elif self._hero.get_y() > self._map.size[1]-9-1:
            y_o = self._map.size[1] - 19

        else:
            y_o = self._hero.get_y() - 9

        floor_list = [self._image_library["texture18.png"],
                      self._image_library["texture16.png"],
                      self._image_library["texture15.png"]]
        wall = self._image_library["texture17.png"]

        for y in xrange(19):
            for x in xrange(19):
                pos = self._map[(x_o+x), (y_o+y)]
                # ściana
                if pos[0] == 'w':
                    self._display_surf.blit(wall, (x * 32, y * 32))

                # podloga
                elif pos[0] != '_':
                    i = pos[0]
                    self._display_surf.blit(floor_list[i % 3],
                                            (x * 32, y * 32))

                # pustka
                else:
                    pygame.draw.rect(self._surface, (0, 0, 0),
                                     (x * 32, y * 32, 32, 32))

                # item
                if pos[1] is not None:

                    for item in pos[1]:
                        self._display_surf.blit(
                            self._image_library[item.get_sprite()],
                            (x * 32, y * 32)
                        )

                # hero
                if (x_o+x, y_o+y) == self._hero.get_position():
                    self._display_surf.blit(self._image_library["hero.png"],
                                            (x * 32, y * 32))

                # enemy
                if pos[2] is not None:
                    self._display_surf.blit(self._image_library[pos[2].get_sprite()],
                                            (x * 32, y * 32))

                # vision
                if not self.check_view(x_o+x, y_o+y):
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

        # nadpisuje czarnym tłem
        pygame.draw.rect(self._surface, (0, 0, 0), (610, 0, 200, 650))

        # prawa strona
        Auxil.do_nice_outlines(self._surface)
        Auxil.write(self._surface, "EQ", 22, 700, 0)
        Auxil.write(self._surface, "Backpack", 22, 660, 80)
        Auxil.write(self._surface, "Stats:", 14, 615, 240+20)
        Auxil.write(self._surface, "HP", 14, 615, 240+35)  # +15 pix pionowo
        Auxil.write(self._surface, "Attack", 14, 615, 240+50)
        Auxil.write(self._surface, "Defense", 14, 615, 240+65)
        Auxil.write(self._surface, "Strength", 14, 615, 240+80)
        Auxil.write(self._surface, "Dexterity", 14, 615, 240+95)
        Auxil.write(self._surface, "Armor", 14, 615, 240+110)
        Auxil.write(self._surface, "Exp", 14, 615, 240+125)

        #,240 + 15*i)
        Auxil.write(self._surface, str(floor(self._hero.get_hp())),
                                                                14, 690, 275)
        Auxil.write(self._surface, str(self._hero.get_attack()), 14, 690, 290)
        Auxil.write(self._surface, str(self._hero.get_defense()), 14, 690, 305)
        Auxil.write(self._surface, str(self._hero.get_strength()), 14, 690, 320)
        Auxil.write(self._surface, str(self._hero.get_dexterity()), 14, 690, 335)
        Auxil.write(self._surface, str(self._hero.get_armor().durability),
                                                                14, 690, 350)
        Auxil.write(self._surface, str(self._hero.get_exp()), 14, 690, 365)


        z = 2
        EQ = self._hero.get_equip()
        if EQ.get_weapon() is not None:
            self._display_surf.blit(
                    self._image_library[EQ.get_weapon().get_sprite()],
                    (615+z, 20+z)
                )
        if EQ.get_suit() is not None:
            self._display_surf.blit(
                    self._image_library[EQ.get_suit().get_sprite()],
                    (615+z+40, 20+z)
                )

        # backpack
        i = 0
        for item in EQ.get_backpack():
            self._display_surf.blit(
                self._image_library[item.get_sprite()],
                (615 + z + (i%5)*40, 100 + z + (i/5)*40)
            )
            i += 1

        # buttons
        if self._hero._skill_points != 0:
            for but in xrange(5):
                self._display_surf.blit(
                    self._image_library["button.png"],
                    (780, 275 + but*16)
                )

        pygame.display.update()

    def check_view(self, x, y):
        """sprawdza zasieg wzroku"""
        d = ceil(sqrt((self._hero.get_x()-x)**2 + (self._hero.get_y()-y)**2))
        return d <= HORIZON

    def load_images(self):
        """
         Chciałem to wydzielić do innego pliku, ale mi nie wyszło,
         dobrze jakby ktoś to ogarnął ~WuJo
         load images from /items """
        path = r"./items/"
        item_list = Auxil.files("items")
        self._image_library = {}

        for item in item_list:
            uni_path = path.replace('/', os.sep).replace('\\', os.sep)
            #universal path, also works: os.path.join('','')
            self._image_library[item] = pygame.image.load(uni_path + item)\
                .convert_alpha()

    def player_action(self):
        """
        Sprawdza ostatnią akcję gracza
        w zależności od tego czy nachodzimy
        atakuje lub po prostu się przemieszcza
        """

        if self._action == 'w':

            action_pos = self._map[self._hero.get_x(), self._hero.get_y()-1]
            # brak wroga
            if action_pos[2] is None:
                self._hero.change_y(-1)

            # atak
            else:
                print "gracz atakuje"
                Auxil.write(self._surface, "gracz atakuje", 14, 615, 400)
                result = self._hero.attack(action_pos[2])

                if result:
                    self._hero.gain_exp(action_pos[2].give_exp())
                    loot = action_pos[2].leave_items()

                    if loot is not None:
                        if action_pos[1] is None:
                            action_pos[1] = [loot]

                        else:
                            action_pos[1].append(loot)

                    action_pos[2] = None

        if self._action == 's':

            action_pos = self._map[self._hero.get_x(), self._hero.get_y()+1]
            if action_pos[2] is None:
                self._hero.change_y(1)

            else:
                print "gracz atakuje"
                Auxil.write(self._surface, "gracz atakuje", 14, 615, 400)
                result = self._hero.attack(action_pos[2])

                if result:
                    self._hero.gain_exp(action_pos[2].give_exp())
                    loot = action_pos[2].leave_items()

                    if loot is not None:
                        if action_pos[1] is None:
                            action_pos[1] = [loot]

                        else:
                            action_pos[1].append(loot)

                    action_pos[2] = None

        if self._action == 'a':

            action_pos = self._map[self._hero.get_x()-1, self._hero.get_y()]
            if action_pos[2] is None:
                self._hero.change_x(-1)

            else:
                print "gracz atakuje"
                Auxil.write(self._surface, "gracz atakuje", 14, 615, 400)
                result = self._hero.attack(action_pos[2])

                if result:
                    self._hero.gain_exp(action_pos[2].give_exp())
                    loot = action_pos[2].leave_items()
                    if loot is not None:
                        if action_pos[1] is None:
                            action_pos[1] = [loot]

                        else:
                            action_pos[1].append(loot)

                    action_pos[2] = None

        if self._action == 'd':

            action_pos = self._map[self._hero.get_x()+1, self._hero.get_y()]
            if action_pos[2] is None:
                self._hero.change_x(1)

            else:
                print "gracz atakuje"
                Auxil.write(self._surface, "gracz atakuje", 14, 615, 400)
                result = self._hero.attack(action_pos[2])

                if result:
                    self._hero.gain_exp(action_pos[2].give_exp())
                    loot = action_pos[2].leave_items()

                    if loot is not None:

                        if action_pos[1] is None:
                            action_pos[1] = [loot]

                        else:
                            action_pos[1].append(loot)

                    action_pos[2] = None

    def enemy_turn(self):
        """
        Symulacja tury przeciwników.
        W praktyce poruszają się tylko ci w zasięgu naszego wzroku
        """

        enemy_list = []

        # szukamy przeciwników w zasięgu wzroku
        hero_x = self._hero.get_x()
        hero_y = self._hero.get_y()
        for i in xrange(-HORIZON, HORIZON):
            for j in xrange(-HORIZON, HORIZON):
                if not (not (hero_x + i >= 0)
                        or not (hero_x + j >= 0)
                        or not (hero_x + i < self._map.size[0])
                        or not (hero_y + j < self._map.size[1])
                        or not (self._map[(hero_x + i),
                                          (hero_y + j)][2] is not None)):
                    enemy_list.append(self._map[(hero_x+i),
                                                (hero_y+j)][2])

        # to tylko tymczasowo do debugu:
        if len(enemy_list) > 0: # jak pusta to po co pisac?
            print "w poblizu mamy: ", enemy_list

        # ruszamy enemy
        for enemy in enemy_list:

            x_enemy, y_enemy = enemy.get_position()

            x_distance = hero_x - x_enemy
            y_distance = hero_y - y_enemy

            # ruszamy się po manhatanie, próbujemy po dłuższej odległości

            if abs(x_distance) > abs(y_distance):

                if (x_distance > 1 or
                    (x_distance == 1 and abs(y_distance) == 1))\
                        and self._map[x_enemy+1, y_enemy][2] is None\
                        and self._map[x_enemy+1, y_enemy][0] != 'w'\
                        and self._map[x_enemy+1, y_enemy][0] != '_':
                    enemy.change_position((x_enemy+1, y_enemy))
                    self._map[x_enemy, y_enemy][2] = None
                    self._map[x_enemy+1, y_enemy][2] = enemy

                elif (x_distance < -1 or
                      (x_distance == -1 and abs(y_distance) == 1))\
                        and self._map[x_enemy-1, y_enemy][2] is None\
                        and self._map[x_enemy-1, y_enemy][0] != 'w'\
                        and self._map[x_enemy-1, y_enemy][0] != '_':
                    enemy.change_position((x_enemy-1, y_enemy))
                    self._map[x_enemy, y_enemy][2] = None
                    self._map[x_enemy-1, y_enemy][2] = enemy

            else:

                if (y_distance > 1 or
                    (y_distance == 1 and abs(x_distance) == 1))\
                        and self._map[x_enemy, y_enemy+1][2] is None\
                        and self._map[x_enemy, y_enemy+1][0] != 'w'\
                        and self._map[x_enemy, y_enemy+1][0] != '_':
                    enemy.change_position((x_enemy, y_enemy+1))
                    self._map[x_enemy, y_enemy][2] = None
                    self._map[x_enemy, y_enemy+1][2] = enemy

                elif (y_distance < -1 or
                      (y_distance == -1 and abs(x_distance) == 1))\
                        and self._map[x_enemy, y_enemy-1][2] is None\
                        and self._map[x_enemy, y_enemy-1][0] != 'w'\
                        and self._map[x_enemy, y_enemy-1][0] != '_':
                    enemy.change_position((x_enemy, y_enemy-1))
                    self._map[x_enemy, y_enemy][2] = None
                    self._map[x_enemy, y_enemy-1][2] = enemy

            # sprawdzamy czy można zaatakować i ewentualnie atakujemy:
            x_distance = hero_x - enemy.get_x()
            y_distance = hero_y - enemy.get_y()

            if abs(x_distance) == 1 and y_distance == 0 \
                    or x_distance == 0 and abs(y_distance) == 1:
                print "potworek atakuje"
                Auxil.write(self._surface, "potwor atakuje", 14, 615, 240+130)

                self._lost = enemy.attack(self._hero)

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
