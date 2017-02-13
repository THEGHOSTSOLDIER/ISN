########################################
# module principal du jeu (Standalone)
 
import pygame
from pygame.locals import *
size = 0
pygame.init()
pygame.mouse.set_visible(False)
son = pygame.mixer.Sound("one.ogg")
fenetre = pygame.display.set_mode((640, 480), FULLSCREEN)

fond = pygame.image.load("back.jpg").convert()
fenetre.blit(fond, (0,0))

perso = pygame.image.load("perso.png").convert_alpha()
perso_x = 0
perso_y = 0

perso2 = pygame.image.load("nin.png").convert_alpha()
perso2 = pygame.transform.scale(perso2, (150,150))
position_perso = perso2.get_rect()

fenetre.blit(perso, (perso_x, perso_y))
fenetre.blit(perso2, position_perso)

son.play()
pygame.display.flip()

continuer = 1

pygame.key.set_repeat(400, 30)
while continuer:
    
    for event in pygame.event.get():

        if event.type == QUIT:
            continuer = 0
            
        if event.type == KEYDOWN:
            
            if event.key == K_DOWN:
                position_perso = position_perso.move(0,3)
            if event.key == K_UP:
                position_perso = position_perso.move(0,-3)
            if event.key == K_LEFT:
                position_perso = position_perso.move(-3,0)
            if event.key == K_RIGHT:
                position_perso = position_perso.move(3,0)
            if event.key == K_ESCAPE:
                fenetre = pygame.display.set_mode((640,480), RESIZABLE)
                son.stop()
                pygame.display.set_icon(perso)
                pygame.display.set_caption("TEST")

        if event.type == MOUSEBUTTONDOWN and event.button == 3 and event.pos[1] < 100:
            print("zone dangereuse")
        if event.type == MOUSEMOTION:
            """if event.button == 1:"""
            perso_x = event.pos[0]
            perso_y = event.pos[1]
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso, (perso_x, perso_y))
    fenetre.blit(perso2, position_perso)
    pygame.display.flip()
pygame.quit()
