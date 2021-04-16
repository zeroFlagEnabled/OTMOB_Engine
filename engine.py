#engineMod
import pygame
from pygame.locals import *

#Un entity est l'élément fondamental du moteur : un joueur, ennemi, environnement, etc.
class Entity()  :
  def __init__(self, name, engine, bounded = True)  :
    self.name = name
    self.engine = engine

    #Permet de savoir si l'entity peut sortir de l'écran
    self.bounded = bounded

    self.hasRect = False
    self.hasSprite = False

    #Permet de garder toutes les entitys dans la liste scene.contenu
    engine.scene.contenu.append(self)

  def InitRect(self, pos, size)  :
    self.Rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

    self.hasRect = True
  
  def InitSprite(self, image) :
    self.Sprite = pygame.image.load(image)

    #Dès qu'un Sprite est attribué, la possibilté d'une animation est envisagée
    self.AnimList = {}
    self.playingAnim = False
    self.playedAnim = 0

    self.hasSprite = True

  def AddAnim(self, name, ImageList):
    if self.hasSprite:
      
      #On charge chaque frame de l'animation
      frameList = []
      for image in ImageList:
        frameList.append([pygame.image.load(image[0]), image[1]])

      #Stocke toutes les animations sous forme d'un dictionnaire
      #"nom de l'anim" : [[Frame1, duréeFrame1], [Frame2, durée,Frame2]...]
      self.AnimList[name] = frameList

  def StartAnim(self, name):
    #On vérifie si l'animation existe
    if name in self.AnimList:
      self.playingAnim = True
      self.playedAnim = name
      #La frame que l'animation est actuellement en train de jouer
      self.AnimFrame = 1
      #On détermine la longeur totale de l'animation
      AnimLength = 0
      for frame in self.AnimList[name]:
        AnimLength += frame[1]
      self.AnimLength = AnimLength

    else :
      print("Cette animation n'a pas été attribuée à cette entité")

  def PlayAnim(self):
    if self.AnimFrame <= self.AnimLength:
      AnimFrame = self.AnimFrame
      AnimNotFound = True
      AnimList = self.AnimList[self.playedAnim].copy()
      #On détermine dans quelle étape de l'animation on se trouve
      while AnimNotFound:
        if AnimFrame > AnimList[0][1] :
          AnimFrame -= AnimList[0][1]
          AnimList.pop(0)
        else :
          AnimNotFound = False
          AnimToPlay = AnimList[0][0]
    else:
      #Pour l'instant, l'animation est jouée en boucle
      self.AnimFrame = 1
      AnimToPlay = self.AnimList[self.playedAnim][0][0]
    
    self.AnimFrame += 1
    return AnimToPlay


  def Draw(self, rendu) :
    if self.hasRect and self.hasSprite :
      #Si on joue une animation, on va déterminer quelle frame de l'animation
      if self.playingAnim:
        rendu.blit(self.PlayAnim(), self.Rect)
      else:
       rendu.blit(self.Sprite, self.Rect)
  
  def Update(self) :
    #Protocole par défaut d'un entity bounded
    #On s'assure qu'il ne sorte pas de l'écran
    if self.bounded:
      if self.hasRect:
        if self.Rect.topleft[0] < 0:
          self.Rect = pygame.Rect.move(self.Rect, (-self.Rect.topleft[0], 0))
        if self.Rect.topright[0] > self.engine.Rlongueur:
          self.Rect = pygame.Rect.move(self.Rect, ( self.engine.Rlongueur - self.Rect.topright[0], 0))

#La scène est l'élément intermédiaire du moteur, elle permet de garder une trace de chaque entity qui s'y trouve
class Scene() :
  def __init__(self) :
    #La fameuse liste avec tout les entitys
    self.contenu = []

  def Draw(self, rendu)  :
    for entity in self.contenu :
      entity.Draw(rendu)

  def Update(self) :
    for entity in self.contenu :
      entity.Update()

#L'élément le plus grand du système, il englobe le tout
class Moteur() :
  def __init__(self, longueur, largeur) :
    self.longueur = longueur
    self.largeur = largeur

    #Vu qu'on a un système de rendu intermédaire (adapté à la taille des sprites)
    #On définit les caractéristiques de ce rendu
    self.rapport = 4
    self.Rlongueur = self.longueur//self.rapport
    self.Rlargeur = self.largeur//self.rapport

  def Init(self) :

    pygame.init()
    
    self.fenetre = pygame.display.set_mode((self.longueur, self.largeur))
    self.rendu = pygame.Surface((self.Rlongueur, self.Rlargeur))
    
    self.scene = Scene()

    self.clock = pygame.time.Clock()

    #Cette liste contient toutes les touches appuyées lors d'une frame
    #Elle permet à tout les entitys subordonnés d'accéder à l'input de l'utilisateur
    self.keystrokes = []

  def Update(self) :

    #On commence par tout recouvrir d'un canevas blanc
    self.rendu.fill((255, 255, 255))

    self.scene.Update()
    self.scene.Draw(self.rendu)

    #Le passage du rendu intérmédiare à la fenêtre finale
    surface = pygame.transform.scale(self.rendu, (self.longueur, self.largeur))
    self.fenetre.blit(surface, (0,0))

    pygame.display.flip()

  #C'est ici que se trouve la boucle principale
  def Run(self) :

    continuer = True

    while continuer :
      self.Update()

      self.keystrokes = []

      #On remplit self.keystrokes une seule fois par frame
      for event in pygame.event.get() :
            if event.type == QUIT :
              pygame.quit()
              continuer = False
            if event.type == KEYDOWN : 
              self.keystrokes.append(event.key)

      #Ça c'est pour garder 60 fps
      self.clock.tick(60)