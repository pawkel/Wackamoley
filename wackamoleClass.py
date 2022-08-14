import pygame,math
pygame.init()
font = pygame.font.SysFont(None, 40)
class Hole:
    def __init__(self,win):
        self.holes = [0,0,0,0,0,0,0,0,0]
        self.win = win
        self.sh = win.get_height()
        self.sw = win.get_width()
        self.x = self.sw//3
        self.y = self.sh//3
        self.count = 0
        hole_opened = pygame.image.load('hole_opened.png')
        hole_closed = pygame.image.load('hole_closed.png')
        self.hole_opened = pygame.transform.scale(hole_opened, (100,100))
        self.hole_closed = pygame.transform.scale(hole_closed, (100,100))
    def openHole(self,hole):
        self.holes[hole] = 1
    def closeHole(self,hole):
        self.holes[hole] = 0
    def checkOpen(self,hole):
        if self.holes[hole]==1:
            return True
        else:
            return False

    def drawHoles(self):
        self.count = 0
        for hole in self.holes:
            row, col = divmod(self.count, 3)
            x, y = self.x*col+50,self.y*row+80
            if hole == 0:
                self.win.blit(self.hole_closed,(x, y))
            else:
                self.win.blit(self.hole_opened,(x, y))
            self.count+=1

    def updateGame(self, keys, mole, hammer):
        for j in range(9):
            moling = keys[mole.pad[j]]
            hammering = keys[hammer.pad[j]]
            if moling and hammering:
                hammer.hammered()
                mole.hammered()
                self.closeHole(j)
            elif moling and not hammering:
                mole.happy()
                self.openHole(j)
            elif not moling and hammering:
                print('hammer hurts')
                self.closeHole(j)
            else:
                self.closeHole(j)
        self.drawHoles()
        self.win.blit(hammer.score, (20, 40))
        self.win.blit(mole.score, (self.sw-200, 40))

class Mole:
    def __init__(self):
        self.pad = [
                pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,
                pygame.K_KP4,pygame.K_KP5,pygame.K_KP6,
                pygame.K_KP1,pygame.K_KP2,pygame.K_KP3
            ]
        self.sound = pygame.mixer.Sound('pickup.wav')
        self._score = 0
        self.scoring()

    def scoring(self):
        self.score = font.render(f'Mole: {math.floor(self._score)}', True, (255,0,0))

    def hammered(self):
        self.sound.stop()
        self._score -=1

    def happy(self):
        self._socre +=self.
        
    def update(self,keys,hole,hammer):
        for j in range(9):
            if keys[self.pad[j]]:
                if hammer.hit[j]==0:
                    hole.openHole(j)
                    self.sound.play(maxtime=500, fade_ms=200)
            else:
                hole.closeHole(j)
            
class Hammer:
    def __init__(self):
        self.hit = [0,0,0,0,0,0,0,0,0]
        self.sound = pygame.mixer.Sound('Ricochet.wav')
        self.sound.set_volume(0.9)
        self.pad = [
            pygame.K_w,pygame.K_e,pygame.K_r,
            pygame.K_s,pygame.K_d,pygame.K_f,
            pygame.K_x,pygame.K_c,pygame.K_v
        ]
        self._score = 0
        self.scoring()
        
    def scoring(self):
        self.score = font.render(f'Hammer: {math.floor(self._score)}', True, (255,0,0))

    def hammered(self):
        self._score +=1
        self.sound.play(maxtime=500, fade_ms=200)

    def update(self,keys,hole,mole):
        for j in range(9):
            moling = hole.checkOpen(j)
            if moling:
                if keys[self.pad[j]]: 
                    hole.closeHole(j)
                    self.hit[j]=1
                    mole.sound.stop()
                    self._score +=1
                    mole._score -=1
                    self.sound.play(maxtime=500, fade_ms=200)
                    # print(f'Hit!, hole:{j},Pad:{self.pad[j]}')
                else:
                    mole._score +=0.02
            else:
                if keys[self.pad[j]]: 
                  self._score-=0.005
            if keys[self.pad[j]] == 0: 
                self.hit[j]=0
        mole.scoring()
        self.scoring()
        