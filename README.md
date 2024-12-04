# Projet-dev-II-2tl1-6
[//]: # (Use this for colored text: ${\textsf{\color{red}text}}$)
## Table of contents

+ [Résumé du projet](#résumé-du-projet)
+ [MVP](#mvp)
+ [États actuelle](#états-actuelle)
+ [À implémenter](#à-implémenter)
+ [Interface graphique](#interface-graphique)

## Résumé du projet

Le système est une solution locale et intuitive pour gérer un parking sur 5 étages. Il permet de suivre en temps réel l’occupation des **places de stationnement** (voitures et deux-roues), d’enregistrer manuellement les **entrées et sorties**, et de **calculer automatiquement les paiements** selon les tarifs ou abonnements. 

L’interface affiche une vue claire des **zones et places disponibles**, gère les abonnements (avec alertes pour expiration), et génère des **rapports statistiques** sur l’occupation et les revenus. 

Tout est pensé pour simplifier la gestion quotidienne sans matériel supplémentaire, tout en offrant une expérience fluide et organisée pour le propriétaire et les clients.

## **MVP**

Le MVP permet, via l'interface de texte, les actions suivantes:

+ créer un client
+ créer un véhicule (seulement 4 roues et pas d'abonnement)
+ rentrer un véhicule dans le parking et affiche la date et l'heure
+ sortir un véhicule dans le parking et affiche la date et l'heure ainsi que le paiements à effectuer
+ afficher les véhicules stationnant actuellement dans le parking ainsi que le propriétaire et la date et l'heure d'arrivé


## États actuelle

Le parking est composé de plusieurs étages (rez-de-chaussé compris).  Chaque étage est composé de 5 zones de 10 places.  Chaque place est un noeuds (class Node) représentant une place et ayant un identifiant composé de l'étage, de la zone et de la place (ex: 1B5, RE0,...).  Une place peut avoir 5 états différents:

+ Réserver (place réservé par un abonné)
+ 2 roues (pour les véhicules 2 roues avec tarif réduit)
+ 2 roues réservé (par un abonné 2-roues)
+ Libre (tarif classic)

Un étage est représenté par la matrice suivante:
```
[
 Zone A [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
 Zone B [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
 Zone C [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
 Zone D [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
 Zone E [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                                      ]
```

Voici les actions disponibles:

+ Création d'un abonnement lors de la création d'un véhicule (nécessite un client) → Dans GUI
+ Supprimer un véhicule (si il n'est pas dans le parking) → Quand un abonnement n'as pas été renouvelé (${\textsf{\color{orange}à implémenter dans le GUI}}$)
+ Informations sur les véhicules abonnés → Dans GUI
+ Afficher l'état de chaque étage du parking → Dans GUI (${\textsf{\color{orange}couleurs à implémenter}}$)
+ Faire un reset du parking → Lors d'une erreur critique (à implémenter dans le GUI)

L'affichage de la date et de l'heure claire → ${\textsf{\color{orange}À utiliser lors des affichages dans GUI}}$

Le parking est enregistré dans un fichier (data.pickle) permettant de garder l'état actuelle du parking ainsi que les véhicules stationnant dans le parking et les véhicules abonnés.
Lors du lancement du programme, ce fichier est utilisé pour charger l'objet parking et par la suite dresser la liste des véhicules et propriétaires actuellement dans le programme. Le format de fichier étant du binaire, il n'est pas lisible par un humain. En cas d'erreur dans le programme, le parking est toujours enregistré dans le fichier (hormis si l'erreur provient du nom du fichier). Si l'erreur provient du fichier (fichier vide), le programme propose de créer un nouveau parking et l'enregistre dans le fichier.

## À implémenter

### Majeures

+ Les véhicules 2 roues (tarifs, abonnement, places 2 roues,...)
+ Terminer l'interface graphique (voir [Interface graphique](#interface-graphique) pour la présentation ou [GUI](#gui) pour ce qu'il faut implémenter)
+ ${\textsf{\color{orange}Transférer la boucle while True du main (le MVP) dans les différentes classes (Vehicle, Parking, GUI)}}$

### Mineurs

+ Ralonger l'abonnement (dans class Vehicle)
+ Faire un résumer de la journée lors de la fermeture du programme (éventuellement reprendre le dernier résumer si la même date)
+ Enregistrer le résumer de la journée dans un fichier (un simple fichier txt devrait suffire)

### GUI

+ Permettre de réserver des places (idéalement dans le form lors d'un abonnement et/ou en cliquant sur la place voulu)
+ ${\textsf{\color{red}Rajouter une voiture sans abonnement dans le parking}}$
+ ${\textsf{\color{red}Sortir une voiture sans abonnement et afficher le montant à payer}}$
+ Alerte lorsque le parking est presque plein via fenêtre pop-up
+ Afficher le résumer de la journée dans le tab dédié
+ Colorer les places réservées (et 2-roues)
+ ${\textsf{\color{orange}Modifier le nombre de places disponibles}}$ (-1 par véhicule abonnée, -1 par véhicule classique dans le parking et +1 quand une voiture classique sort du parking)

## Interface graphique

1. **Tableau de bord principal** : 
   - Une grande vue d'ensemble du parking, montrant chaque étage avec les places représentées par des petites cases colorées : par exemple, vert pour libre, rouge pour occupé, et peut-être une couleur spéciale (bleu ?) pour les places réservées aux abonnés.
   - À chaque instant, je pourrais voir l’état de chaque place sans avoir besoin de chercher.

2. **Section d’enregistrement des entrées et sorties** :
   - Un formulaire simple où je pourrais entrer le numéro de plaque d'immatriculation et la place où le client se gare. Quand le client part, je retrouverais sa plaque et noterais l’heure de sortie pour calculer automatiquement le montant.
   - Un bouton "Enregistrer sortie" qui mettrait la place à jour, libérant automatiquement celle-ci pour le prochain client.

3. **Gestion des abonnements** :
   - Une liste des abonnés avec leurs informations (plaque, type d’abonnement, date d’expiration). Ça me permettrait de rapidement vérifier si un client est abonné et de voir s’il est à jour avec son abonnement.
   - Un système de notification ou un rappel pour les abonnements proches de l’expiration, pour que je puisse en informer les clients à l’avance.

4. **Zone des alertes** :
   - Une petite zone où des alertes s’afficheraient, par exemple si le parking est à 90% de sa capacité ou plus, ou si une anomalie se produit, comme un paiement en attente.

5. **Statistiques et rapports** :
   - Une page dédiée où je pourrais consulter les statistiques, par exemple, les périodes de forte affluence, les revenus totaux par semaine, mois, etc.
   - Des graphiques simples pour voir les tendances d’occupation et les revenus. Pas besoin de quelque chose de complexe, juste assez pour que je puisse analyser l’activité du parking facilement.

En résumé, une interface visuelle, colorée, et organisée par sections pour naviguer sans perdre de temps.

## Chatbot

Pour voire l'échange avec le chatbot cliquer [ici](https://chatgpt.com/share/67334a38-3b74-8008-935a-d0c5ae250b18)
