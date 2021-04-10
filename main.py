#main

import pygame
from pygame.locals import *

class objet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        self.image = pygame.image.load("Spreet.png")
        self.image = pygame.transform.scale(self.image, (64,64))

        #self.image = pygame.Surface([width, height])
        #self.image.fill(WHITE)
        #self.image.set_colorkey(WHITE)

    def Update(self, deltaPos):
        self.rect.move(deltaPos[0], deltaPos[1])


if __name__ == "__main__" :

    largeur = 600
    longueur = 800

    fenetre = pygame.display.set_mode((longueur, largeur))

    pos = [longueur//2 ,largeur//2]

    sprite = objet(pos)
    
    continuer = True
    
    while continuer :
        
        pygame.display.flip()

        fenetre.fill((255, 255, 255))

        #pygame.draw.circle(fenetre, (255, 0, 0), tuple(pos), 50)
        fenetre.blit(sprite.image, sprite.rect)
        
        for event in pygame.event.get() :
            print(event)
            if event.type == QUIT :
                pygame.quit()
                continuer = False
            if event.type == KEYDOWN :
                if event.key == K_d :
                    pos[0] += 8
                elif event.key == K_a :
                    pos[0] -= 8

