from intro import hello, welcome_message, mession_message, titre
from menu import show_menu, get_user_choice

def main():
    hello()
    input()
    titre()
    input()
    welcome_message()
    input("Appuyez sur Entrée pour continuer...") 
    mession_message()
    input() 
    
    show_menu()
    get_user_choice()
    
    
if __name__ == "__main__":
    main()