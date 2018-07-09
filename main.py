#https://github.com/herodote2242/projet5_openfoodfacts.git!/usr/bin/env python3
# -*- coding: Utf-8 -*

from menus import Menu
import config as c
from managers import ProductManager, StoreManager, FavoriteManager
import records


class Application:
    """This class constructs and displays the different menus
    during the life of the application."""

    def __init__(self):
        self.db = records.Database(c.DATABASE_URL)

    def start(self):
        """Main entry point of the demo application.
        The main menu is handled by self.handle_start_menu.
        """
        self.handle_start_menu()

    def handle_start_menu(self, entries={}):
        """Handler method for the main menu.
        1. Creates the menu.
        2. Adds menu entries.
        3. Displays the menu to the user.
        """
        menu = Menu('Démarrage', title='------ Menu ------',
            prompt='Veuillez choisir une option et appuyez sur Entrée : ')
        menu.add('Quel aliment souhaitez-vous remplacer ?',
            self.handle_categories_menu, '1')
        menu.add('Retrouver mes aliments substitués.',
            self.handle_favorites_menu, '2')
        menu.add("Quitter l'application.", self.handle_quit, 'q')
        menu.manager.ask(entries)

    def handle_categories_menu(self, entries={}):
        """Handler method for the categories menu.
        1. Creates the menu.
        2. Adds numeric menu entries from the categories
        stored in the config.py module.
        2. Adds keyword menu entries to quit the app and
        to return to the previous menu.
        3. Displays the menu to the user.
        """
        menu = Menu('Catégories', title="Les catégories de produits :",
            prompt='Sélectionnez la catégorie en entrant son numéro : ')
        for cat in c.CATEGORIES_TO_RECOVER.keys():
            menu.add(cat, self.handle_products_menu)
        menu.add("Quitter l'application.", self.handle_quit, 'q')
        menu.add("Revenir au menu principal.", self.handle_start_menu, 'm')
        menu.manager.ask(entries)

    def handle_products_menu(self, entries={}):
        """Handler method for the products menu.
        1. Creates the menu.
        2. Adds numeric menu entries for the (bad nutriscore')
        products selected from the category.
        2. Adds keyword menu entries to quit, return to the main
        menu or return to the previous menu.
        3. Displays the menu to the user.
        """
        menu = Menu('Produits', title="Les produits à remplacer :",
            prompt='Sélectionnez le produit en entrant son numéro : ')
        product_manager = ProductManager(self.db)
        for prod in product_manager.find_n_unhealthy_products_by_category(
                c.CATEGORIES_TO_RECOVER[entries['Catégories'].label]):
            menu.add(prod['product_name'], self.handle_substitutes_menu)
        menu.add("Quitter l'application.", self.handle_quit, 'q')
        menu.add("Revenir au menu principal.", self.handle_start_menu, 'm')
        menu.add("Revenir en arrière.", self.handle_categories_menu, 'b')
        menu.manager.ask(entries)

    def handle_substitutes_menu(self, entries={}):
        """Handler method for the substitutes menu.
        1. Creates the menu.
        2. Adds numeric menu entries for the (good nutriscore')
        products selected from the category
        2. Adds keyword menu entries to quit, return to the main
        menu or return to the previous menu.
        3. Displays the menu to the user.
        """
        menu = Menu('Substituts', title="Les substituts :",
            prompt="""Nous vous proposons ces produits
            de substitution, lequel choisissez-vous ? """)
        product_manager = ProductManager(self.db)
        for sub in product_manager.find_n_healthy_products_by_category(
                entries['Catégories'].label):
            menu.add(sub['product_name'], self.handle_substitute_selected_menu, data=sub)
        menu.add("Quitter l'application.", self.handle_quit, 'q')
        menu.add("Revenir au menu principal.", self.handle_start_menu, 'm')
        menu.add("Revenir en arrière.", self.handle_products_menu, 'b')
        menu.manager.ask(entries)

    def handle_substitute_selected_menu(self, entries={}):
        """Handler method for the selected substitute menu. It gives the
        possibilities of seeing the specific details of a product,
        saving it into the favorites, going back to the main menu,
        going back to the previous menu or quit.
        """
        menu = Menu('Description', title="Gestion du substitut :",
            prompt="""Pour ce produit de substitution,
            que souhaitez-vous faire ? """)
        favorite_manager = FavoriteManager(self.db)
        menu.add("Consulter la description détaillée du substitut.",
            self.handle_product_details, 'c')
        menu.add("Enregister le produit dans les favoris.",
            favorite_manager.add_favorite_from_product_code, 'e')
        menu.add("Quitter l'application.", self.handle_quit, 'q')
        menu.add("Revenir au menu principal", self.handle_start_menu, 'm')
        menu.add("Revenir en arrière.", self.handle_substitutes_menu, 'b')
        menu.manager.ask(entries)
        if menu.manager.menu_entry == 'e':
            self.handle_final_print()

    def handle_product_details(self, entries={}):
        """For a selected product, this function displays the name, nutriscore,
        url link to the openfoodfacts's website, the store(s) where it can be
        bought.
        """
        menu = Menu('Description détaillée', title="Description détaillée du substitut :",
            prompt="Voici les informations détaillées du substitut.")
        product_manager = ProductManager(self.db)
        menu.add("Nom du produit :", product_manager.find_product_description, 'd')
        menu.add("Quitter l'application.", self.handle_quit, 'q')
        menu.add("Revenir au menu principal.", self.handle_start_menu, 'm')
        menu.add("Revenir en arrière.", self.handle_substitute_selected_menu, 'b')
        menu.manager.ask(entries)

    def handle_final_print(self, entries={}):
        """Reminds of the different answers given until this conclusion
        point, in case of a substitute is saved as a favorite.
        """
        print(
            "Vous avez sélectionné:\n"
            f"- {entries['Démarrage'].label} ({entries['Démarrage'].id})\n"
            f"-- {entries['Catégories'].label} ({entries['Catégories'].id})\n"
            f"--- {entries['Produits'].label} ({entries['Produits'].id})\n"
            f"---- {entries['Substituts'].label} ({entries['Substituts'].id})\n"
            f"----- {entries['Description'].label} ({entries['Description'].id})\n"
        )
        # Then, the application gets back to the start menu.
        self.handle_start_menu(entries)

    def handle_favorites_menu(self, entries={}):
        """Handler method for the favorites menu.
        1. Creates the menu.
        2. Adds numeric menu entries for the favorites.
        2. Adds keyword menu entries to quit, return to the main menu.
        3. Displays the menu to the user
        """
        menu = Menu('Favoris', title="Mes Favoris :",
            prompt="Sélectionnez un favori en entrant son numéro : ")
        favorite_manager = FavoriteManager(self.db)
        for fav in favorite_manager.find_favorite_list():
            menu.add(fav, self.handle_selected_favorite_menu)
        menu.add("Quitter l'application.", self.handle_quit, 'q')
        menu.add("Revenir au menu principal.", self.handle_start_menu, 'm')
        menu.manager.ask(entries)

    def handle_selected_favorite_menu(self, entries={}):
        """The user has the possibility of exploring all the saved
        substitutes products. He has a view of all the substitutes,
        he can check their openfoodfacts'page from the favorite
        menu, and of course he can delete a substitute."""
        menu = Menu('Gestion', title="Gestion du favori :",
            prompt="Pour ce favori, que souhaitez-vous faire ? ")
        menu.add("""Consulter la description détaillée
            du favori.""",
            self.manager.find_favorite_description, 'c')
        menu.add("Supprimer le favori.", self.app.delete_favorite, 's')
        menu.add("Quitter l'application.", self.handle_quit, 'q')
        menu.add("Revenir au menu principal", self.handle_start_menu, 'm')
        menu.add("Revenir en arrière.", self.handle_favorites_menu, 'b')
        menu.manager.ask(entries)

    def handle_quit(self, entries):
        """This method says goodbye when the user quits."""
        print("A bientôt !")


def main():
    """Main entry point of the application."""
    main = Application()
    main.start()


if __name__ == "__main__":
    main()
