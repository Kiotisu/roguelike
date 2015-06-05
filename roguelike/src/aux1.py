"""
auxiliary class
"""

import os
import pygame


class Aux(object):
    """ auxiliary class """
    def __init__(self):
        pass

    @staticmethod
    def files(dir_):
        """ lists files in a directory """
        files = []
        pop = os.popen("ls \"" + dir_ + "\"", "r")  # \" w przypadku spacji
        line = pop.readline()  #managery contextu do obslugi plikow!!!!
        while line:
            files.append(line.rstrip('\n'))
            line = pop.readline()
        return files

    def do_nice_outlines(self, surface):
        """ some outlines """
        color1 = (128, 0, 0)  # red
        # pozioma
        start_1 = (0, 610-1)
        end_1 = (610-1, 610-1)
        width = 5
        pygame.draw.line(surface, color1, start_1, end_1, width)
        # pionowa
        start_2 = (610-1, 0)
        end_2 = (610-1, 610-1)
        pygame.draw.line(surface, color1, start_2, end_2, width)

        color2 = (0, 64, 0)  #green
        # draw a rectangle
        for col in xrange(5):
            for row in xrange(6):
                pygame.draw.rect(surface, color2,
                                 pygame.Rect(610+col*40+2, 20+row*40+2, 40, 2))
                                 #left top width height
                pygame.draw.rect(surface, color2,
                                 pygame.Rect(610+col*40+2, 20+row*40+2, 2, 40))
                pygame.draw.rect(surface, color2,
                                 pygame.Rect(610+col*40+40, 20+row*40+2, 2, 40))
                pygame.draw.rect(surface, color2,
                                 pygame.Rect(610+col*40+2, 20+row*40+40, 40, 2))

    def write(self, surface, msg, size, where_x, where_y):
        """ write text """
        font = pygame.font.SysFont('mono', size, bold=True)
        text = font.render(msg, True, (0, 128, 0))
        text = text.convert_alpha()
        surface.blit(text, (where_x, where_y))