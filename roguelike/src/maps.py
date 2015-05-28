# -*- coding: utf-8 -*-
from random import random, choice


class Map(object):
    def __init__(self, rmnum, rsize):
        #generacja mapy ŻYDOWSKĄ METODĄ
        #nie no, żartuje. Metodą Szymuna-Knutha [;
        parts_used = [(rmnum/2, rmnum/2)]
        rooms = [[(rmnum/2, rmnum/2)]]
        posible = []
        next_room = 1
        
        if rmnum != 1:
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
                if choice([True, False]):#join or new
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
        maxx = 1
        maxy = 1
        for part in parts_used:
            if part[0] > maxx:
                maxx = part[0]
            if part[1] > maxy:
                maxy = part[1]
        
        #każde pole jest listą trzyelementową: [typ_pola, przedmioty, postać]
        self.board = [[['_', None, None] for _y in xrange(rsize[1]*(maxy+1))] for _x in xrange(rsize[0]*(maxx+1))]
        for index in xrange(len(rooms)):
            for part in rooms[index]:
                for x in xrange(rsize[0]):
                    for y in xrange(rsize[1]):
                        self.board[part[0]*rsize[0]+x][part[1]*rsize[1]+y][0] = index
        self.size = (maxx+1)*rsize[0], (maxy+1)*rsize[1]
    
    def __setitem__(self, pos, item):
        #Map[x,y]
        x,y = pos
        self.board[x][y] = item

    def __getitem__(self, pos):
        #Map[x,y]
        x,y = pos
        return self.board[x][y]


class Room(object):
    def __init__(self):
        pass
