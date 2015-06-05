# -*- coding: utf-8 -*-
from random import random, choice
import characters as ch


class Map(object):
    def __init__(self, rmnum, rsize):
        #generacja mapy
        parts_used = [(rmnum/2, rmnum/2)] #wszystkie użyte części
        rooms = [[(rmnum/2, rmnum/2)]] #jeszcze nie zmieniam na klasę Room, bo trzeba ją dokończyć. W tej chwili da to więcej kłopotów niż korzyści
        posible = []
        next_room = 1
        
        if rmnum != 1: #możliwe stają się przyległe pola
            posible.append((rmnum/2-1, rmnum/2))
            posible.append((rmnum/2, rmnum/2-1))
            posible.append((rmnum/2+1, rmnum/2))
            posible.append((rmnum/2, rmnum/2+1))
        
        while next_room < rmnum and len(parts_used) < rmnum ** 2:
            new = choice(posible)
            posible.remove(new)
            if new not in parts_used:
                close_parts = [(new[0]-1, new[1]), (new[0], new[1]-1),
                              (new[0]+1, new[1]), (new[0], new[1]+1)]
                if random() > 0.75:#choice([True, False]):#join or new (teraz nowe, nierówne prawdopodobieństwo ;])
                    for room in rooms:
                        if any(i in room for i in close_parts):
                            room.append(new)
                            break
                else:
                    rooms.append([new])
                    next_room += 1
                posible.remove(choice(posible))
                parts_used.append(new)
                for part in close_parts:
                    if part not in parts_used:
                        posible.append(part)
        #"obcinamy" puste boki
        maxx = 1
        maxy = 1
        minx = rmnum
        miny = rmnum
        for part in parts_used:
            if part[0] < minx:
                minx = part[0]
            if part[1] < maxy:
                miny = part[1]
            if part[0] > maxx:
                maxx = part[0]
            if part[1] > maxy:
                maxy = part[1]
        
        #każde pole jest listą trzyelementową: [typ_pola, przedmioty, postać]
        self.board = [[['_', None, None] for _y in xrange(rsize[1]*miny, rsize[1]*(maxy+1))] for _x in xrange(rsize[0]*minx, rsize[0]*(maxx+1))]
        for index in xrange(len(rooms)):
            for part in rooms[index]:
                for x in xrange(rsize[0]):
                    for y in xrange(rsize[1]):
                        self.board[(part[0]-minx)*rsize[0]+x][(part[1]-miny)*rsize[1]+y][0] = index
                        if random() > 0.95:
                             self.board[(part[0]-minx)*rsize[0]+x][(part[1]-miny)*rsize[1]+y][2] = ch.Enemy(10, 10, ch.Damage(1.0, 1.0, 10, 5), ch.Armor(0.5, 10), 15, (part[0]-minx)*rsize[0]+x, (part[1]-miny)*rsize[1]+y) 
        self.size = (maxx+1)*rsize[0]-rsize[0]*minx, (maxy+1)*rsize[1]-rsize[1]*miny
    
    def __setitem__(self, pos, item):
        #Map[x,y]
        x, y = pos
        self.board[x][y] = item

    def __getitem__(self, pos):
        #Map[x,y]
        x, y = pos
        return self.board[x][y]
    
    def get_size(self):
        return self.size


class Room(object):
    def __init__(self, first_part):
        self._parts = [first_part]
        self._ways = []
        
    def add_part(self, part):
        self._parts.append(part)
    
    def make_way(self, from_part, to_part, of_room):#trochę przekombinowane ale pracuje nad tym
        self._ways.append((from_part, to_part, of_room))
