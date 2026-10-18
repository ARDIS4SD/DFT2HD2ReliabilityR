.. image:: https://github.com/ARDIS4SD/DFT2HD2ReliabilityR/blob/main/DFT2HD2ReliabilityR.svg


A quoi sert ce projet ?
========================
Le projet a pour de mettre à disposition des maintenanciers ayant 
des connaissances de base de programmation python, des fonctions 
permettant de construire des structures d'évaluation de la fiabilité 
(arbre de défaillance, diagramme de Hasse). En particulier, il vise à 
faire le calcul rapide par la méthode de satisfiabilité (coupe, lien, 
polynôme de fiabilité).

The project aims to provide maintainers with basic knowledge of python 
programming, functions to build reliability assessment structures (fault 
tree, Hasse diagram). In particular, it aims to do fast computation by the 
satisfiability method (cut, link, reliability polynomial).


Pourquoi ce projet est-il utile ?
=================================

L'évaluation de la fiabilité est un enjeux majeur de la maintenance qui elle même
est indispensable pour la productivité des entreprises. Le fait est que la maintenance 
moderne est assistée par ordinateur. Malheureusement, les logiciels de gestion de la 
maintenance sont assez onéreux. Il serait idéal de developper un projet open source 
permettant de pallier le problème de coût, et de developper un communauté collaborative 
qui fera rapidement avancer de façon ludique, les outils logiciels de pointe en matière
de maintenance.

Reliability assessment is a major maintenance issue which itself is essential for business 
productivity. The fact is that maintenance modern is computer-assisted. Unfortunately, maintenance 
management sofwares are quite expensive. It would be ideal to develop an open source project to 
overcome the cost problem, and to develop a collaborative community which will quickly advance in 
a playful way, the cutting-edge software tools for maintenance.

Comment démarrer ?
====================

Installation (dépendance dure : sympy)::

    pip install dft2hd2reliabilityr            # version publiée sur PyPI
    pip install "dft2hd2reliabilityr[viz]"     # + matplotlib/networkx (ViewGraph)
    # ou depuis ce dépôt :
    pip install .                              # dépendance sympy uniquement
    pip install -e ".[test]"                   # mode développement + pytest

Utilisation minimale — fiabilité d'un système OR 2 composants::

    from dft2hd2reliabilityr import FaultTree, DownHasseDiagram, One
    import sympy

    tree = FaultTree(3)
    tree.NewRelation(3, [1, 1, 0], [0, 0, 1])          # OR(c0, c1)
    h = DownHasseDiagram(tree, [0, 1], [sympy.Symbol("R1"), sympy.Symbol("R2")],
                         [[1], [1]], [One, One], [0], 1)
    print(h.GetPolyFiab())                             # -> poly de fiabilité

Où puis-je obtenir plus d'aide, si j'en ai besoin?
====================================================

En cas de besoin d'aide, bien vouloir contacter l'auteur Dr. Fotsa-Mbogne David Jaures à l'une 
des adresses jauresfotsa@gmail.com, david_jamesf@yahoo.fr et mjd.fotsa@univ-ndere.cm . Dr. Fotsa-Mbogne
est également disponible sur la page https://sites.google.com/site/mjdavidfotsa/home

If you need help, please contact the author Dr. Fotsa-Mbogne David Jaures at one addresses 
jauresfotsa@gmail.com, david_jamesf@yahoo.fr and mjd.fotsa@univ-ndere.cm. Dr. Fotsa-Mbogne is also 
available at https://sites.google.com/site/mjdavidfotsa/home

