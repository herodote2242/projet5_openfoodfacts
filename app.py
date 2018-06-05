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
            print("1 - Quel aliment souhaitez-vous remplacer ?")
            print("2 - Retrouver mes aliments substitués.")
            print("q - Quitter l'application.")
            user_answer = input()
        
            # The user chooses to switch a product.
            if user_answer == '1':
                # Category selection :
                print("Sélectionnez la catégorie en entrant son numéro:")
                print("m - Revenir au menu")
                print("q - Quitter l'application")
                print(c.CATEGORIES_TO_RECOVER)
                category_selected = input()

                # The user chooses one of the category.
                if category_selected in ("1", "2", "3", "4", "5", "6"):

                    # Product selection :
                    if product_choice == 1:
                        print("Catégorie sélectionnée : ", c.CATEGORIES_TO_RECOVER[category_selected])
                        print("Sélectionnez l'aliment en entrant son numéro :")
                        print("b - Revenir en arrière")
                        print("m - Revenir au menu")
                        print("q - Quitter l'application")
                        self.db.query(f"""USE {c.DATABASE_NAME};""")            
                        rows = self.db.query(f"""SELECT DISTINCT product_name FROM product
                            JOIN product_category ON product_category.product_code = product.code
                            JOIN category ON product_category.category_id = category.id
                            WHERE nutrition_grade_fr IN ('e', 'd')
                            AND category.name = :catname
                            ORDER BY RAND() LIMIT {c.NUMBER_OF_BAD_FOOD};""",
                            catname=c.CATEGORIES_TO_RECOVER[category_selected])
                        for row in rows:
                            print(row["product.product_name"])

                # The user gets back to the menu.
                elif category_selected == "m":
                    menu_loop = 1
                    # créer pour retourner au menu
        
                # The user wants to quit.
                elif category_selected == 'q':
                    pass

                    # The user's input is out of concern.
                else:
                    print("Votre saisie ne correspond pas aux options, veuillez réessayer.")
                        # Back to the same category selection menu.

            # The user chooses to see all the previous saved substitutes.
            elif user_answer == '2':
                print("Mes aliments substitués :")
                menu_loop = 1
                #faire une query("""affichage de l'historique des aliments substitués (favoris) + consulter la fiche et suivre url""")
            
            #User chooses to quit.
            elif user_answer == 'q':
                # Application quits.
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
