import csv
from database import db, cursor

CSV_PATH = "questons.csv"

CATEGORIES = [
    "anglais",
    "culture_generale",
    "metiers_informatique",
    "logique",
    "algorithmes"
]

def insert_categories():
    for cat in CATEGORIES:
        cursor.execute(
            "INSERT OR IGNORE INTO categories (nom_categorie) VALUES (?)",
            (cat,)
        )
    db.commit()

def get_categorie_id(nom_categorie: str) -> int | None:
    cursor.execute("SELECT id_categorie FROM categories WHERE nom_categorie = ?", (nom_categorie,))
    row = cursor.fetchone()
    return row[0] if row else None

def import_csv_questions(csv_path="questons.csv"):
    insert_categories()

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")

        for categorie, question, a, b, c, rep in reader:
            categorie = categorie.strip()
            question = question.strip()
            a = a.strip()
            b = b.strip()
            c = c.strip()
            rep = rep.strip().lower()

            cat_id = get_categorie_id(categorie)

            cursor.execute("""
                INSERT INTO questions
                (question, option_a, option_b, option_c, reponse, type_question, categorie)
                VALUES (?, ?, ?, ?, ?, 'normal', ?)
            """, (question, a, b, c, rep, cat_id))

    db.commit()
    print("✅ Import terminé")

def insert_boss_questions():
    boss_questions = {
        "anglais": ("BOSS: What does the expression “the elephant in the room” mean?",
                    "A large problem that everyone notices but avoids talking about", "A person who lies too much in the room", "A large problem that everyone talks about", "a"),
        "culture_generale": ("BOSS: What happens at the event horizon of a black hole?",
                             "Time appears to stop for a distant observer", "Gravity suddenly disappears", "Light speeds up infinitely", "a"),
        "metiers_informatique": ("BOSS: Quel rôle modélise les menaces, définit les politiques de sécurité et supervise le risque?",
                                 "CISO", "Front-end Dev", "QA Tester", "a"),
        "logique": ("BOSS: Sur une île, les habitants sont soit toujours menteurs, soit toujours véridiques. Tu croises un habitant qui dit : “Nous sommes tous menteurs ici.” Que peut-on conclure?",
                    "Il ment donc au moins une personne dit la vérité", "Il dit la vérité", "Tout le monde ment", "a"),
        "algorithmes": ("BOSS: En Pyhton, Que va afficher ce code? print(0.1 + 0.2 == 0.3)",
                        "False", "True", "Erreur", "a"),
    }
    
    for cat, (q, a, b, c, rep) in boss_questions.items():
        cat_id = get_categorie_id(cat)
        cursor.execute("""
            INSERT INTO questions (question, option_a, option_b, option_c, reponse, type_question, categorie)
            VALUES (?, ?, ?, ?, ?, 'boss', ?)
        """, (q, a, b, c, rep, cat_id))
    
    db.commit()
    print("✅ 5 boss ajoutés !")
    

if __name__ == "__main__":
    import_csv_questions()
    insert_boss_questions()