# -*- coding: utf-8 -*-
"""
Funkcje pomocnicze
"""

import os
import pygame
from collections import namedtuple


Damage = namedtuple('Damage', 'pierce hurt base extra')
#Struktura Obrażeń(Damage):
#przebicie(pierce) = liczba ~ 1.0 +-1.0
#zranienie(hurt) = liczba ~ 1.0 +-1.0
#baza(base) = liczba całkowita
#dodatkowe(extra) = liczba całkowita

Armor = namedtuple('Armor', 'gauge durability')
#Struktura Pancerza(Armor):
#kaliber(gauge) = liczba z zakresu <0.0 , 1.0>
#wytrzymałość(durability) = liczba całkowita

class Auxil(object):
    """ auxiliary class """

    @staticmethod
    def files(dir_):
        """ lists files in a directory """
        files = []
        pop = os.popen("ls \"" + dir_ + "\"", "r")  # \" w przypadku spacji
        line = pop.readline()  #managery contextu do obslugi plikow?
        while line:
            files.append(line.rstrip('\n'))
            line = pop.readline()
        return files

    @staticmethod
    def do_nice_outlines(surface):
        """ some outlines """
        red = (128, 0, 0)

        # pozioma
        start_1 = (0, 610-1)
        end_1 = (610-1, 610-1)
        width = 5
        pygame.draw.line(surface, red, start_1, end_1, width)

        # pionowa
        start_2 = (610-1, 0)
        end_2 = (610-1, 610-1)
        pygame.draw.line(surface, red, start_2, end_2, width)

        green = (0, 64, 0)

        pygame.draw.line(surface, green, (612, 20), (812, 20), 4)
        pygame.draw.line(surface, green, (612, 60), (812, 60), 4)

        for col in xrange(6):
            pygame.draw.rect(surface, green,
                              pygame.Rect(610+col*40+2, 20+2, 2, 40))
            pygame.draw.rect(surface, green,
                              pygame.Rect(610+col*40+40, 20+2, 2, 40))

        for col in xrange(6):
            pygame.draw.line(surface, green,
                             (612+col*40, 100),
                             (612+col*40, 100+4*40), 4)
        for row in xrange(5):
            pygame.draw.line(surface, green,
                             (612, 100+row*40),
                             (812, 100+row*40), 4)

    @staticmethod
    def write(surface, msg, size, where_x, where_y):
        """ write text """
        font = pygame.font.SysFont('mono', size, bold=True)
        text = font.render(msg, True, (0, 128, 0))
        text = text.convert_alpha()
        surface.blit(text, (where_x, where_y)) 
