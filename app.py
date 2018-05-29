#!/usr/bin/env python3
# -*- coding: Utf-8 -*

import records
import config as c

"""This is the main application : it asks the user several questions
and the user is able to answer in order to search products, see products, 
save them into his favorites and see the list of favorites."""

# User opens the app, the app shows:
print("1 - Quel aliment souhaitez-vous remplacer ?")
print("2 - Retrouver mes aliments substitués.")

#User chooses 1:
if input() == "1":
    print("Sélectionnez la catégorie :")
    print(c.CATEGORIES_TO_RECOVER)
    category_selected = int(input())
    print("Catégorie sélectionnée : ", c.CATEGORIES_TO_RECOVER[category_selected])
    print("Sélectionnez l'aliment :")


    #print("Sélectionnez l'aliment :")
    #pour n aliments, afficher un chiffre de 1 à n devant chacun
    #print("Aliment sélectionné : "yyyy"")
    #query("""USE projet5;""")
    #query("""SELECT * FROM product WHERE category = "xxxx" AND nutrition_grade_fr = 'a'
    #    OR nutition_grade_fr = 'b' LIMIT 3""")

#User chooses 2:
elif input() == "2":
    print("Mes aliments substitués :")
    #faire une query("""affichage de l'historique des aliments substitués""")

#User hits an other key:
else:
    print("Veuillez entrer votre choix : 1 ou 2.")
