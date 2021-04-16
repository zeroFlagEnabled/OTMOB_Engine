#main

import engine
import playerCharacter

if __name__ == "__main__" :

    #Dimensions de la fenêtre
    largeur = 1024
    longueur = 768

    #Voir engine.py
    #On crée une instance de Moteur, on l'initialise
    moteur = engine.Moteur(longueur, largeur)
    moteur.Init()

    #On crée un objet Joueur
    joueur = playerCharacter.Player("Player", moteur)

    #On lui attribue un sprite, un rect
    joueur.InitSprite("Spreet.png")
    joueur.InitRect([moteur.Rlongueur//2, moteur.Rlargeur//2], [16, 16])

    #On définit une animation, puis on la démarre
    joueur.AddAnim("idle", [["Assets/ElPlombier1.png", 10], ["Assets/ElPlombier2.png", 10]])
    joueur.StartAnim("idle")

    #On fait tourner le moteur
    moteur.Run()