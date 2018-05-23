#!/usr/bin/env python3
# -*- coding: Utf-8 -*

import records

"""This is the main application : it asks the user several questions
and the user is able to answer in order to search products, see products, 
save them into his favorites and see the list of favorites."""

# User opens the app, the app shows:
print("1 - Quel aliment souhaitez-vous remplacer ?")
print("2 - Retrouver mes aliments substitués.")

#User chooses 1:
if int(input()) = 1:
    print("Sélectionnez la catégorie :")
    #pour n catégories, afficher un chiffre de 1 à n devant chacune
    if int(input()) = #number of category:
        print("Catégorie sélectionnée : "xxxx"")
        print("Sélectionnez l'aliment :")
        #pour n aliments, afficher un chiffre de 1 à n devant chacun
        print("Aliment sélectionné : "yyyy"")
        query("""USE projet5;""")
        query("""SELECT * FROM product WHERE category = "xxxx" AND nutrition_grade_fr = 'a'
            OR nutition_grade_fr = 'b' LIMIT 1""")

#User chooses 2:
elif int(input()) = 2:
    print("Mes aliments substitués :")
    query("""affichage de l'historique des aliments substitués""")

#User hits an other key:
else:
    print("Veuillez entrer votre choix : 1 ou 2.")
