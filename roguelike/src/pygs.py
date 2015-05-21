"""
main app
"""
import pygame
import pygame.locals as loc
from maps import Map
import characters
import os

loc = pygame.locals
class App(object):
    """ a """
    def __init__(self):
        """ s """
        self._running = True
        self._surface = None
        self._size = self.weight, self.height = 810, 650
        self._map = Map(50, (10, 10)) #rmnum, rsize 
        self._posx = 250
        self._posy = 250

    def init(self):
        """ s """
        pygame.init()
        pygame.display.set_caption('Rogaliq')
        self._surface = pygame.display.set_mode(self._size)
        self._running = True
        self._display_surf = pygame.display.set_mode((self._size), pygame.HWSURFACE) #
        self.load_images()
        self.load_music()
        self.play_music()

        self.do_nice_outlines(self._surface)
        pygame.key.set_repeat(5,100)#(delay, interval) in milisec

    def event(self, event):
        """ to do, soon"""
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == loc.K_UP  or event.key == loc.K_w:
                if self._posy > 0 and self._map[self._posx,self._posy-1][0] != '_':
                    self._posy -= 1
            if event.key == loc.K_DOWN  or event.key == loc.K_s:
                if self._posy < self._map.size[1]-1 and self._map[self._posx,self._posy+1][0] != '_':
                    self._posy += 1
            if event.key == loc.K_LEFT  or event.key == loc.K_a:
                if self._posx > 0 and self._map[self._posx-1,self._posy][0] != '_':
                    self._posx -= 1
            if event.key == loc.K_RIGHT  or event.key == loc.K_d:
                if self._posx < self._map.size[0]-1 and self._map[self._posx+1,self._posy][0] != '_':
                    self._posx += 1
            if event.key == loc.K_ESCAPE: #quit
                self._running = False

            if event.key == loc.K_m: #volume up
                if  self.volume<1:
                    self.volume+=0.05
                    pygame.mixer.music.set_volume(self.volume)
            if event.key == loc.K_n: #volume down
                if  self.volume>0:
                    self.volume-=0.05
                    pygame.mixer.music.set_volume(self.volume)

        if event.type == pygame.USEREVENT + 1:
            print(self.song_num ,"song ended")
            self.play_music()
    def loop(self):
        """ to do, soon """
        pass

    def render(self):
        """ in prog """
        _40 = 32
        _7 = (608/_40-1)/2 #9
        _15 = 608/_40 #19
        if self._posx < _7:
            x_o = 0
        elif self._posx > self._map.size[0]-_7-1:
            x_o = self._map.size[0]-_15
        else:
            x_o = self._posx-_7
        if self._posy < _7:
            y_o = 0
        elif self._posy > self._map.size[1]-_7-1:
            y_o = self._map.size[1]-_15
        else:
            y_o = self._posy-_7
        for y in xrange(608/_40):
            for x in xrange(608/_40):
                #not wall
                if self._map[(x_o+x),(y_o+y)][0] != '_': 
                    pygame.draw.rect(self._surface, ((self._map[(x_o+x),(y_o+y)][0]*64)%256, 100,
                    (self._map[(x_o+x),(y_o+y)][0]*32)%256),(x * _40, y * _40, _40, _40))
                #elif (x_o+x) % 5 == 0 or (y_o+y) % 5 == 0:
                #    pygame.draw.rect(self._surface, (0, 255, 0), (x * 40, y * 40, 40, 40))
                #wall
                else: 
                    # pygame.draw.rect(self._surface, (0, 0, 0),(x * _40, y * _40, _40, _40))
                    self._display_surf.blit(self.wall,(x * _40, y * _40))
                #hero
                if (self._posx, self._posy) == (x_o+x, y_o+y):  
                    #pos = ((x*40+20, y*40), (x*40+40, y*40+40), (x*40, y*40+15),(x*40+40, y*40+15), (x*40, y*40+40))
                    #pygame.draw.polygon(self._surface, (255, 0, 0), pos)
                    self._display_surf.blit(self.hero_image,(x * _40, y * _40))

        #minimap
        # ~~~~~~~~~~index out of range error
        _40 = 5 
        _7 = ((200-5)/_40-1)/2
        if self._posx < _7:
            x_o = 0
        elif self._posx > self._map.size[0]-_7-1:
            x_o = self._map.size[0]-2*_7-1
        else:
            x_o = self._posx-_7
        if self._posy < _7:
            y_o = 0
        elif self._posy > self._map.size[1]-_7-1:
            y_o = self._map.size[1]-2*_7-1
        else:
            y_o = self._posy-_7
        for y in xrange(200/_40):
            for x in xrange(200/_40):
                #not wall
                if self._map[(x_o+x),(y_o+y)][0] != '_':
                    pygame.draw.rect(self._surface, ((self._map[(x_o+x),(y_o+y)][0]*64)%256, 100,
                    (self._map[(x_o+x),(y_o+y)][0]*32)%256),(610+2+ x * _40, 405+ y * _40, _40, _40))
                #wall
                else:
                    pygame.draw.rect(self._surface, (0, 0, 0), (610+2+ x * _40, 405+ y * _40, _40, _40))
                #hero
                if (self._posx, self._posy) == (x_o+x, y_o+y):
                    pygame.draw.rect(self._surface, (255, 255, 255), pygame.Rect(610+2+ x*_40, 405+ y*_40, _40,  _40))

        # pygame.display.update()

        #volume visual
        self._display_surf.blit(self._image_library["004000-speaker-32.png"],(0, 612))
        light_bars = (0, 96, 0) 
        dark_bars = (0, 32, 0) 
        w =6
        for bar in xrange(20):
            if bar < self.volume*20:
                pygame.draw.rect(self._surface, light_bars, (20 +bar*w, 650- bar*2, w-1, bar*2))
            else:
                pygame.draw.rect(self._surface, dark_bars, (20 +bar*w, 650- bar*2, w-1, bar*2))
        pygame.display.update()
    # def cleanup(self):
    #     pygame.quit()

    def files(self, dir_): #lists files in directory
        files=[]
        p = os.popen("ls \"" + dir_+ "\"","r")# \" w przypadku spacji
        line = p.readline()
        while line:
            files.append(line.replace('\n',''))
            line = p.readline()
        return files

    def load_images(self):
        path =r"./items/"
        lista = self.files("items")
        self._image_library = {}
        for item in lista:
            uni_path = path.replace('/', os.sep).replace('\\', os.sep)#universal path, also works: os.path.join('','') 
            self._image_library[item] = pygame.image.load( uni_path + item ).convert_alpha()
            print("done loading " + item)

        #define short names 
        self.hero_image = self._image_library["ball.png"]
        self.wall = self._image_library["in36.png"]
    def load_music(self):
        '''load music from /music'''
        #https://freemusicarchive.org/music/Sycamore_Drive/The_Waves_The_Sea/
        #https://freemusicarchive.org/music/Sycamore_Drive/Sycamore_Drive/
        self.song_num = 0
        self.songs = self.files("music")
        self.volume = 0.05
        SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(SONG_END)
        pygame.mixer.pre_init(44100, -16, 2, 2048)
    def play_music(self):
        path =r"./music/"
        uni_path = path.replace('/', os.sep).replace('\\', os.sep)
        pygame.mixer.music.load(uni_path + self.songs[self.song_num])
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        self.song_num = (self.song_num +1)%len(self.songs)

    def do_nice_outlines(self,surface):
        color1 = (128, 0, 0) # red
        # 800 640
        # 610 610
        # pozioma
        start_1= (0, 609)
        end_1= (609, 609)
        width   = 5 
        pygame.draw.line(surface, color1, start_1, end_1, width)
        # pionowa 
        start_2= (609, 0)
        end_2= (609, 609)
        pygame.draw.line(surface, color1, start_2, end_2, width)

        color2 = (0, 64, 0) #green
        # draw a rectangle
        for p in xrange(5):
            for q in xrange(10):
                pygame.draw.rect(surface, color2, pygame.Rect(610+ p*40 + 2, 0+ q*40 + 2, 40,  2))# left top width height
                pygame.draw.rect(surface, color2, pygame.Rect(610+ p*40 + 2, 0+ q*40 + 2,  2, 40))#pion
                pygame.draw.rect(surface, color2, pygame.Rect(610+ p*40 +40, 0+ q*40 + 2,  2, 40))#pion
                pygame.draw.rect(surface, color2, pygame.Rect(610+ p*40 + 2, 0+ q*40 +40, 40,  2))
                
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
