import mysql
from termcolor import colored
from Database.create import database
from Database.database import Database
from Database.request import Request
from Class.category import Category
from Class.product import Product
from Class.favorite import Favorite


def main():

    init = Main()
    init.main_menu()


class Main:
    """implementation of different menus"""

    def __init__(self):
        """set up attributes"""
        self.green_line = colored("-----------------------------------------", "green")
        self.red_line = colored("-----------------------------------------", "red")
        self.touch_error = colored("Pour faire une sélection. Tapez son numéro", "red")
        self.database = Database()
        self.list_product = []
        self.cat = 0
        self.sub = 0

    def main_menu(self):
        """first menu et creation of database in second choice"""
        print(self.green_line)
        print(colored("1. Utiliser application", "yellow",))
        print(colored("2. Supression/Création de la database", "magenta"))
        print(colored("0. Quitter l'application ", "red"))
        print(self.green_line)
        choice_main = input(colored("\n ---> ", "green"))
        try:
            choice_main = int(choice_main)
        except ValueError:
            choice_main = -1
        if choice_main == 1:
            self.api_menu()
        elif choice_main == 2:
            database()
            data = Database()
            request = Request()
            request.create_database(data)
            self.main_menu()
        elif choice_main == 0:
            self.bye()
        else:
            print(self.touch_error)
            self.main_menu()

    def api_menu(self):
        """second menu, use the application"""
        print(self.green_line)
        print(colored("1. Choix d'une catégorie", "yellow"))
        print(colored("2. Afficher sauvegarde", "yellow"))
        print(colored("0. Quitter le programme", "red"))
        print(self.green_line)
        choice_api = input(colored("\n ---> ", "green"))
        print(self.green_line)
        try:
            choice_api = int(choice_api)
        except ValueError:
            choice_api = -1
        if choice_api == 1:
            self.cat_menu()
        elif choice_api == 2:
            check = self.database.check_favorite()
            if check == 0:
                print(colored("*.backup is empty", "yellow"))
                print(self.green_line)
                self.api_menu()
            else:
                prod = self.database.search_favorite()
                for i, values in enumerate(prod):
                    favorite = Favorite(
                        prod[i][0], prod[i][1], prod[i][2], prod[i][3], prod[i][4],
                    )
                    print(
                        i + 1,
                        ".\t",
                        favorite.nutriscore,
                        "\t",
                        favorite.name,
                        "\n",
                        "..\t",
                        favorite.url,
                        "\n",
                        "..\t",
                        "store:",
                        favorite.market,
                        "\n",
                        "......................................",
                    )
                print(self.green_line)
                self.api_menu()
        elif choice_api == 0:
            self.bye()
        else:
            print(self.touch_error)
            self.api_menu()

    def cat_menu(self):
        """categorie's menu, choice categorie"""
        cat = self.database.search_categorie()
        for i, values in enumerate(cat):
            category = Category(cat[i][0], cat[i][1])
            print(i + 1, category.name)
        print(self.green_line)
        print(colored("Choix de la catégorie", "yellow"))
        cat = input(colored("\n ---> ", "green"))
        try:
            cat = int(cat)
        except ValueError:
            print(self.red_line)
            print(self.touch_error)
            print(self.red_line)
            self.cat_menu()
        if cat <= i + 1:
            self.prod_menu(cat, i)
        else:
            print(self.red_line)
            print(self.touch_error)
            print(self.red_line)
            self.cat_menu()

    def prod_menu(self, cat, i):
        """product menu, product choice"""
        list_nb = []
        prod = self.database.search_product(cat)
        for i, values in enumerate(prod):
            product = Product(
                prod[i][0], prod[i][1], prod[i][2], prod[i][3], prod[i][4],
            )
            print(
                i + 1, ".\t", product.nutriscore, "\t", product.name,
            )
            list_nb.append(i + 1)
        print(colored("Choix d'un produit", "yellow"))
        choice_prod = input(colored("\n ---> ", "green"))
        try:
            choice_prod = int(choice_prod)
        except ValueError:
            choice_prod != list_nb
        if choice_prod in list_nb:
            self.sub_menu(cat)
        else:
            print(self.red_line)
            print(self.touch_error)
            print(self.red_line)
            self.prod_menu(cat, i)

    def sub_menu(self, cat):
        """substitute menu, substitute choice"""
        list_nb = []
        subst = self.database.search_better_products(cat)
        for i, values in enumerate(subst):
            product = Product(
                subst[i][0], subst[i][1], subst[i][2], subst[i][3], subst[i][4],
            )
            print(
                i + 1, ".\t", product.nutriscore, "\t", product.name,
            )
            list_nb.append(i + 1)
        print(colored("Choix d'un substitut", "yellow"))
        sub = input(colored("\n ---> ", "green"))
        try:
            sub = int(sub)
        except ValueError:
            sub != list_nb
        if sub in list_nb:
            self.save_menu(cat, sub)
        else:
            print(self.touch_error)
            self.sub_menu(cat)

    def save_menu(self, cat, sub):
        """save menu, Adding substitute in the database"""
        print(colored("Voulez-vous sauvegarder: 1(Oui) 2(Non)", "yellow"))
        choice_save = input(colored("\n ---> ", "green"))
        try:
            choice_save = int(choice_save)
        except ValueError:
            choice_save = -1
        if choice_save == 1:
            try:
                self.database.save_favorite(cat, sub)
                print(self.red_line)
                print(colored("favoris enregistrer", "green"))
                print(self.red_line)
                self.main_menu()
            except mysql.connector.errors.IntegrityError:
                print(self.red_line)
                print(colored("Le favoris est déjà enregistrer", "yellow"))
                print(self.red_line)
                self.main_menu()
        elif choice_save == 2:
            self.main_menu()
        else:
            print(self.red_line)
            print(self.touch_error)
            print(self.red_line)
            self.save_menu(cat, sub)

    def bye(self):
        """say goodbye"""
        print(colored("**********************************************", "green"))
        print(colored("----------------------------------------------", "cyan"))
        print(colored("                  Au revoir !                 ", "yellow"))
        print(colored("----------------------------------------------", "cyan"))
        print(colored("**********************************************", "green"))
        quit()


if __name__ == "__main__":
    main()
