import engine
import pygame
from pygame.locals import * 

#Puisqu'un joueur est un objet spécial sa classe est dérivée de celle de l'objet
class Player(engine.Entity) :
  def __init__(self, name, moteur) :
    #Permet d'appeler la fonction __init__() d'Objet
    super().__init__(name, moteur)

    self.momentum = 0

  def Update(self) :
    #On prend en compte le mouvement latéral du joueur
    deltaPos = [0,0]
    if K_a in self.engine.keystrokes :
      deltaPos[0] -= 4
    if K_d in self.engine.keystrokes :
      deltaPos[0] += 4

    #Implémentation de la gravité
    self.momentum += 0
    deltaPos[1] += self.momentum

    self.Rect = pygame.Rect.move(self.Rect, (deltaPos[0], deltaPos[1]))

    #Effet trampoline
    if self.Rect.bottomleft[1] > self.engine.Rlargeur :
      self.momentum = -self.momentum

    super().Update()