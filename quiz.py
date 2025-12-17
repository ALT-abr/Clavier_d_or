from database import save_partie, update_joueur, get_categories, get_questions_by_categorie, get_categorie_name, get_categorie_id, get_boss_question_by_categorie
import os

# Efface l’écran du terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

SEUIL_POINTS = {
    0: 10,  # pour passer de catégorie 1 → 2
    1: 20,  # pour passer de catégorie 2 → 3
    2: 30,  # pour passer de catégorie 3 → 4
    3: 40,  # pour passer de catégorie 4 → 5
}

# La fonction principale de jeu
def jouer_quiz(joueur, partie=None):
    clear_screen()
    print("=== Bienvenue dans le Grand Quiz ! ===\n")

    score_total = 0
    start_theme = None
    start_question = 0  
    resume_on_boss = False #vrai si on a quitté pendant le boss
    
    # Si on reprend une partie
    if partie:
        score_total = partie["score"]
        joueur.score = score_total             
        joueur.boss_elimine = partie["boss_elimine"]
        start_theme = get_categorie_name(partie["id_categorie"])
        start_question = partie["question_index"]
        resume_on_boss = (start_question == -1) # si on était sur le boss


    categories = get_categories()  
    if not categories:
        print("❌ Aucune catégorie trouvée. As-tu importé le CSV ?")
        return
    
    # recupère l'index de la catégorie de départ et de la question de départ pour reprendre
    start_index = categories.index(start_theme) if (start_theme in categories) else 0

    total_questions = 0
    bonnes_reponses = score_total  # si tu reprends, ton score est déjà là
    
    # t_i = index de catégorie (0,1,2,3,4)
    for t_i in range(start_index, len(categories)):
        theme = categories[t_i]
        rows = get_questions_by_categorie(theme)  # list des tuples: (question, a, b, c, rep)

        if not rows:
            continue

        print(f"\n{'='*20} Thème : {theme} {'='*20}")

        # Si on reprend sur le boss, on saute toutes les questions normales du thème
        if resume_on_boss and theme == start_theme:
            q_start = len(rows)  # la boucle des questions normales ne s’exécute pas, boss direct
        else:
            q_start = start_question if theme == start_theme else 0


        for i in range(q_start, len(rows)):
            question, a, b, c, rep = rows[i]
            rep = rep.strip().lower()  # a,b,c

            print(f"\nQuestion {i+1} : {question}")
            print(f"a) {a}")
            print(f"b) {b}")
            print(f"c) {c}")

            while True:
                reponse = input("Votre réponse (a/b/c) ou quit : ").strip().lower()

                if reponse in ["quit", "q"]:
                    id_cat = get_categorie_id(theme)
                    save_partie(joueur.id_joueur, id_cat, i, score_total, joueur.boss_elimine)
                    joueur.score = score_total
                    update_joueur(joueur.id_joueur, joueur.score, joueur.boss_elimine)
                    print("\n💾 Partie sauvegardée !")
                    return

                if reponse in ["a", "b", "c"]:
                    break

                print("Veuillez entrer a, b ou c.")

            total_questions += 1

            if reponse == rep:
                print("✔ Bonne réponse ! +1 point")
                score_total += 1
                bonnes_reponses += 1
            else:
                # afficher la bonne option
                bonne_texte = {"a": a, "b": b, "c": c}.get(rep, rep)
                print(f"✘ Mauvaise réponse. La bonne était : {rep}) {bonne_texte}")
        
        if resume_on_boss and theme != start_theme:
            resume_on_boss = False

        boss = get_boss_question_by_categorie(theme)
        if boss and (not resume_on_boss or theme == start_theme):
            question, a, b, c, rep = boss
            rep = rep.strip().lower()
        
            print("\n🔥🔥🔥 QUESTION BOSS 🔥🔥🔥")
            print(question)
            print(f"a) {a}")
            print(f"b) {b}")
            print(f"c) {c}")
        
            while True:
                reponse = input("\nVotre réponse (a/b/c) ou quit : ").strip().lower()
        
                if reponse in ["quit", "q"]:
                    # on sauvegarde un marqueur: question_index = -1 pour dire “je suis sur le boss”
                    id_cat = get_categorie_id(theme)
                    save_partie(joueur.id_joueur, id_cat, -1, score_total, joueur.boss_elimine)
                    joueur.score = score_total
                    update_joueur(joueur.id_joueur, joueur.score, joueur.boss_elimine)
                    print("\n💾  Partie sauvegardée (pendant le BOSS) !")
                    return
        
                if reponse in ["a", "b", "c"]:
                    break
        
                print("Veuillez entrer a, b ou c.")
        
            if reponse == rep:
                print("\n👑  BOSS VAINCU ! +5 points et +1 boss éliminé")
                score_total += 5
                joueur.boss_elimine += 1
            else:
                bonne_texte = {"a": a, "b": b, "c": c}.get(rep, rep)
                print(f"\n☠️  Défaite contre le boss. La bonne était : {rep}) {bonne_texte}")
                print("⚠️  Règle: défaite => reset score à 0")
                score_total = 0
                joueur.boss_elimine = 0

            resume_on_boss = False
        
        # === CONDITION POUR PASSER À LA CATÉGORIE SUIVANTE ===
        seuil = SEUIL_POINTS.get(t_i, 0)
        
        if joueur.boss_elimine > t_i:
            print("\n✅  Condition validée : boss éliminé → catégorie suivante débloquée")
        elif score_total >= seuil:
            print(f"✅   Condition validée : {score_total} ≥ {seuil} points")
        else:
            print("\n❌  Condition NON remplie")
            print("➡   Boss non éliminé ET score insuffisant")
            print("🔄  Retour à zéro selon les règles")
        
            score_total = 0
            joueur.boss_elimine = 0
            joueur.score = 0
        
            update_joueur(joueur.id_joueur, 0, 0)
            first_cat = get_categories()[0]
            first_cat_id = get_categorie_id(first_cat)
            save_partie(joueur.id_joueur, first_cat_id, 0, 0, 0)
            return  # fin immédiate du jeu
        
        # après un thème, on reset la reprise
        start_question = 0
        start_theme = None

    # CONDITION POUR OBTENIR LE CLAVIER D’OR
    POINTS_CLAVIER_OR = 85
    BOSS_TOTAL = 5
    
    print("\n🏆 ÉPREUVE FINALE : LE CLAVIER D’OR 🏆")
    
    if joueur.boss_elimine >= BOSS_TOTAL:
        print("\n👑  LÉGENDE ! Tu as éliminé les 5 boss.")
        print("✨  LE CLAVIER D’OR EST À TOI ✨")
    elif score_total >= POINTS_CLAVIER_OR:
        print(f"\n🔥  MAÎTRISE ABSOLUE ! {score_total} ≥ {POINTS_CLAVIER_OR} points")
        print("✨   LE CLAVIER D’OR EST À TOI ✨")
    else:
        print("\n❌ Tu n’as pas rempli les conditions finales.")
        print("☠️ Le Clavier d’Or te rejette…")
    
    # Fin de partie
    print("\n" + "=" * 50)
    print("=== FIN DE LA PARTIE ! ===")
    print(f"Score final : {score_total} points\n")
        
    joueur.score = score_total
    update_joueur(joueur.id_joueur, joueur.score, joueur.boss_elimine)

    # On “vide” la reprise
    save_partie(joueur.id_joueur, None, 0, joueur.score, joueur.boss_elimine)

    if total_questions > 0:
        pourcentage = (bonnes_reponses / total_questions) * 100
        print(f"({pourcentage:.1f}% de réussite)")
    else:
        print("(Aucune question jouée)")