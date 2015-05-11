"""
main app
"""
import pygame
import pygame.locals as loc
from maps import Map
import characters

loc = pygame.locals
class App(object):
    """ a """
    def __init__(self):
        """ s """
        self._running = True
        self._surface = None
        self._size = self.weight, self.height = 600, 600
        self._map = Map(50, (10, 10))
        self._posx = 250
        self._posy = 250

    def init(self):
        """ s """
        pygame.init()
        pygame.display.set_caption('Rogal')
        self._surface = pygame.display.set_mode(self._size)
        self._running = True

    def event(self, event):
        """ to do, soon"""
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == loc.K_UP:
                if self._posy > 0 and self._map[self._posx,self._posy-1][0] != '_':
                    self._posy -= 1
            if event.key == loc.K_DOWN:
                if self._posy < self._map.size[1]-1 and self._map[self._posx,self._posy+1][0] != '_':
                    self._posy += 1
            if event.key == loc.K_LEFT:
                if self._posx > 0 and self._map[self._posx-1,self._posy][0] != '_':
                    self._posx -= 1
            if event.key == loc.K_RIGHT:
                if self._posx < self._map.size[0]-1 and self._map[self._posx+1,self._posy][0] != '_':
                    self._posx += 1

    def loop(self):
        """ to do, soon """
        pass

    def render(self):
        """ in prog """
        if self._posx < 7:
            x_o = 0
        elif self._posx > self._map.size[0]-8:
            x_o = self._map.size[0]-15
        else:
            x_o = self._posx-7
        if self._posy < 7:
            y_o = 0
        elif self._posy > self._map.size[1]-8:
            y_o = self._map.size[1]-15
        else:
            y_o = self._posy-7
        for y in xrange(15):
            for x in xrange(15):
                if self._map[(x_o+x),(y_o+y)][0] != '_':
                    pygame.draw.rect(self._surface, ((self._map[(x_o+x),(y_o+y)][0]*64)%256, 100, (self._map[(x_o+x),(y_o+y)][0]*32)%256),
                                     (x * 40, y * 40, 40, 40))
                #elif (x_o+x) % 5 == 0 or (y_o+y) % 5 == 0:
                #    pygame.draw.rect(self._surface, (0, 255, 0),
                #                     (x * 40, y * 40, 40, 40))
                else:
                    pygame.draw.rect(self._surface, (0, 0, 0),
                                     (x * 40, y * 40, 40, 40))
                if (self._posx, self._posy) == (x_o+x, y_o+y):
                    pos = ((x*40+20, y*40), (x*40+40, y*40+40), (x*40, y*40+15),
                           (x*40+40, y*40+15), (x*40, y*40+40))
                    pygame.draw.polygon(self._surface, (255, 0, 0), pos)
        pygame.display.update()

    # def cleanup(self):
    #     pygame.quit()

    def execute(self):
        """ s """
        self.init()

        while self._running:
            for event in pygame.event.get():
                self.event(event)
            self.loop()
            self.render()
        # self.cleanup()


if __name__ == '__main__':
    __TheApp__ = App()
    __TheApp__.execute()
