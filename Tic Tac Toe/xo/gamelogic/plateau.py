__authors__ = "Mohamed Yassine RIANI"

"""
Ce fichier permet de...(complétez la description de ce que
ce fichier est supposé faire !
"""

from .case import Case
from random import randrange, random , choice
from math import inf

class Plateau:
    """
    Classe modélisant le plateau du jeu Tic-Tac-Toe.

    Attributes:
        cases (dictionary): Dictionnaire de cases. La clé est une position (ligne, colonne),
                            et la valeur est une instance de la classe Case.
    """

    def __init__(self):
        """
        Méthode spéciale initialisant un nouveau plateau contenant les 9 cases du jeu.
        """

        # Dictionnaire de cases.
        # La clé est une position (ligne, colonne), et la valeur est une instance de la classe Case.
        self.cases = {}

        # Appel d'une méthode qui initialise un plateau contenant des cases vides.
        self.initialiser()

    def initialiser(self):
        """
        Méthode fournie permettant d'initialiser le plateau avec des cases vides (contenant des espaces).
        """

        # Vider le dictionnaire (pratique si on veut recommencer le jeu).
        self.cases.clear()
        # Parcourir le dictionnaire et mettre des objets de la classe Case.
        # dont l'attribut "contenu" serait un espace (" ").
        for i in range(0, 3):
            for j in range(0, 3):
                self.cases[i,j] = Case(" ")

    def __str__(self):
        """Méthode spéciale fournie indiquant à Python comment représenter une instance de Plateau
        sous la forme d'une chaîne de caractères. Permet donc d'afficher le plateau du jeu
        à l'écran en faisant par exemple:
        p1 = Plateau()
        print(p1)
        Donc, lorsque vous affichez un objet, Python invoque automatiquement la méthode __str__
        Voici un exemple d'affichage:
         +-0-+-1-+-2-+
        0|   | X | X |
         +---+---+---+
        1| O | O | X |
         +---+---+---+
        2|   |   | O |
         +---+---+---+

        Returns:
            string: Retourne la chaîne de caractères à afficher.
        """
        s = " +-0-+-1-+-2-+\n"
        for i in range(0, 3):
            s += str(i)+ "| "
            for j in range(0, 3):
                s += self.cases[(i,j)].contenu + " | "
            if i<=1:
                s += "\n +---+---+---+\n"
            else:
                s += "\n +---+---+---+"
        return s

    def non_plein(self):
        """
        Retourne si le plateau n'est pas encore plein.
        Il y a donc encore des cases vides (contenant des espaces et non des "X" ou des "O").

        Returns:
            bool: True si le plateau n'est pas plein, False autrement.
        """
        for case in self.cases.values():
            if case.est_vide():
                return True
        
        return False

    def position_valide(self, ligne, colonne):
        """
        Vérifie si une position est valide pour jouer.
        La position ne doit pas être occupée.
        Il faut utiliser la méthode est_vide() de la classe Case.

        Args:
            ligne (int): Le numéro de la ligne dans le plateau du jeu.
            colonne (int): Le numéro de la colonne dans le plateau du jeu.

        Returns:
            bool: True si la position est valide, False autrement.
        """
        assert isinstance(ligne, int), "Plateau: ligne doit être un entier."
        assert isinstance(colonne, int), "Plateau: colonne doit être un entier."

        return self.cases[(ligne,colonne)].est_vide()

    def selectionner_case(self, ligne, colonne, pion):
        """
        Permet de modifier le contenu de la case
        qui a les coordonnées (ligne,colonne) dans le plateau du jeu
        en utilisant la valeur de la variable pion.

        Args:
            ligne (int): Le numéro de la ligne dans le plateau du jeu.
            colonne (int): Le numéro de la colonne dans le plateau du jeu.
            pion (string): Une chaîne de caractères ("X" ou "O").
        """
        assert isinstance(ligne, int), "Plateau: ligne doit être un entier."
        assert isinstance(colonne, int), "Plateau: colonne doit être un entier."
        assert isinstance(pion, str), "Plateau: pion doit être une chaîne de caractères."
        assert pion in ["O", "X"], "Plateau: pion doit être 'O' ou 'X'."

        self.cases[ (ligne,colonne) ].contenu = pion


    def est_gagnant(self, pion):
        """
        Permet de vérifier si un joueur a gagné le jeu.
        Il faut vérifier toutes les lignes, colonnes et diagonales du plateau.

        Args:
            pion (string): La forme du pion utilisé par le joueur en question ("X" ou "O").

        Returns:
            bool: True si le joueur a gagné, False autrement.
        """

        assert isinstance(pion, str), "Plateau: pion doit être une chaîne de caractères."
        assert pion in ["O", "X"], "Plateau: pion doit être 'O' ou 'X'."

        #horizontal
        for i in range(0,3):
            if ( self.cases[ (i,0)].est_pion(pion) and self.cases[ (i,1)].est_pion(pion) and self.cases[ (i,2)].est_pion(pion)):
                return True

        #vertical
        for j in range(0,3):
            if ( self.cases[ (0,j)].est_pion(pion) and self.cases[ (1,j)].est_pion(pion) and self.cases[ (2,j)].est_pion(pion)):
                return True

        #diagonal
        if ( (self.cases[ (0,0)].est_pion(pion) and self.cases[ (1,1)].est_pion(pion) and self.cases[ (2,2)].est_pion(pion) ) or (self.cases[ (0,2)].est_pion(pion) and self.cases[ (1,1)].est_pion(pion) and self.cases[ (2,0)].est_pion(pion))):
            return True

        return False

    def choisir_prochaine_case(self, pion , difficulte):
        """
        Permet de retourner les coordonnées (ligne, colonne) de la case que l'ordinateur
        peut choisir afin de jouer contre un autre joueur qui est normalement une personne.
        Ce choix doit se faire en fonction de la configuration actuelle du plateau.
        L'algorithme que vous allez concevoir permettant de faire jouer l'ordinateur
        n'a pas besoin d'être optimal. Cela permettra à l'adversaire de gagner de temps en temps.
        Il faut par contre essayer de mettre le pion de l'ordinateur dans une ligne, une colonne
        ou une diagonale contenant deux pions de l'adversaire pour que ce dernier ne gagne pas facilement.
        Il faut aussi essayer de mettre le pion de l'ordinateur dans une ligne, une colonne
        ou une diagonale contenant deux pions de l'ordinateur pour que ce dernier puisse gagner.
        Vous pouvez utiliser ici la fonction randrange() du module random.
        Par exemple: randrange(1,10) vous retourne une valeur entre 1 et 9 au hasard.

        Args:
            pion (string): La forme du pion de l'adversaire de l'ordinateur ("X" ou "O").

        Returns:
            (int,int): Une paire d'entiers représentant les coordonnées de la case choisie.
        """
        assert isinstance(pion, str), "Plateau: pion doit être une chaîne de caractères."
        assert pion in ["O", "X"], "Plateau: pion doit être 'O' ou 'X'."
        
        pionOrdinateur = 'X' if pion == 'O' else 'O'
        
        if(difficulte == 'Amateur' and random() < 0.15):
            print("random pos")
            choix = [ pos for pos,case in self.cases.items() if case.est_vide() ]
            return choice(choix)
        else:
            meilleurScore = -inf
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.cases[ (i,j) ].est_vide():
                        #on met le pion de l'ordinateur pour tester si cette case est un bon choix ou pas
                        self.selectionner_case(i , j , pionOrdinateur)
                        #la fonction minimax retourne un entier positif , nul ou négatif 
                        #on passe les pions et false car c'est le tour de l'humain fictif
                        score = self.minimax(pion , False)
                        #on annule la selection de la case 
                        self.cases[ (i,j) ].contenu =  " "
                        if(score > meilleurScore):
                            meilleurScore = score
                            meilleurePosition = ( i , j ) 
            return meilleurePosition


    def minimax(self,pion,maximiser):
        pionOrdinateur = 'X' if pion == 'O' else 'O'
        scores = {pion: -1 ,pionOrdinateur: 1 , 'partie_nulle' : 0}

        if(self.est_gagnant(pion)):
        #si l'humain gagne alors le score est négatif
            return scores[ pion ]
        elif(self.est_gagnant(pionOrdinateur)):
            #si l'ordinateur gagne alors le score est positif
            return scores[ pionOrdinateur]
        elif not self.non_plein():
            #plateau plein donc partie nulle , score nul
            return scores['partie_nulle']
       
        #la partie n'est pas terminée
        if maximiser:
            #c'est le tour de l'ordinateur ( il veut maximiser son score)
            meilleurScore = -inf
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.cases[ (i,j) ].est_vide():
                        self.selectionner_case(i , j , pionOrdinateur)
                        score = self.minimax(pion , False)
                        self.cases[ (i,j) ].contenu =  " "
                        meilleurScore = max(score , meilleurScore )

            return meilleurScore
        else:
            #c'est le tour de l'humain fictif  , on veux minimiser son score
            meilleurScore = inf
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.cases[ (i,j) ].est_vide():
                        self.selectionner_case(i , j , pion)
                        score = self.minimax(pion , True)
                        self.cases[ (i,j) ].contenu =  " "
                        meilleurScore = min(score , meilleurScore )

            return meilleurScore

