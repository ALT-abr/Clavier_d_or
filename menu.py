import os
from database import load_partie
from intro import mession_message
from player import Joueur
from quiz import jouer_quiz

def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
        
def show_menu() -> str:
    clear_screen()
    print("\n\n")
    print("""
                      ╔═══════════════════════════════════════════════════════════════════════╗
                      ║             ═════ LE MENU LÉGENDAIRE DU CLAVIER D’OR ═════            ║
                      ║                                                                       ║
                      ║  [1] ➤  N o u v e l l e   p a r t i e                                 ║
                      ║  [2] ➤  C o n t i n u e r   u n e   p a r t i e                       ║
                      ║  [3] ➤  H i s t o r i q u e   d e s   p a r t i e s                   ║
                      ║  [4] ➤  A i d e                                                       ║
                      ║  [5] ➤  M e s s i o n                                                 ║
                      ║  [6] ➤  Q u i t t e r   l e   j e u                                   ║
                      ║                                                                       ║
                      ╚═══════════════════════════════════════════════════════════════════════╝
""")
    return ''  # Retourne une chaîne vide pour éviter l'affichage None

def get_user_choice() -> str:
    while True:
        choice = input('👉 Votre choix: ').lower()
        if choice == "1":
            clear_screen()
            print("\n\n")
            joueur = Joueur.creer_joueur()
            if joueur is None:
                show_menu()
                continue
            joueur.sauvegarder_joueur()
            input("\n let's goo ! Appuyez sur Entrée pour continuer ᯓ➤ ")
            jouer_quiz(joueur)
            input("\n👈 Entrée pour revenir au menu...")
            show_menu()
        elif choice == "2":
            clear_screen()
            joueur = Joueur.charger_joueur()
            if joueur is None:
                print("\n\n")
                print("le jouer n'a pas pu être chargé. Retour au menu principal.")
                input("\n👈 Entrée pour revenir au menu...")
                show_menu()
                continue
            partie = load_partie(joueur.id_joueur)
            if partie is None or partie["id_categorie"] is None:
                print("\n--------__ℹ️ Aucune partie en cours pour ce joueur!__--------")
                input()
                show_menu()
                continue
            jouer_quiz(joueur, partie)
            input("\n👈 Entrée pour revenir au menu...")
            show_menu()
        elif choice == "3":
            clear_screen()
            print("\n\n")
            Joueur.afficher_historique_joueur()
            input("\n👈 Entrée pour revenir au menu...")
            show_menu()
        elif choice in ["4", "help", "h"]:
            clear_screen()
            print("\n\n")
            help_section()
            input("\n👈 Entrée pour revenir au menu...")
            show_menu()
        elif choice == "5":
            clear_screen()
            print("\n\n")
            mession_message()
            input()
            show_menu()
        elif choice == "6":
            quit_game()
        else:
            print("❌ Choix invalide! Veuillez réessayer ❌")
            input("\nAppuyez sur Entrée pour continuer ᯓ➤ ")


