# -*- coding: utf-8 -*-
"""
Moduł odpowiedzielany za losowe generowanie mapy
"""
from random import random, choice
# from auxil import Damage, Armor
from characters import get_random_enemy
from copy import deepcopy


class Map(object):
    """klasa reprezentująca mapę oraz wszystko co się na niej znajduje"""
    def __init__(self, rooms_number, room_size):
        """
        Generacja mapy:
        1.Wybieramy pewien element początkowy który staje się pierwszym pokojem
        2.Tworzymy zbiór przyległych elementów...
        3.... z którego losujemy kolejny element
        4.Decydujemy czy ma być to nowy pokój czy fragment obecnego pokoju
        5.Dodajemy do zbioru nowe przyległe elementy
        6.Odrzucam ze zbioru jeden element
            (daje to większą różnorodność wyników)
        7.Jeżeli nie mamy jeszcze docelowej liczby pokoi wracamy do punktu 3.
        8.Tworzymy tablicę odpowiednich rozmiarów, na której wypisujemy planszę
            z odpowiednimi szczegółami
        9.Dla każdego pokoju losujemy góra dwa elementy,
            z których tworzymy przejścia
        """

        parts_used = [(rooms_number/2, rooms_number/2)]  # wszystkie użyte części
        self._rooms = [Room((rooms_number/2, rooms_number/2))]
        possible = []
        next_room = 1

        # możliwe stają się przyległe pola
        if rooms_number != 1:
            possible.append((rooms_number/2-1, rooms_number/2))
            possible.append((rooms_number/2, rooms_number/2-1))
            possible.append((rooms_number/2+1, rooms_number/2))
            possible.append((rooms_number/2, rooms_number/2+1))

        while next_room < rooms_number and len(parts_used) < rooms_number ** 2:
            new = choice(possible)
            possible.remove(new)
            if new not in parts_used:
                close_parts = [(new[0]-1, new[1]), (new[0], new[1]-1),
                               (new[0]+1, new[1]), (new[0], new[1]+1)]

                if random() > 0.60:#join or new
                    for room in self._rooms:
                        if any(i in room.parts for i in close_parts):
                            room.append(new)
                            break

                else:
                    self._rooms.append(Room(new))
                    next_room += 1

                possible.remove(choice(possible))
                parts_used.append(new)

                for part in close_parts:
                    if part not in parts_used:
                        possible.append(part)

        # "obcinamy" puste boki
        max_x = 1
        max_y = 1
        min_x = rooms_number
        min_y = rooms_number

        for part in parts_used:

            if part[0] < min_x:
                min_x = part[0]

            if part[1] < min_y:
                min_y = part[1]

            if part[0] > max_x:
                max_x = part[0]

            if part[1] > max_y:
                max_y = part[1]

        # każde pole jest listą trzyelementową: [typ_pola, przedmioty, postać]
        self.board = [
            [['_', None, None]
             for _ in xrange(room_size[1]*min_y, room_size[1]*(max_y+1)+1)]
            for _ in xrange(room_size[0]*min_x, room_size[0]*(max_x+1)+1)
        ]

        for index in xrange(len(self._rooms)):
            for part in self._rooms[index].parts:
                for x in xrange(room_size[0]):
                    for y in xrange(room_size[1]):
                        temp_x = (part[0]-min_x)*room_size[0]+x
                        temp_y = (part[1]-min_y)*room_size[1]+y
                        #sprawdzamy czy na krawędzi = sciana
                        if (x == 0 and ((part[0]-1, part[1])
                                not in self._rooms[index].parts))\
                            or (x == room_size[0]-1 and ((part[0]+1, part[1])\
                                not in self._rooms[index].parts))\
                            or (y == 0 and ((part[0], part[1]-1)\
                                not in self._rooms[index].parts))\
                            or (y == room_size[1]-1 and ((part[0], part[1]+1)\
                                not in self._rooms[index].parts)):
                            self.board[temp_x][temp_y][0] = 'w'

                        else:
                            self.board[temp_x][temp_y][0] = index
                            if random() > 0.97:
                                self.board[temp_x][temp_y][2]\
                                    = deepcopy(get_random_enemy())
                                self.board[temp_x][temp_y][2]\
                                    .change_position((temp_x, temp_y))
                            elif random() > 0.995:
                                self.board[temp_x][temp_y][2] = "rf"

        self._size = (max_x+1-min_x)*room_size[0], (max_y+1-min_y)*room_size[1]

        # drogi
        ways = []

        for room in self._rooms:
            chosen_part = choice(room.parts)

            if (chosen_part[0]-1, chosen_part[1]) not in room.parts\
                    and (chosen_part[0]-1, chosen_part[1]) in parts_used:
                room.make_way(chosen_part, (chosen_part[0]-1, chosen_part[1]))
                ways.append((chosen_part, (chosen_part[0]-1, chosen_part[1])))

            if (chosen_part[0]+1, chosen_part[1]) not in room.parts\
                    and (chosen_part[0]+1, chosen_part[1]) in parts_used:
                room.make_way(chosen_part, (chosen_part[0]+1, chosen_part[1]))
                ways.append((chosen_part, (chosen_part[0]+1, chosen_part[1])))

            if (chosen_part[0], chosen_part[1]-1) not in room.parts\
                    and (chosen_part[0], chosen_part[1]-1) in parts_used:
                room.make_way(chosen_part, (chosen_part[0], chosen_part[1]-1))
                ways.append((chosen_part, (chosen_part[0], chosen_part[1]-1)))

            if (chosen_part[0], chosen_part[1]+1) not in room.parts\
                    and (chosen_part[0], chosen_part[1]+1) in parts_used:
                room.make_way(chosen_part, (chosen_part[0], chosen_part[1]+1))
                ways.append((chosen_part, (chosen_part[0], chosen_part[1]+1)))

            if len(room.parts) > 1:

                chosen_part = choice(room.parts)

                if (chosen_part[0]-1, chosen_part[1]) not in room.parts\
                        and (chosen_part[0]-1, chosen_part[1]) in parts_used:
                    room.make_way(chosen_part,
                                  (chosen_part[0]-1, chosen_part[1]))
                    ways.append((chosen_part,
                                 (chosen_part[0]-1, chosen_part[1])))

                if (chosen_part[0]+1, chosen_part[1]) not in room.parts\
                        and (chosen_part[0]+1, chosen_part[1]) in parts_used:
                    room.make_way(chosen_part,
                                  (chosen_part[0]+1, chosen_part[1]))
                    ways.append((chosen_part,
                                 (chosen_part[0]+1, chosen_part[1])))

                if (chosen_part[0], chosen_part[1]-1) not in room.parts\
                        and (chosen_part[0], chosen_part[1]-1) in parts_used:
                    room.make_way(chosen_part,
                                  (chosen_part[0], chosen_part[1]-1))
                    ways.append((chosen_part,
                                 (chosen_part[0], chosen_part[1]-1)))

                if (chosen_part[0], chosen_part[1]+1) not in room.parts\
                        and (chosen_part[0], chosen_part[1]+1) in parts_used:
                    room.make_way(chosen_part,
                                  (chosen_part[0], chosen_part[1]+1))
                    ways.append((chosen_part,
                                 (chosen_part[0], chosen_part[1]+1)))

        for way in ways:
            if way[0][0] == way[1][0] and way[0][1] < way[1][1]:
                self.board[(way[0][0]-min_x)*room_size[0]+(room_size[0]/2)]\
                    [(way[0][1]-min_y)*room_size[1]+room_size[1]-1][0] = 1
                self.board[(way[1][0]-min_x)*room_size[0]+(room_size[0]/2)]\
                    [(way[1][1]-min_y)*room_size[1]][0] = 1
                self.board[(way[0][0]-min_x)*room_size[0]+(room_size[0]/2)-1]\
                    [(way[0][1]-min_y)*room_size[1]+room_size[1]-1][0] = 1
                self.board[(way[1][0]-min_x)*room_size[0]+(room_size[0]/2)-1]\
                    [(way[1][1]-min_y)*room_size[1]][0] = 1

            if way[0][0] == way[1][0] and way[0][1] > way[1][1]:
                self.board[(way[0][0]-min_x)*room_size[0]+(room_size[0]/2)]\
                    [(way[0][1]-min_y)*room_size[1]][0] = 1
                self.board[(way[1][0]-min_x)*room_size[0]+(room_size[0]/2)]\
                    [(way[1][1]-min_y)*room_size[1] + room_size[1]-1][0] = 1
                self.board[(way[0][0]-min_x)*room_size[0]+(room_size[0]/2)-1]\
                    [(way[0][1]-min_y)*room_size[1]][0] = 1
                self.board[(way[1][0]-min_x)*room_size[0]+(room_size[0]/2)-1]\
                    [(way[1][1]-min_y)*room_size[1] + room_size[1]-1][0] = 1

            if way[0][1] == way[1][1] and way[0][0] < way[1][0]:
                self.board[(way[0][0]-min_x)*room_size[0]+room_size[1]-1]\
                    [(way[0][1]-min_y)*room_size[1]+(room_size[0]/2)][0] = 1
                self.board[(way[1][0]-min_x)*room_size[0]]\
                    [(way[1][1]-min_y)*room_size[1]+(room_size[0]/2)][0] = 1
                self.board[(way[0][0]-min_x)*room_size[0]+room_size[1]-1]\
                    [(way[0][1]-min_y)*room_size[1]+(room_size[0]/2)-1][0] = 1
                self.board[(way[1][0]-min_x)*room_size[0]]\
                    [(way[1][1]-min_y)*room_size[1]+(room_size[0]/2)-1][0] = 1

            if way[0][1] == way[1][1] and way[0][1] > way[1][0]:
                self.board[(way[0][0]-min_x)*room_size[0]]\
                    [(way[0][1]-min_y)*room_size[1]+(room_size[0]/2)][0] = 1
                self.board[(way[1][0]-min_x)*room_size[0]+room_size[1]-1]\
                    [(way[1][1]-min_y)*room_size[1]+(room_size[0]/2)][0] = 1
                self.board[(way[0][0]-min_x)*room_size[0]]\
                    [(way[0][1]-min_y)*room_size[1]+(room_size[0]/2)-1][0] = 1
                self.board[(way[1][0]-min_x)*room_size[0]+room_size[1]-1]\
                    [(way[1][1]-min_y)*room_size[1]+(room_size[0]/2)-1][0] = 1

    def __setitem__(self, pos, item):
        x, y = pos
        self.board[x][y] = item

    def __getitem__(self, pos):
        x, y = pos
        return self.board[x][y]
    
    @property
    def size(self):
        """zwraca rozmiar mapy - parę"""
        return self._size
    
    @property
    def rooms(self):
        """zwraca listę pokoi"""
        return self._size


class Room(object):
    """Reprezentuje pojedyńczy pokój"""

    def __init__(self, first_part):
        self._parts = [first_part]
        self._ways = []

    @property
    def parts(self):
        """zwraca listę części"""
        return self._parts

    @property
    def ways(self):
        """zwraca listę ścieżek"""
        return self._ways

    def append(self, part):
        """dodaje element do pokoju"""
        self._parts.append(part)

    def make_way(self, from_part, to_part):
        """tworzy ścieżkę z elementu do elementu"""
        self._ways.append((from_part, to_part))
