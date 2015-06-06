# -*- coding: utf-8 -*-
"""
Moduł odpowiedzielany za losowe generowanie mapy
"""
from random import random, choice
from aux import Damage, Armor
from characters import Enemy


class Map(object):
    def __init__(self, rmnum, rsize):
        """Generacja mapy"""
        parts_used = [(rmnum/2, rmnum/2)] #wszystkie użyte części
        rooms = [Room((rmnum/2, rmnum/2))]
        possible = []
        next_room = 1
        
        if rmnum != 1: #możliwe stają się przyległe pola
            possible.append((rmnum/2-1, rmnum/2))
            possible.append((rmnum/2, rmnum/2-1))
            possible.append((rmnum/2+1, rmnum/2))
            possible.append((rmnum/2, rmnum/2+1))
        
        while next_room < rmnum and len(parts_used) < rmnum ** 2:
            new = choice(possible)
            possible.remove(new)
            if new not in parts_used:
                close_parts = [(new[0]-1, new[1]), (new[0], new[1]-1),
                               (new[0]+1, new[1]), (new[0], new[1]+1)]
                if random() > 0.60:#join or new
                    for room in rooms:
                        if any(i in room.get_parts() for i in close_parts):
                            room.append(new)
                            break
                else:
                    rooms.append(Room(new))
                    next_room += 1
                possible.remove(choice(possible))
                parts_used.append(new)
                for part in close_parts:
                    if part not in parts_used:
                        possible.append(part)
        #"obcinamy" puste boki
        maxx = 1
        maxy = 1
        minx = rmnum
        miny = rmnum
        for part in parts_used:
            if part[0] < minx:
                minx = part[0]
            if part[1] < miny:
                miny = part[1]
            if part[0] > maxx:
                maxx = part[0]
            if part[1] > maxy:
                maxy = part[1]
        
        #każde pole jest listą trzyelementową: [typ_pola, przedmioty, postać]
        self.board = [[['_', None, None] \
                    for _y in xrange(rsize[1]*miny, rsize[1]*(maxy+1)+1)] \
                    for _x in xrange(rsize[0]*minx, rsize[0]*(maxx+1)+1)]
        for index in xrange(len(rooms)):
            for part in rooms[index].get_parts():
                for x in xrange(rsize[0]):
                    for y in xrange(rsize[1]):
                        temp_x = (part[0]-minx)*rsize[0]+x
                        temp_y = (part[1]-miny)*rsize[1]+y
                        #sprawdzamy czy na krawędzi = sciana
                        if (x == 0 and ((part[0]-1, part[1]) \
                                    not in rooms[index].get_parts()))\
                                or (x == rsize[0]-1 and ((part[0]+1, part[1])\
                                    not in rooms[index].get_parts()))\
                                or (y == 0 and ((part[0], part[1]-1)\
                                    not in rooms[index].get_parts()))\
                                or (y == rsize[1]-1 and ((part[0], part[1]+1)\
                                    not in rooms[index].get_parts())):
                            self.board[temp_x][temp_y][0] = 'w'

                        else:
                            self.board[temp_x][temp_y][0] = index
                            if random() > 0.99:
                                self.board[temp_x][temp_y][2] \
                                    = Enemy(10, 10, Damage(1.0, 1.0, 10, 5),
                                            Armor(0.5, 10), 15, temp_x, temp_y)
        
        self.size = (maxx+1-minx)*rsize[0], (maxy+1-miny)*rsize[1]
        
        #drogi
        ways = []
        for room in rooms:
            chosen_part = choice(room.get_parts())
            
            if (chosen_part[0]-1, chosen_part[1]) not in room.get_parts()\
                    and (chosen_part[0]-1, chosen_part[1]) in parts_used:
                room.make_way(chosen_part, (chosen_part[0]-1, chosen_part[1]))
                ways.append((chosen_part, (chosen_part[0]-1, chosen_part[1])))
                
            if (chosen_part[0]+1, chosen_part[1]) not in room.get_parts()\
                    and (chosen_part[0]+1, chosen_part[1]) in parts_used:
                room.make_way(chosen_part, (chosen_part[0]+1, chosen_part[1]))
                ways.append((chosen_part, (chosen_part[0]+1, chosen_part[1])))
                
            if (chosen_part[0], chosen_part[1]-1) not in room.get_parts()\
                    and (chosen_part[0], chosen_part[1]-1) in parts_used:
                room.make_way(chosen_part, (chosen_part[0], chosen_part[1]-1))
                ways.append((chosen_part, (chosen_part[0], chosen_part[1]-1)))
                
            if (chosen_part[0], chosen_part[1]+1) not in room.get_parts()\
                    and (chosen_part[0], chosen_part[1]+1) in parts_used:
                room.make_way(chosen_part, (chosen_part[0], chosen_part[1]+1))
                ways.append((chosen_part, (chosen_part[0], chosen_part[1]+1)))

            
            if len(room.get_parts()) > 1:
                
                chosen_part = choice(room.get_parts())
                
                if (chosen_part[0]-1, chosen_part[1]) not in room.get_parts()\
                        and (chosen_part[0]-1, chosen_part[1]) in parts_used:
                    room.make_way(chosen_part, 
                                  (chosen_part[0]-1, chosen_part[1]))
                    ways.append((chosen_part,
                                 (chosen_part[0]-1, chosen_part[1])))
                    
                if (chosen_part[0]+1, chosen_part[1]) not in room.get_parts()\
                        and (chosen_part[0]+1, chosen_part[1]) in parts_used:
                    room.make_way(chosen_part,
                                  (chosen_part[0]+1, chosen_part[1]))
                    ways.append((chosen_part,
                                 (chosen_part[0]+1, chosen_part[1])))
                    
                if (chosen_part[0], chosen_part[1]-1) not in room.get_parts()\
                        and (chosen_part[0], chosen_part[1]-1) in parts_used:
                    room.make_way(chosen_part,
                                  (chosen_part[0], chosen_part[1]-1))
                    ways.append((chosen_part,
                                 (chosen_part[0], chosen_part[1]-1)))
                    
                if (chosen_part[0], chosen_part[1]+1) not in room.get_parts()\
                        and (chosen_part[0], chosen_part[1]+1) in parts_used:
                    room.make_way(chosen_part,
                                  (chosen_part[0], chosen_part[1]+1))
                    ways.append((chosen_part,
                                 (chosen_part[0], chosen_part[1]+1)))
                
        for way in ways:
            if way[0][0] == way[1][0] and way[0][1] < way[1][1]:
                self.board[(way[0][0]-minx)*rsize[0] + (rsize[0]/2)][(way[0][1]-miny)*rsize[1] + rsize[1]-1][0] = 1
                self.board[(way[1][0]-minx)*rsize[0] + (rsize[0]/2)][(way[1][1]-miny)*rsize[1]][0] = 1
                self.board[(way[0][0]-minx)*rsize[0] + (rsize[0]/2)-1][(way[0][1]-miny)*rsize[1] + rsize[1]-1][0] = 1
                self.board[(way[1][0]-minx)*rsize[0] + (rsize[0]/2)-1][(way[1][1]-miny)*rsize[1]][0] = 1
                
            if way[0][0] == way[1][0] and way[0][1] > way[1][1]:
                self.board[(way[0][0]-minx)*rsize[0] + (rsize[0]/2)][(way[0][1]-miny)*rsize[1]][0] = 1
                self.board[(way[1][0]-minx)*rsize[0] + (rsize[0]/2)][(way[1][1]-miny)*rsize[1] + rsize[1]-1][0] = 1
                self.board[(way[0][0]-minx)*rsize[0] + (rsize[0]/2)-1][(way[0][1]-miny)*rsize[1]][0] = 1
                self.board[(way[1][0]-minx)*rsize[0] + (rsize[0]/2)-1][(way[1][1]-miny)*rsize[1] + rsize[1]-1][0] = 1
            
            if way[0][1] == way[1][1] and way[0][0] < way[1][0]:
                self.board[(way[0][0]-minx)*rsize[0] + rsize[1]-1][(way[0][1]-miny)*rsize[1] + (rsize[0]/2)][0] = 1
                self.board[(way[1][0]-minx)*rsize[0]][(way[1][1]-miny)*rsize[1] + (rsize[0]/2)][0] = 1
                self.board[(way[0][0]-minx)*rsize[0] + rsize[1]-1][(way[0][1]-miny)*rsize[1] + (rsize[0]/2)-1][0] = 1
                self.board[(way[1][0]-minx)*rsize[0]][(way[1][1]-miny)*rsize[1] + (rsize[0]/2)-1][0] = 1
            
            if way[0][1] == way[1][1] and way[0][1] > way[1][0]:
                self.board[(way[0][0]-minx)*rsize[0]][(way[0][1]-miny)*rsize[1] + (rsize[0]/2)][0] = 1
                self.board[(way[1][0]-minx)*rsize[0] + rsize[1]-1][(way[1][1]-miny)*rsize[1] + (rsize[0]/2)][0] = 1
                self.board[(way[0][0]-minx)*rsize[0]][(way[0][1]-miny)*rsize[1] + (rsize[0]/2)-1][0] = 1
                self.board[(way[1][0]-minx)*rsize[0] + rsize[1]-1][(way[1][1]-miny)*rsize[1] + (rsize[0]/2)-1][0] = 1
    
    def __setitem__(self, pos, item):
        x, y = pos
        self.board[x][y] = item

    def __getitem__(self, pos):
        x, y = pos
        return self.board[x][y]
    
    def get_size(self):
        """zwraca rozmiar mapy - parę"""
        return self.size


class Room(object):

    def __init__(self, first_part):
        self._parts = [first_part]
        self._ways = []
        
    def get_parts(self):
        return self._parts
    
    def get_ways(self):
        return self._ways
        
    def append(self, part):
        self._parts.append(part)
    
    def make_way(self, from_part, to_part): # trochę przekombinowane ale pracuje nad tym
        self._ways.append((from_part, to_part))
