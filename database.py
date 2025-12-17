import sqlite3

# Connexion à la base de données SQLite
# Cette base stocke les joueurs, les catégories, les questions et les parties sauvegardées
db = sqlite3.connect('quiz_database.db')
cursor = db.cursor()

# Activation des clés étrangères pour assurer l’intégrité des relations
cursor.execute("PRAGMA foreign_keys = ON;")

# Table des joueurs, contient les informations de jeoueur
cursor.execute("""
CREATE TABLE IF NOT EXISTS joueurs(
    id_joueur INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_joueur VARCHAR(50) NOT NULL,
    score INTEGER DEFAULT 0,
    boss_elimine INTEGER DEFAULT 0,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")
# Table des catégories, contient les différentes catégories de questions
cursor.execute("""
CREATE TABLE IF NOT EXISTS CATEGORIES(
    id_categorie INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_categorie VARCHAR(50) NOT NULL
    );
""")
# Table des parties, contient l'état sauvegardé des parties des joueurs
cursor.execute("""
CREATE TABLE IF NOT EXISTS parties (
    id_partie INTEGER PRIMARY KEY AUTOINCREMENT,
    id_joueur INTEGER UNIQUE,
    id_categorie INTEGER,
    question_index INTEGER,
    score INTEGER,
    boss_elimine INTEGER,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_joueur) REFERENCES joueurs(id_joueur),
    FOREIGN KEY (id_categorie) REFERENCES categories(id_categorie)
    );
""")
# Table des questions, contient les questions du quiz
cursor.execute("""
CREATE TABLE IF NOT EXISTS QUESTIONS(
    id_question INTEGER PRIMARY KEY AUTOINCREMENT,
    question VARCHAR(255) NOT NULL,
    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    reponse VARCHAR(255) NOT NULL,
    type_question CHECK(type_question IN ('normal','boss')),
    categorie INTEGER,
    FOREIGN KEY (categorie) REFERENCES categories(id_categorie)
    );
""")

# Fonctions d'accès à la base de données
def get_joueurs(nom_joueur: str):
    cursor.execute("SELECT * FROM joueurs WHERE nom_joueur = ?", (nom_joueur,))
    return cursor.fetchone()
# recupère un joueur par son nom, utilise lors de la création ou du chargement d'une partie
def get_joueur(nom_joueur: str):
    cursor.execute("SELECT id_joueur, nom_joueur, score, boss_elimine FROM joueurs WHERE nom_joueur = ?", (nom_joueur,))
    return cursor.fetchone()

def update_joueur(id_joueur: str, score: int, boss_elimine: int):
    cursor.execute("UPDATE joueurs SET score = ?, boss_elimine = ? WHERE id_joueur = ?", (score, boss_elimine, id_joueur)) #player_name de la place de nom_joueur
    db.commit()

# Affiche l'historique des joueurs, trié par score décroissant
def get_historique():
    cursor.execute("SELECT nom_joueur, score, boss_elimine, date_creation FROM joueurs order by score DESC")
    return cursor.fetchall()

# Sauvegarde l'état exact de la partie d'un joueur
def save_partie(id_joueur: str, id_categorie: str | None, question_index: int, score: int, boss_elimine: int):
    cursor.execute("""
        INSERT INTO parties (id_joueur, id_categorie, question_index, score, boss_elimine)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id_joueur) DO UPDATE SET
            id_categorie = excluded.id_categorie,
            question_index = excluded.question_index,
            score = excluded.score,
            boss_elimine = excluded.boss_elimine,
            date_creation = CURRENT_TIMESTAMP
    """, (id_joueur, id_categorie, question_index, score, boss_elimine))
    db.commit()
# Charge la dernière partie sauvegardée d'un joueur
def load_partie(id_joueur: int):
    cursor.execute("""
        SELECT id_categorie, question_index, score, boss_elimine
        FROM parties
        WHERE id_joueur = ?
    """, (id_joueur,))
    
    row = cursor.fetchone()
    if row is None:
        return None

    return {
        "id_categorie": row[0],
        "question_index": row[1],
        "score": row[2],
        "boss_elimine": row[3]
    }
#recupère l'id d'une catégorie par son nom pour la fichage
def get_categorie_id(nom_categorie: str):
    cursor.execute("SELECT id_categorie FROM categories WHERE nom_categorie = ?", (nom_categorie,))
    row = cursor.fetchone()
    return row[0] if row else None
# recupère le nom d'une catégorie par son id, Reprendre une partie, Passer à la catégorie suivante...
def get_categorie_name(id_categorie: int):
    cursor.execute("SELECT nom_categorie FROM categories WHERE id_categorie = ?", (id_categorie,))
    row = cursor.fetchone()
    return row[0] if row else None

# Récupère la liste des catégories disponibles par ordre d'id "l'ordre de jeu"
def get_categories():
    cursor.execute("SELECT nom_categorie FROM categories ORDER BY id_categorie")
    return [row[0] for row in cursor.fetchall()]

# Récupère les questions normales d'une catégorie 
def get_questions_by_categorie(nom_categorie: str):
    cursor.execute("""
        SELECT q.question, q.option_a, q.option_b, q.option_c, q.reponse
        FROM questions q
        JOIN categories c ON c.id_categorie = q.categorie
        WHERE c.nom_categorie = ?
        AND q.type_question = 'normal'
        ORDER BY q.id_question
    """, (nom_categorie,))
    return cursor.fetchall()
# Récupère la question boss d'une catégorie 
def get_boss_question_by_categorie(nom_categorie: str):
    cursor.execute("""
        SELECT q.question, q.option_a, q.option_b, q.option_c, q.reponse
        FROM questions q
        JOIN categories c ON c.id_categorie = q.categorie
        WHERE c.nom_categorie = ? AND q.type_question = 'boss'
        ORDER BY q.id_question
        LIMIT 1
    """, (nom_categorie,))
    return cursor.fetchone()

# un message de finalisation 
print("\n\n\n✅ Tables vérifiées/créées avec succès.")
print("✅ Connexion à la base de données établie.")
print("✅ La base de données est prête à être utilisée.")