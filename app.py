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

        # User opens the app, the app shows:
        print("1 - Quel aliment souhaitez-vous remplacer ?")
        print("2 - Retrouver mes aliments substitués.")
        user_answer = input()

        #User chooses 1:
        if user_answer == "1":
            print("Sélectionnez la catégorie :")
            print(c.CATEGORIES_TO_RECOVER)
            category_selected = int(input())
            print("Catégorie sélectionnée : ", c.CATEGORIES_TO_RECOVER[category_selected])
            print("Sélectionnez l'aliment :")
            self.db.query(f"""USE {c.DATABASE_NAME};""")
            # la requête ci dessous fonctionne dans mysql. reste à la faire fonctionner depuis
            #python et ajouter le filtre sur la catégorie sélectionnée
            self.db.query("""SELECT DISTINCT product_name FROM product
                WHERE nutrition_grade_fr IN ('e', 'd') 
                AND ORDER BY RAND() LIMIT 10;""")
            # associer un numéro à chacun des 10 résultats

            # The user chooses the good to be replaced.
            #good_selected = int(input())
            #print("Nous vous proposons ces substituts avec un meilleur score nutritionnel")
            #self.db.query("""SELECT DISTINCT product_name FROM ... nutri IN ('a', 'b') ...""")

        #User chooses 2:
        elif user_answer == "2":
            print("Mes aliments substitués :")
            #faire une query("""affichage de l'historique des aliments substitués""")

        #User hits an other key:
        else:
            print("Veuillez entrer votre choix : 1 ou 2.")


#Tests:
if __name__=="__main__":
    connection = records.Database(c.DATABASE_URL)
    runner = AppRunner(connection)
    runner.runapp(connection)