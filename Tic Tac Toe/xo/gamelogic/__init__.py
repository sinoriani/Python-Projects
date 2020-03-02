__authors__ = "Mohamed Yassine RIANI"

"""Ce fichier permet de...(complétez la description de ce que
ce fichier est supposé faire ! """

from .plateau import Plateau
from .joueur import Joueur

class Partie:
    """
    Classe modélisant une partie du jeu Tic-Tac-Toe utilisant
    un plateau et deux joueurs (deux personnes ou une personne et un ordinateur).

    Attributes:
        plateau (Plateau): Le plateau du jeu contenant les 9 cases.
        joueurs (Joueur list): La liste des deux joueurs (initialement une liste vide).
        joueur_courant (Joueur): Le joueur courant (initialisé à une valeur nulle: None)
        nb_parties_nulles (int): Le nombre de parties nulles (aucun joueur n'a gagné).
    """

    def verifier_fin_partie(self):
        """ retourne etat , gagnant
            etat : [non terminé , nul , gagnant]
            gagnant : nom du gagnant"""
        gagnant = False 
        if ( self.plateau.est_gagnant(self.joueur_courant.pion)):
            self.joueur_courant.nb_parties_gagnees += 1
            print(f"Partie terminée! Le joueur gagnant est: {self.joueur_courant.nom}")
            print(f"Parties gagnées par {self.joueurs[0].nom} : {self.joueurs[0].nb_parties_gagnees}")
            print(f"Parties gagnées par {self.joueurs[1].nom} : {self.joueurs[1].nb_parties_gagnees}")
            print(f"Parties nulles {self.nb_parties_nulles}")
            #il y a un gagnant
            gagnant = True
            print(self.joueur_courant.numero, ' a gagné')
            return { 'etat': 'gagnant' ,'gagnant' :  self.joueur_courant.numero }

        #si il n'y a pas de gagnant et le plateau est plein alors partie nulle
        if ( not gagnant and  not self.plateau.non_plein()):
            self.nb_parties_nulles += 1  
            print(self.plateau)
            print("Partie terminée! Aucun joueuer n'a gagné!")
            print(f"Parties gagnées par {self.joueurs[0].nom} : {self.joueurs[0].nb_parties_gagnees}")
            print(f"Parties gagnées par {self.joueurs[1].nom} : {self.joueurs[1].nb_parties_gagnees}")
            print(f"Parties nulles {self.nb_parties_nulles}")
            return {'etat': 'nul' , 'gagnant' :  None }

        return {'etat': 'non terminé' , 'gagnant' :  None }

    def __init__(self):
        """
        Méthode spéciale initialisant une nouvelle partie du jeu Tic-Tac-Toe.
        """
        self.plateau = Plateau()    # Le plateau du jeu contenant les 9 cases.
        self.joueurs = []       # La liste des deux joueurs (initialement une liste vide).
                                # Au début du jeu, il faut ajouter les deux joueurs à cette liste.
        self.joueur_courant = None  # Le joueur courant (initialisé à une valeur nulle: None)
                                    # Pendant le jeu et à chaque tour d'un joueur,
                                    # il faut affecter à cet attribut ce joueur courant.
        self.nb_parties_nulles = 0  # Le nombre de parties nulles (aucun joueur n'a gagné).
        self.difficulte = "Amateur" # La difficulté de l'ordinateur ( amateur ou pro )

    def jouer(self,nom1,nom2):
        #Joueur 1
        pionJoueur = 'X'
        self.joueurs.append( Joueur(nom1,pionJoueur,1) )
       
        #Joueur 2
        pionJoueur = 'O'
        self.joueurs.append( Joueur(nom2,pionJoueur,2) )

        self.joueur_courant = self.joueurs[0]   
        
    def recommencer(self):
        self.joueur_courant = self.joueurs[0]   
        self.plateau = Plateau()

    def tour(self, position):
        
        self.plateau.selectionner_case(position[0], position[1] , self.joueur_courant.pion )
        resultat = self.verifier_fin_partie()
        print(self.plateau)
        gagnant = self.joueur_courant.nom
        self.joueur_courant = self.joueurs[1] if self.joueurs[0] is self.joueur_courant else self.joueurs[0]
        return resultat,gagnant
        

if __name__ == "__main__":
    # Just for testing
    partie = Partie()
    partie.jouer('j1','j2')

