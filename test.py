import unittest
from unittest.mock import patch
import questionnaire
import questionnaire_import
import os
import json

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
            self.assertEqual(q.lancer(), 4) # tester si le score final en répondant 1 à tout égal 4 bonnes réponses

    def test_questionnaire_format_invalide(self):
        # ici, le fichier "format_invalide1.json" n'a pas de catégorie ni de titre et devrait donc obtenir "inconnue" pour ces 2 propriétés
        filename = os.path.join("test_data", "format_invalide1.json") # technique pour concaténer les chemins pour tous les os
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNotNone(q)
        self.assertEqual(q.categorie, "inconnue")
        self.assertEqual(q.difficulte, "inconnue")
        self.assertIsNotNone(q.questions)

        # ici, le fichier "format_invalide2.json" n'a pas de titre et devrait donc retourner un questionnaire à None
        filename = os.path.join("test_data", "format_invalide2.json") # technique pour concaténer les chemins pour tous les os
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNone(q)

        # ici, le fichier "format_invalide3.json" n'a pas de questions et devrait donc retourner un questionnaire à None
        filename = os.path.join("test_data", "format_invalide3.json") # technique pour concaténer les chemins pour tous les os
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNone(q)


class TestsImportQuestionnaire(unittest.TestCase):
    def test_import_format_json(self):
        questionnaire_import.generate_json_file("Animaux", "Les chats", "https://www.codeavecjonathan.com/res/mission/openquizzdb_50.json") # passer les données en dur dans la génération du fichier json
        filenames = ("animaux_leschats_confirme.json", "animaux_leschats_debutant.json", "animaux_leschats_expert.json") # récupération du nom des 3 fichiers json
        for filename in filenames:
            self.assertTrue(os.path.isfile(filename)) # Contrôler que tous les fichiers existent
            file = open(filename, "r")
            json_data = file.read()
            file.close()
            try:
                data = json.loads(json_data)
            except: # si le test échoue
                self.fail("Problème de désérialisation pour le fichier :", filename)
            
            self.assertIsNotNone(data.get("titre")) # titre
            self.assertIsNotNone(data.get("questions")) # questions
            self.assertIsNotNone(data.get("difficulte")) # difficulté
            self.assertIsNotNone(data.get("categorie")) # catégorie
            # s'il manque un champ, cela génère un échec du test
            if data.get("questions"): # s'il y a des questions
                for question in data["questions"]:
                    self.assertIsNotNone(question.get("titre")) # la question a un titre
                    self.assertIsNotNone(question.get("choix")) # test s'il y a du choix
                    if question.get("choix"): # si la question a au moins un choix
                        self.assertGreater(len(question["choix"]), 1) # la question a au moins 2 choix
                        for i in range(0, len(question["choix"])):
                            self.assertGreater(len(question["choix"][i][0]), 0) # pour chaque choix, la longueur du titre > 0 (test longueur nb caractères)
                            self.assertIsInstance(question["choix"][i][1], bool) # test si le 2ème champ est un booléen
                            bonnes_reponses = [i[0] for i in question.get("choix") if i[1]]
                    self.assertEqual(len(bonnes_reponses), 1) # tester qu'il y a bien qu'une seule bonne réponse par question via une boucle
            

unittest.main()
