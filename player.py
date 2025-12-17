import sqlite3
from database import db, cursor, get_joueurs, get_historique, get_joueur

class Joueur:
    #initialisation du joueur avec id, nom, score et boss_elimine
    def __init__(self, id_joueur: int, nom: str):
        self.id_joueur = id_joueur
        self.nom = nom
        self.score = 0
        self.boss_elimine = 0

    # methode statique pour créer un nouveau joueur avec vérification du nom  
    @staticmethod   
    def creer_joueur():
        nom_joueur = input("Entrez le nom de votre héros : ")
        row = get_joueurs(nom_joueur)
        if row is not None:
            print("Ce nom est déjà pris!! Veuillez en choisir un autre!")
            return Joueur.creer_joueur()
        elif nom_joueur == "":
            print("Le nom ne peut pas être vide! Veuillez réessayer.")
            return Joueur.creer_joueur()
        elif len(nom_joueur) < 3:
            print("Le nom doit contenir au moins 3 caractères. Veuillez réessayer.")
            return Joueur.creer_joueur()
        elif nom_joueur == "menu":
            return None
        else:
            print(f"Bienvenue, {nom_joueur}, dans la quête du Clavier d'Or !")
        return Joueur(None, nom_joueur)
    
    # pour charger une partie existante, recupère les infos du joueur dans la BDD
    @staticmethod
    def charger_joueur():
        nom = input("Entrez le nom du joueur à reprendre : ").strip()
        row = get_joueur(nom)
        if row is None:
            print("❌ Aucun joueur trouvé avec ce nom.")
            return None
    
        id_j, nom_db, score_db, boss_db = row
        j = Joueur(id_j, nom_db)
        j.score = score_db
        j.boss_elimine = boss_db
        print(f"\n✅ Partie chargée : {j.nom} (score={j.score}, boss={j.boss_elimine})")
        return j

    # sauvegarde le joueur dans la BDD, et récupère son id automatiquement
    def sauvegarder_joueur(self):
        try:
            cursor.execute("""
            INSERT INTO joueurs (nom_joueur, score, boss_elimine)
            VALUES (?, ?, ?)
            """, (self.nom, self.score, self.boss_elimine))
            db.commit()
            self.id_joueur = cursor.lastrowid
            print(f"Le joueur {self.nom} a été sauvegardé dans la base de données.")
        except sqlite3.Error as e:
            print(f"Une erreur est survenue lors de la sauvegarde du joueur : {e}")
    
    # affiche l'historique des joueurs leur nom, score, boss éliminés et date de création
    def afficher_historique_joueur():
        historique = get_historique()
        if not historique:
            print("Aucun historique de joueurs trouvé.")
            return
        else:
            print("\n                      ╔════════════════════════════════════════════════════════════════════════╗")
            print("                      ║                    __---HISTORIQUE DES JOUEURS---__                    ║")
            print("                      ╠════════════════════════════════════════════════════════════════════════╣")
            print("                      ║  Nom du Joueur  ║   Score   ║  Bosss Éliminés  ║    Date de Création   ║")
            print("                      ╠════════════════════════════════════════════════════════════════════════╣")
            for row in historique:
                nom_joueur, score, boss_elimine, date_creation = row
                print(f"                      ║  {nom_joueur:<15} ║  {score:<8} ║  {boss_elimine:<10}     ║  {date_creation:<20} ║")
            print("                      ╚════════════════════════════════════════════════════════════════════════╝")