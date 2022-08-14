from wackamoleClass import *
import pygame
run = True
pygame.init()
screen_width = 800
screen_hight = 800
win = pygame.display.set_mode((screen_width,screen_hight))
pygame.display.set_caption("Wackamole!")
clock = pygame.time.Clock()
bgcolor = (0,155,255)
mole = Mole()
hammer = Hammer()
hole = Hole(win)

while run:
    win.fill(bgcolor)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mole._score = 0
            hammer._score = 0
    keys = pygame.key.get_pressed()
    hole.updateGame(keys, mole, hammer)
    pygame.display.update()
    clock.tick(100)