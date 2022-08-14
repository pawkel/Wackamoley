import pygame,math
pygame.init()
font = pygame.font.SysFont(None, 40)
class Hole:
    def __init__(self,win):
        self.holes = [0,0,0,0,0,0,0,0,0]
        self.hit = [0,0,0,0,0,0,0,0,0]
        self.win = win
        self.sh = win.get_height()
        self.sw = win.get_width()
        self.x = self.sw//3
        self.y = self.sh//3
        self.count = 0
        hole_opened = pygame.image.load('hole_opened.png')
        hole_closed = pygame.image.load('hole_closed.png')
        hole_hammered = pygame.image.load('hole_being_hammered.png')
        mole_hammered = pygame.image.load('mole_being_hammered.png')
        self.hole_opened = pygame.transform.scale(hole_opened, (100,100))
        self.hole_closed = pygame.transform.scale(hole_closed, (100,100))
        self.hole_hammered = pygame.transform.scale(hole_hammered, (100,175))
        self.mole_hammered = pygame.transform.scale(mole_hammered, (110,185))

    def drawHoles(self):
        self.count = 0
        for hole in self.holes:
            row, col = divmod(self.count, 3)
            x, y = self.x*col+50,self.y*row+80
            if hole == 0:
                self.win.blit(self.hole_closed,(x, y))
            elif hole == 1: ## moling but not hammered
                self.win.blit(self.hole_opened,(x, y))
            elif hole == 2: ## not moling and got hammered
                self.win.blit(self.hole_hammered,(x,y))
            else: ## moling and hammered
                self.win.blit(self.mole_hammered,(x,y))
            self.count+=1

    def updateGame(self, keys, mole, hammer):
        for j in range(9):
            moling = keys[mole.pad[j]]
            hammering = keys[hammer.pad[j]]
            if sum(self.hit) == 0: ## only update if the hit state relaxed back
                if moling and not hammering:
                    mole.happy()
                    self.holes[j] = 1
                elif not moling and hammering:
                    self.holes[j]=2
                    hammer.empty()
                elif moling and hammering:
                    mole.hammered()
                    hammer.hammered()
                    self.holes[j]=3
                    self.hit[j] = 1
                else:
                    self.holes[j] = 0
            else:
                self.hit[j] -=0.01
                self.hit[j] = max(self.hit[j],0)
                if  self.hit[j] <0.65:               
                    self.holes[j] = 0
        mole.scoring()
        hammer.scoring()
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
        self.molingCost = 0.005
        self.juicy = 0.02
        self.scoring()

    def scoring(self):
        self.score = font.render(f'Mole: {math.floor(self._score)}', True, (255,0,0))

    def hammered(self):
        self.sound.stop()
        self._score -=1

    def happy(self):
        self._score +=self.juicy-self.molingCost
        self.sound.play()
                  
class Hammer:
    def __init__(self):
        self.sound = pygame.mixer.Sound('Ricochet.wav')
        self.sound.set_volume(0.9)
        self.pad = [
            pygame.K_w,pygame.K_e,pygame.K_r,
            pygame.K_s,pygame.K_d,pygame.K_f,
            pygame.K_x,pygame.K_c,pygame.K_v
        ]
        self.punlishment = 0.002
        self._score = 0
        self.scoring()
        
    def scoring(self):
        self.score = font.render(f'Hammer: {math.floor(self._score)}', True, (255,0,0))

    def hammered(self):
        self._score +=1
        self.sound.play(maxtime=500, fade_ms=200)

    def empty(self):
        self._score -= self.punlishment

        