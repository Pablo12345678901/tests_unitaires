import unittest
from unittest.mock import patch
import questionnaire
import os

def additionner(a, b):
    return a+b

def conversion_nombre():
    num_str = input("Rentrez un nombre : ")
    return int(num_str)

class TestUnitaireDemo(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    def test_additionner1(self):
        self.assertEqual(additionner(5, 10),15)
    
    def test_additionner2(self):
        self.assertEqual(additionner(6, 10),16)

    def test_conversion_nombre_valide(self):
        with patch("builtins.input", return_value="10"):
            self.assertEqual(conversion_nombre(), 10)

    # TESTER SI UNE EXCEPTION SE DECLENCHE EN CAS DE MAUVAISE VALEUR FOURNIE PAR L'UTILISATEUR
    def test_conversion_entree_invalide(self):
        with patch("builtins.input", return_value="abcd"):
            # ASSETRAISES POUR TESTER LE DECLENCHEMENT D'UNE EXCEPTION
            self.assertRaises(ValueError, conversion_nombre)
            # assetRaises prend en paramètres :
            #   le type d'exception
            #   la fonction a tester : en paramètre donc sans les parenthèses

# TEST SUR CODE EXISTANT
class TestsQuestion(unittest.TestCase):
    # Ici, je vais simuler une partie du programme
    def test_question_bonne_mauvaise_reponse(self):
        # je crée volontairement une liste de choix
        choix = ("choix1", "choix2", "choix3")
        # j'appelle la class "Question" du fichier importé "questionnaire"
        q = questionnaire.Question("titre_question", choix, "choix2") # je fourni les données
         # je fourni à nouveau des données en dur sur la méthode appelée depuis le fichier importé
        # Je simule les réponse de l'utilisateur avec un patch
        with patch("builtins.input", return_value="1"):
            self.assertFalse(q.poser(1, 1)) # je vérifie si lorsqu'il saisit une mauvaise réponse, la fonction du module importé retourne "False"
        with patch("builtins.input", return_value="2"): 
            self.assertTrue(q.poser(1, 1)) # idem pour une bonne réponse -> True
        with patch("builtins.input", return_value="3"): 
            self.assertFalse(q.poser(1, 1)) # Test de toutes les réponses possibles

class TestsQuestionnaire(unittest.TestCase):
    def test_questionnaire_lancer_alien_debutant(self):
        filename = os.path.join("test_data", "cinema_alien_debutant.json") # technique pour concaténer les chemins pour tous les os
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNotNone(q) # tester si le questionnaire n'est pas None
        
        self.assertEqual(len(q.questions), 10) # Nb de questions > tester si le nombre de questions est correct > ici = 10
        self.assertEqual(q.titre, 'Alien') # titre
        self.assertEqual(q.categorie, 'Cinéma') # catégorie
        self.assertEqual(q.difficulte, 'débutant') # difficulté
        # patcher le input -> forcer de répondre toujours à 1 > score final = 4/10
        with patch("builtins.input", return_value="1"):
            self.assertEqual(q.lancer(), 4)

unittest.main()
