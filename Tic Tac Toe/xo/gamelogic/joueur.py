__author__ = 'M. Bouden'
__date__ = "Déc. 2019"

"""Ce fichier permet de définir la classe Joueur permettant de jouer au jeu Tic-Tac-Toe"""

class Joueur:
    """
    Classe modélisant le joueur qui une personne ou un ordinateur.

    Attributes:
        nom (str): Le nom du joueur.
        type (str): Le type du joueur ("Personne" ou "Ordinateur").
        pion (str): La forme du pion affecté au joueur ('X' ou 'O').
        nb_parties_gagnees (int): Le nombre de parties gagnées par le joueur.
    """

    def __init__(self, nom, pion,numero):
        """
        Méthode spéciale initialisant un nouveau joueur.
        Args:
            nom (string): Le nom du joueur.
            type (string): Le type du joueur ("Personne", "Ordinateur")
            pion (string): La forme du pion choisi (ou affecté) par le joueur ("O" ou "X")
        """

        assert isinstance(nom, str), "Joeur: nom doit être une chaîne de caractères."
        assert isinstance(pion, str), "Joueur: pion doit être une chaîne de caractères."
        assert pion in ["O", "X"], "Joueur: pion doit être 'O' ou 'X'."

        self.nom = nom      # Nom du joueur.
        self.pion = pion    # Forme du pion affecté au joueur.
        self.nb_parties_gagnees = 0 # Nombre de parties gagnées par le joueur.
        self.numero = numero
        self.pret = True
    
    def set_pret(self,val):
        self.pret = val