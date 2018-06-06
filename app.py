#!/usr/bin/env python3
# -*- coding: Utf-8 -*

import records
import requests
import config as c


class AppRunner:
    """This is the main application : it asks the user several questions
    and the user is able to answer in order to search products, see products, 
    save them into his favorites and see the list of favorites."""

    def __init__(self, connection):

        self.db = connection
        self.db.query(f"""USE {c.DATABASE_NAME};""")

    def runapp(self, connection):

        # Menu loop :
        menu_loop = 1
        while menu_loop == 1:
            print('--------MENU--------')
            print("1 - Quel aliment souhaitez-vous remplacer ?")
            print("2 - Retrouver mes aliments substitués.")
            print("q - Quitter l'application.")
            user_answer = input()
        
            # The user chooses to switch a product.
            if user_answer == '1':
                # Category loop :
                category_loop = 1
                menu_loop = 0
                while category_loop == 1:
                    print("Sélectionnez la catégorie en entrant son numéro:")
                    print(c.CATEGORIES_TO_RECOVER)
                    print("m - Revenir au menu")
                    print("q - Quitter l'application")
                    category_selected = input()

                    # The user chooses one of the category.
                    if category_selected in ("1", "2", "3", "4", "5", "6"):

                        # Product selection :
                        print("Catégorie sélectionnée : ", c.CATEGORIES_TO_RECOVER[category_selected])
                        print("Sélectionnez l'aliment en entrant son numéro :")
                        self.db.query(f"""USE {c.DATABASE_NAME};""")
                        rows = self.db.query(f"""SELECT DISTINCT product_name FROM product
                            JOIN product_category ON product_category.product_code = product.code
                            JOIN category ON product_category.category_id = category.id
                            WHERE nutrition_grade_fr IN ('e', 'd')
                            AND category.name = :catname
                            ORDER BY RAND() LIMIT {c.NUMBER_OF_BAD_FOOD};""",
                            catname=c.CATEGORIES_TO_RECOVER[category_selected])
                        print("b - Revenir en arrière")
                        print("m - Revenir au menu")
                        print("q - Quitter l'application")
                        for row in rows:
                            print(row["product.product_name"])

                        product_selected = input()

                        # The user chooses one product of the list.
                        #if product_selected == query pour une sélection de produit

                        # The user wants to get back at the category selection.
                        if product_selected == 'b':
                            category_loop = 1
                            menu_loop = 0

                        # The user wants to get back at the menu selection.
                        if product_selected == 'm':
                            category_loop = 0
                            menu_loop = 1

                        # The user wants to quit.
                        if product_selected == 'q':
                            category_loop = 0
                            menu_loop = 0
                            pass

                    # The user gets back to the menu.
                    elif category_selected == "m":
                        category_loop = 0
                        menu_loop = 1
            
                    # The user chooses to quit.
                    elif category_selected == 'q':
                        category_loop = 0
                        menu_loop = 0
                        pass

                    # The user's input is out of concern.
                    else:
                        # Back to the menu.
                        print("Votre saisie ne correspond pas aux options, veuillez réessayer.")
                        menu_loop = 1

            # The user chooses to see all the previous saved substitutes.
            elif user_answer == '2':
                menu_loop = 0
                print("Mes aliments substitués :")
                #faire une query("""affichage de l'historique des aliments substitués (favoris) + consulter la fiche et suivre url""")
            
            #User chooses to quit.
            elif user_answer == 'q':
                # Application quits.
                menu_loop = 0
                pass

            #User hits an other key:
            else:
                # Back to menu.
                print("Veuillez entrer votre choix : 1 ou 2.")
                menu_loop = 1

#Tests:
if __name__=="__main__":
    connection = records.Database(c.DATABASE_URL)
    runner = AppRunner(connection)
    runner.runapp(connection)
