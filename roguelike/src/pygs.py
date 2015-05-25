"""
main app
"""

import pygame
import pygame.locals as loc
import os
from maps import Map
from characters import Hero
from characters import Enemy
from collections import deque
loc = pygame.locals


class App(object):

    def execute(self):
        """ s """
        self.init()

        while self._running:
            for event in pygame.event.get():
                self.event(event)
            self.turn()
            self.render()
        # self.cleanup()

    def __init__(self):
        """ s """
        self._running = True
        self._surface = None
        self._size = self.weight, self.height = 810, 650
        self._map = Map(50, (10, 10))  #rmnum, rsize
        self._posx = 250
        self._posy = 250
        
        self._horizon = 3  # zasieg wzroku w kazda strone  if == 3 => [][][] postac [][][]
        self._myturn = True

        # gosc czasem rodzi sie w pustce
        while self._map[self._posx,self._posy][0] == '_':
            self._posx +=1

        self._hero = None
        self._enemy1 = None
        self._display_surf = None

        self._image_library = None
        self.hero_image = None
        self.wall = None
        self.terrain = None
        self.enemy1 = None

        self.song_num = None
        self.songs = None
        self.volume = None

        self._action = None

    def init(self):
        """ s """
        pygame.init()
        pygame.display.set_caption('Rogal')
        self._surface = pygame.display.set_mode(self._size)
        self._running = True
        self._display_surf = pygame.display.set_mode(self._size, pygame.HWSURFACE)
        self.load_images()
        self.load_music()
        self.play_music()

        self.do_nice_outlines(self._surface)
        pygame.key.set_repeat(5,100)  #(delay, interval) in milisec
        
        #napisy
        self.write("EQ", 22, 700, 0)
        self.write("Stats:", 14, 615, 0+6*40+20)
        self.write("HP", 14, 615, 0+6*40+35)  # +15 pix pionowo
        self.write("Attack", 14, 615, 0+6*40+50)
        self.write("Defense", 14, 615, 0+6*40+65)

        #Create Hero
        self._hero = Hero(0, 0, 1, 1, 1, 0, 100, self._posx, self._posx)

        self.write(str(self._hero._hp), 14, 615+60, 0+6*40+35)
        self.write(str(self._hero._attack), 14, 615+60, 0+6*40+50)
        self.write(str(self._hero._defense), 14, 615+60, 0+6*40+65)

        #Create Enemy
        self._enemy1 = Enemy(1, 1, 1, 0, 100, 260, 260)
        # attack, defense, damage, armor, hp, x, y

    def event(self, event):
        """ to do, soon"""
        #alternative?
        # pressedkeys = pygame.key.get_pressed()
        # if pressedkeys[pygame.K_x]:

        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if self._myturn == True:
                if event.key == loc.K_UP or event.key == loc.K_w:
                    if self._posy > 0 and self._map[self._posx,self._posy-1][0] != '_':
                        self._posy -= 1
                        self._action.append('w')
                        self._myturn = False
                if event.key == loc.K_DOWN or event.key == loc.K_s:
                    if self._posy < self._map.size[1]-1 and self._map[self._posx,self._posy+1][0] != '_':
                        self._posy += 1
                        self._action.append('s')
                        self._myturn = False
                if event.key == loc.K_LEFT or event.key == loc.K_a:
                    if self._posx > 0 and self._map[self._posx-1, self._posy][0] != '_':
                        self._posx -= 1
                        self._action.append('a')
                        self._myturn = False
                if event.key == loc.K_RIGHT or event.key == loc.K_d:
                    if self._posx < self._map.size[0]-1 and self._map[self._posx+1,self._posy][0] != '_':
                        self._posx += 1
                        self._action.append('d')
                        self._myturn = False

            if event.key == loc.K_ESCAPE:  #quit
                self._running = False
            if event.key == loc.K_m:  #volume up
                if self.volume <= 1:
                    self.volume += 0.05
                    pygame.mixer.music.set_volume(self.volume)
            if event.key == loc.K_n:  #volume down
                if self.volume >= 0:
                    self.volume -= 0.05
                    pygame.mixer.music.set_volume(self.volume)

        if event.type == pygame.USEREVENT + 1:
            print(self.song_num, "song ended")
            self.play_music()

        if event.type == pygame.MOUSEBUTTONDOWN: 
            if event.button == 1:
                (po_x, po_y)  = pygame.mouse.get_pos()
                if po_x >= 610 and po_y >= 20 and po_y <= 20+6*40:   #mouse pointer in the equipment zone
                    (square_x, square_y) =((po_x-610)/40, (po_y-20)/40)
                    self._marked_y = square_x
                    self._marked_x = square_y


    def render(self):
        """ in prog """
        _boczne_pola = (608/32-1)/2  # powinno byc 9
        if self._posx < _boczne_pola:
            x_o = 0
        elif self._posx > self._map.size[0]-_boczne_pola-1:
            x_o = self._map.size[0] - (2*_boczne_pola+1)  # 2*_boczne_pola+1 = 19
        else:
            x_o = self._posx-_boczne_pola
        if self._posy < _boczne_pola:
            y_o = 0
        elif self._posy > self._map.size[1]-_boczne_pola-1:
            y_o = self._map.size[1] - (2*_boczne_pola+1)
        else:
            y_o = self._posy-_boczne_pola
        for y in xrange(608/32):
            for x in xrange(608/32):
                if self._map[(x_o+x), (y_o+y)][0] != '_':  # podloga
                    pygame.draw.rect(self._surface, ((self._map[(x_o+x), (y_o+y)][0]*64) % 256, 100,
                                                     (self._map[(x_o+x), (y_o+y)][0]*32) % 256),
                                     (x * 32, y * 32, 32, 32))
                    self._display_surf.blit(self.terrain, (x * 32, y * 32))
                #elif (x_o+x) % 5 == 0 or (y_o+y) % 5 == 0:
                #    pygame.draw.rect(self._surface, (0, 255, 0), (x * 32, y * 32, 32, 32))
                else:  # pustka - nie sciana
                    # self._display_surf.blit(self.wall, (x * 32, y * 32))
                    pygame.draw.rect(self._surface, (0, 0, 0),(x * 32, y * 32, 32, 32))
                #hero
                if (x_o+x, y_o+y) == (self._posx, self._posy):  
                    self._display_surf.blit(self.hero_image,(x * 32, y * 32))
                #enemy
                # if self._map[(x_o+x),(y_o+y)][2] != None:
                    # self._display_surf.blit(self.enemy1, (x * 32, y * 32))
        
                #vision
                if not (abs(x_o+x - self._posx) <= self._horizon and abs(y_o+y - self._posy) <= self._horizon ):
                    self._display_surf.blit(self._image_library["black.png"],(x * 32, y * 32))

        #volume visual
        self._display_surf.blit(self._image_library["004000-speaker-32.png"],(0, 612))
        light_bars = (0, 96, 0) 
        dark_bars = (0, 32, 0) 
        w = 5

        for bar in xrange(20):
            if bar < self.volume*20:
                pygame.draw.rect(self._surface, light_bars, (20+bar*w, 650-bar*2, w-1, bar*2))
            else:
                pygame.draw.rect(self._surface, dark_bars, (20+bar*w, 650-bar*2, w-1, bar*2))
        pygame.display.update()
    # def cleanup(self):
    #     pygame.quit()

    def files(self, dir_): #lists files in directory
        files = []
        p = os.popen("ls \"" + dir_ + "\"", "r")  # \" w przypadku spacji poki co ta linijka wyglada strasznie @WJ
        line = p.readline()  # poza tym menagery contextu do obslugi plikow!!!!
        while line:
            files.append(line.rstrip('\n'))
            line = p.readline()
        return files

    """
    Dorzucam deklaracje tych wszystkich self.cos do __init__
    ale jesli serio ma byc tego tak duzo to bedzie to trzeba niestety przeniesc
    do innej klasy pewnie... @WJ
    """

    def load_images(self):
        path = r"./items/"
        lista = self.files("items")
        self._image_library = {}

        for item in lista:
            uni_path = path.replace('/', os.sep).replace('\\', os.sep)  #universal path, also works: os.path.join('','')
            self._image_library[item] = pygame.image.load(uni_path + item).convert_alpha()

        #define short names 
        self.hero_image = self._image_library["ball.png"]
        self.wall = self._image_library["texture9.png"]
        self.terrain = self._image_library["texture18.png"]  # 12 lub 18
        self.enemy1 = self._image_library["enemy1.png"]

    def load_music(self):
        """load music from /music"""
        #https://freemusicarchive.org/music/Sycamore_Drive/The_Waves_The_Sea/
        #https://freemusicarchive.org/music/Sycamore_Drive/Sycamore_Drive/
        self.song_num = 0
        self.songs = self.files("music")
        self.volume = 0.00
        SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(SONG_END)
        pygame.mixer.pre_init(44100, -16, 2, 2048)

    def play_music(self):
        path = r"./music/"
        uni_path = path.replace('/', os.sep).replace('\\', os.sep)
        pygame.mixer.music.load(uni_path + self.songs[self.song_num])
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        self.song_num = (self.song_num+1) % len(self.songs)

    def do_nice_outlines(self, surface):
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
        for p in xrange(5):
            for q in xrange(6):
                pygame.draw.rect(surface, color2, pygame.Rect(610+p*40+2, 20+q*40+2, 40, 2))  #left top width height
                pygame.draw.rect(surface, color2, pygame.Rect(610+p*40+2, 20+q*40+2, 2, 40))  #pion
                pygame.draw.rect(surface, color2, pygame.Rect(610+p*40+40, 20+q*40+2, 2, 40))  #pion
                pygame.draw.rect(surface, color2, pygame.Rect(610+p*40+2, 20+q*40+40, 40, 2))

    def turn(self):
        if self._myturn:
            self._action = deque([])  # kolejka dwukierunkowa
        else:
            self.player_action()
            self.enemy_turn()

    def player_action(self):
        while len(self._action) > 0:
           act = self._action.popleft()  # zwroc akcje
           print(act)  # na razie nie wiem co z tym zrobic, bo nie mamy ataku

    def enemy_turn(self):
        #przeciwnicy w zasiegu wzroku
        _enemy_list = []
        for i in xrange(self._horizon*2+1):
            for j in xrange(self._horizon*2+1):
                if not self._map[(self._posx+i-self._horizon), (self._posy+j-self._horizon)][2] is None:  # nie puste pole
                    _enemy_list.append(self._map[(self._posx+i-self._horizon), (self._posy+j-self._horizon)][2])

        # for en in _enemy_list:
            # en.move()  # not implemented

	    self._myturn = True

    def write(self, msg, size, xx, yy):
        font = pygame.font.SysFont('mono', size, bold=True)
        text = font.render(msg, True, (0, 128, 0))
        text = text.convert_alpha()
        self._display_surf.blit(text, (xx, yy))


if __name__ == '__main__':
    __TheApp__ = App()
    __TheApp__.execute()