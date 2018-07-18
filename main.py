#!/usr/bin/env python3
# -*- coding: Utf-8 -*

from menus import Menu
import config as c
from managers import ProductManager, StoreManager, FavoriteManager
import records


class Application:
    """This class constructs and displays the different menus
    during the life of the application.
    """

    def __init__(self):
        self.db = records.Database(c.DATABASE_URL)

    def start(self):
        """Main entry point of the application. The main menu
        is handled by self.handle_start_menu.
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
        menu.add('Retrouver mes substituts favoris.',
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
            # -tc- ajouter prod à data
            menu.add(prod['product_name'], self.handle_substitutes_menu, data=prod)
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
        prompt = (
            "Nous vous proposons ces produits de substitution, "
            "lequel choisissez-vous ? "
            )
        menu = Menu('Substituts', title="Les substituts :", prompt=prompt)
        product_manager = ProductManager(self.db)
        for sub in product_manager.find_n_healthy_products_by_category(
                entries['Catégories'].label):
            menu.add((sub['product_name']+" (Note nutitionnelle = "
                + sub['nutrition_grade_fr']+")"),
                self.handle_substitute_selected_menu, data=sub)
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
        prompt = "Pour ce produit de substitution, que souhaitez-vous faire ? "
        menu = Menu('Description', title="Gestion du substitut :",
            prompt=prompt)
        print("\nSubstitut sélectionné = "+entries['Substituts'].label)
        menu.add("Consulter la description détaillée du substitut.",
            self.handle_product_details, 'c')
        menu.add("Enregister le produit dans les favoris.",
            self.handle_record_substitute, 'e')
        menu.add("Quitter l'application.", self.handle_quit, 'q')
        menu.add("Revenir au menu principal", self.handle_start_menu, 'm')
        menu.add("Revenir en arrière.", self.handle_substitutes_menu, 'b')
        menu.manager.ask(entries)

    def handle_record_substitute(self, entries={}):
        """This method handles the process of saving the substitute
        into the favorite table.
        """
        # -tc- récupérer le code du produit
        product_code = entries['Produits'].data['code']
        substitute_code = entries['Substituts'].data['code']
        favorite_manager = FavoriteManager(self.db)
        # -tc- ajouter product_code en paramètre
        favorite_manager.add_favorite_from_product_code(substitute_code)
        print("\nVotre choix a été sauvegardé dans les favoris.")
        # Then, the application gets back to the start menu.
        self.handle_start_menu()

    def handle_product_details(self, entries={}):
        """For a selected product, this function displays the name, nutriscore,
        url link to the openfoodfacts's website, the store(s) where it can be
        bought.
        """
        menu = Menu('Description détaillée', title="Description détaillée",
            prompt="")
        product_manager = ProductManager(self.db)
        store_manager = StoreManager(self.db)
        substitute_code = entries['Substituts'].data['code']
        substitute = product_manager.find_product_description(substitute_code)
        print("\n--- Description détaillée ---\n")
        for sub in substitute:
            stores = store_manager.find_stores_by_product_code(substitute_code)
            stores = [store['name'] for store in stores]
            stores = ", ".join(stores)
            print("Nom du produit : "+str(sub['product_name']))
            print("Code du produit : "+str(sub['code']))
            print("Marque du produit : "+sub['brand'])
            print("Lien Openfoodfacts : "+sub['url_link'])
            print("Note nutritionnelle : "+sub['nutrition_grade_fr'])
            print("Magasin(s) où l'acheter : "+str(stores))
        menu = Menu('Description détaillée',
            prompt="Que souhaitez-vous faire ? ")
        menu.add("Quitter l'application.", self.handle_quit, 'q')
        menu.add("Revenir au menu principal.", self.handle_start_menu, 'm')
        menu.add("Revenir en arrière.",
            self.handle_substitute_selected_menu, 'b')
        menu.manager.ask(entries)

    def handle_favorites_menu(self, entries={}):
        """Handler method for the favorites menu.The user has the possibility
        of exploring all the saved substitutes products.
        1. Creates the menu.
        2. Adds numeric menu entries for the favorites.
        2. Adds keyword menu entries to quit, return to the main menu.
        3. Displays the menu to the user.
        """
        prompt = "Sélectionnez un favori en entrant son numéro : "
        menu = Menu('Favoris', prompt=prompt)
        favorite_manager = FavoriteManager(self.db)
        favorite_list = favorite_manager.find_favorite_list()
        print('\n--- Favoris enregistrés : ---\n')
        if not favorite_list:
            print("Il n'y a pas encore de favoris sauvegardés.\n")
        for fav in favorite_list:
            menu.add(fav['product_name'], self.handle_selected_favorite_menu,
                data=fav)
        menu.add("Quitter l'application.", self.handle_quit, 'q')
        menu.add("Revenir au menu principal.", self.handle_start_menu, 'm')
        menu.manager.ask(entries)

    def handle_selected_favorite_menu(self, entries={}):
        """The user has a view of all the favorites,
        he can choose to check their details with the favorite details
        menu, and of course he can delete a substitute if needed.
        """
        favorite_manager = FavoriteManager(self.db)
        product_code = entries['Favoris'].label
        menu = Menu('Gestion', title="Gestion du favori :",
            prompt="Pour ce favori, que souhaitez-vous faire ? ")
        menu.add("""Consulter les détails du favori.""",
            self.handle_favorite_details, 'c')
        menu.add("Supprimer le favori.", self.handle_delete_favorite, 's')
        menu.add("Quitter l'application.", self.handle_quit, 'q')
        menu.add("Revenir au menu principal", self.handle_start_menu, 'm')
        menu.add("Revenir en arrière.", self.handle_favorites_menu, 'b')
        menu.manager.ask(entries)

    def handle_delete_favorite(self, entries={}):
        """This function is called when the user wants to delete a
        favorite from the favorite list.
        """
        favorite_code = entries['Favoris'].data['code']
        favorite_manager = FavoriteManager(self.db)
        favorite_manager.delete_from_favorite(favorite_code)
        print("\nVotre choix a été supprimé des favoris.")
        # Then, the application gets back to the start menu.
        self.handle_start_menu()

    def handle_favorite_details(self, entries={}):
        """Handler in charge of displaying all the favorite'details :
        the name, product code, brand, url link, nutrition grade
        and of course the retail(s) where to find the product.
        """
        print("\n--- Détails du favori ---\n")
        product_manager = ProductManager(self.db)
        store_manager = StoreManager(self.db)
        favorite_code = entries['Favoris'].data['code']
        favorite = product_manager.find_product_description(favorite_code)
        for fav in favorite:
            stores = store_manager.find_stores_by_product_code(favorite_code)
            stores = [store['name'] for store in stores]
            stores = ", ".join(stores)
            print("Nom du produit : "+str(fav['product_name']))
            print("Code du produit : "+str(fav['code']))
            print("Marque du produit : "+fav['brand'])
            print("Lien Openfoodfacts : "+fav['url_link'])
            print("Note nutritionnelle : "+fav['nutrition_grade_fr'])
            print("Magasin(s) où l'acheter : "+str(stores))
        menu = Menu('Détails du favori', prompt="Que souhaitez-vous faire ? ")
        menu.add("Quitter l'application.", self.handle_quit, 'q')
        menu.add("Revenir au menu principal.", self.handle_start_menu, 'm')
        menu.add("Revenir en arrière.", self.handle_selected_favorite_menu,
            'b')
        menu.manager.ask(entries)

    def handle_quit(self, entries):
        """This method says goodbye when the user quits.
        """
        print("A bientôt !")


def main():
    """Main entry point of the application.
    """
    main = Application()
    main.start()


if __name__ == "__main__":
    main()