def help_section() -> str:
    print("""
            ╔══════════════════════════════════════════════════════════════════════════════════════════╗
            ║                                                                                          ║
            ║         ██████╗ ██╗     █████╗ ██╗   ██╗██╗███████╗██████╗      ██████╗ ██████╗          ║
            ║        ██╔════╝ ██║    ██╔══██╗██║   ██║██║██╔════╝██╔══██╗    ██╔═══██╗██╔══██╗         ║
            ║        ██║  ███╗██║    ███████║██║   ██║██║█████╗  ██████╔╝    ██║   ██║██████╔╝         ║
            ║        ██║   ██║██║    ██╔══██║╚██╗ ██╔╝██║██╔══╝  ██╔══██╗    ██║   ██║██╔══██╗         ║
            ║        ╚██████╔╝██████╗██║  ██║ ╚████╔╝ ██║███████╗██║  ██║    ╚██████╔╝██║  ██║         ║
            ║         ╚═════╝ ╚═════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝╚═╝  ╚═╝     ╚═════╝ ╚═╝  ╚═╝         ║
            ║                                                                                          ║
            ╠══════════════════════════════════════════════════════════════════════════════════════════╣
            ║ ⚔️  ⚔️  ⚔️                   ⚔️  AIDE – QUÊTE DU CLAVIER D’OR⚔️                      ⚔️  ⚔️  ⚔️  ║
            ╠══════════════════════════════════════════════════════════════════════════════════════════╣
            ║                                                                                          ║
            ║  ⚔️   BIENVENUE, HÉROS DU CODE ! ⚔️                                                        ║
            ║   Dans un monde où la programmation est le plus grand des arts martiaux,                 ║
            ║   un seul artefact brille au-dessus de tous :                                            ║
            ║  🗝️  LE MYTHIQUE CLAVIER D’OR 🗝️                                                           ║
            ║   Symbole ultime de maîtrise absolue… Seuls les plus grands peuvent le réclamer !        ║
            ║                                                                                          ║
            ╠══════════════════════════════════════════════════════════════════════════════════════════╣
            ║                              🏰  STRUCTURE DE LA QUÊTE 🏰                                ║
            ╠══════════════════════════════════════════════════════════════════════════════════════════╣
            ║  5 DOMAINES MAUDITS – 5 BOSS LÉGENDAIRES – 100 ÉPREUVES (20 questions par domaine)       ║
            ║      1.  🇬🇧 ANGLAIS – Le Gardien des Mots Interdits                                      ║
            ║      2.  CULTURE GÉNÉRALE – La Sphinx des Savoirs Oubliés                                ║
            ║      3.  MÉTIERS DE L’IT – Le Titan des Carrières Numériques                             ║
            ║      4.  LOGIQUE – Le Démon des Paradoxes                                                ║
            ║      5.  ALGORITHMES – Le Roi des Abysses Computationnels                                ║
            ║                                                                                          ║
            ║                                                                                          ║
            ╠══════════════════════════════════════════════════════════════════════════════════════════╣
            ║                           🔥 RÈGLES SACRÉES DE PROGRESSION 🔥                            ║
            ╠══════════════════════════════════════════════════════════════════════════════════════════╣
            ║  Pour avancer et passer au domaine suivant, tu DOIS :                                    ║
            ║     ✦  VAINCRE LE BOSS DU DOMAINE (question ultime secrète après les 20 épreuves) ✦      ║
            ║                             OU                                                           ║
            ║     ✦  ATTEINDRE LE SEUIL DE PUISSANCE MINIMUM : ✦                                       ║
            ║        10 points  → Ouvre le Domaine 2                                                   ║
            ║        20 points  → Ouvre le Domaine 3                                                   ║
            ║        30 points  → Ouvre le Domaine 4                                                   ║
            ║        40 points  → Ouvre le Domaine 5                                                   ║
            ║                                                                                          ║
            ╠══════════════════════════════════════════════════════════════════════════════════════════╣
            ║                         🏆 COMMENT REMPORTER LE CLAVIER D’OR 🏆                          ║
            ╠══════════════════════════════════════════════════════════════════════════════════════════╣
            ║  Deux chemins mènent à la gloire éternelle :                                             ║
            ║     1. Terrasser LES 5 BOSS LÉGENDAIRES                                                  ║
            ║                             OU                                                           ║
            ║     2. Atteindre 85 POINTS OU PLUS à travers tous les domaines                           ║
            ║                                                                                          ║
            ╠══════════════════════════════════════════════════════════════════════════════════════════╣
            ║                       ⚠️  ⚠️  ⚠️   A T T E N T I O N ⚠️  ⚠️  ⚠️                                ║
            ╠══════════════════════════════════════════════════════════════════════════════════════════╣
            ║  ⚠️   Si tu échoues à remplir l’une des deux conditions à la fin d’un domaine…  ⚠️         ║
            ║      🌑 TON SCORE EST RÉDUIT EN CENDRES 🌑                                               ║
            ║      Tu repars de zéro… Le monde entier te maudira…                                      ║
            ║                                                                                          ║
            ╠══════════════════════════════════════════════════════════════════════════════════════════╣
            ║                                 🛡️  COMMANDES MAGIQUES 🛡️                                  ║
            ╠══════════════════════════════════════════════════════════════════════════════════════════╣
            ║  quit  / out    → Sauvegarder et fuir le destin (temporairement)                         ║
            ║  help  /  H     → Invoquer cette aide sacrée                                             ║
            ║                                                                                          ║
            ╠══════════════════════════════════════════════════════════════════════════════════════════╣
            ║                           🌟 MOTS D’ENCOURAGEMENTS FINAUX 🌟                             ║
            ╠══════════════════════════════════════════════════════════════════════════════════════════╣
            ║                 Que les dieux du code guident tes doigts sur le clavier…                 ║
            ║                                  Prouve que tu es digne.                                 ║
            ║                                 Le Clavier d’Or t’attend…                                ║
            ╚══════════════════════════════════════════════════════════════════════════════════════════╝
            """)

def quit_game() -> str:
    clear_screen()
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("\nSauvegarde en cours... Au revoir, héros du code !")
    exit()
    return ''  # Retourne une chaîne vide pour éviter l'affichage None


def return_to_menu() -> str:
    if input().lower() in ['return', 'menu']:
        print("Retour au menu principal...")
    return show_menu()