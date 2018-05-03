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
    print("#categories to be shown")
    if int(input()) = #number of category:
        print("Sélectionnez l'aliment :")
        print("#aliments to be shown")
        query("""USE projet5;""")
        query("""SELECT #use the previous answers to construct the request""")


#User chooses 2:
elif int(input()) = 2:
    print("Mes aliments substitués :")
    print("#favorites to be shown")

#User hits an other key:
else:
    print("Veuillez entrer votre choix : 1 ou 2.")


