from datetime import datetime  # Pour gérer les temps et dates
from traceback import print_exc  # Pour avoir le message d'erreur en entier
import pickle  # Pour stocker les données

from parking import Parking
from vehicle import Vehicle, Owner


def manage_vehicles(vehicles, owners, parking):
    """
    gère les véhicules en ligne de commande
    :param vehicles: set des véhicules existants
    :param owners: set des clients ayant un ou plusieurs véhicule(s) abonné(s)
    :param parking: l'objet parking
    :return: None
    """
    action = input("Créer (c)/ Suprimmer (s)/ Info (i)")
    if action == "i":
        for v in vehicles:
            print(v)
    elif action == "c":
        plaque = input("plaque d'immatriculation : ")
        for i in vehicles:
            if plaque == i.licence_plate:
                return print("Ce numéro d'immatriculation est déjà assigné")
        abonnement = input("abonnement (vide si aucun sinon entrer le nombre de mois) : ")
        if abonnement != "":
            try:
                abonnement = int(abonnement)
            except ValueError:
                print("Veuillez rentrer un entier pour le temps d'abonnement")
            else:
                name = input("nom du propriétaire : ")
                owner = None
                for i in owners:
                    if name == i.last_name:
                        owner = i
                if owner == None:
                    print("le propriétaire n'as pas été trouver")
                else:
                    new_vehicle = Vehicle(plaque, owner, True, abonnement, parking)
                    vehicles.add(new_vehicle)
                    parking.prime_vehicles.add(new_vehicle)
        else:
            vehicles.add(Vehicle(plaque))
    elif action == "s":
        plaque = input("plaque d'immatriculation : ")
        vehicle = None
        for v in vehicles:
            if plaque == v.licence_plate:
                vehicle = v
                break
        if vehicle != None:
            if vehicle in parking.vehicles:
                print("La voiture se trouve actuellement dans le parking, si vous voulez supprimez ce véhicule veuillez d'abord le sortir du parking")
            else:
                if parking.remove_prime_vehicle(vehicle):
                    vehicles.remove(vehicle)
        else:
            print("Ce véhicule n'existe pas")


def manage_parking(parking, vehicles):
    action = input("Entrée (e)/ sortie (s)/ info (i)/ afficher étages (p) : ")
    if action == "i":
        print(parking)
    elif action == "p":
        parking.print_parking()
    else:
        plaque = input("Plaque d'immatriculation du véhicule : ")
        vehicle = None
        for i in vehicles:
            if plaque == i.licence_plate:
                vehicle = i
        if vehicle == None:
            print("Le véhicule n'as pas été trouver")
        else:
            if action == "e":
                parking.add_vehicle(vehicle)
            elif action == "s":
                try:
                    parking.remove_vehicle(vehicle)
                except ValueError:
                    print("Le véhicule n'est pas dans le parking")


def reset_parking():
    try:
        nbr_spot = int(input("Nombres de places de parking : "))
        price = float(input("tarif : "))
        nbr_floor = int(input("Nombres d'étages (rez-de-chaussé compris) : "))
    except TypeError:
        print("Veuillez entrer des nombres entiers")
    else:
        new_parking = Parking(nbr_spot, price, nbr_floor)
        new_parking.print_parking()
        with open("data.pickle", "wb") as f:
            pickle.dump(new_parking, f, protocol=pickle.HIGHEST_PROTOCOL)
        return new_parking

def init():
    with open("data.pickle", "rb") as datafile:
        parking = pickle.load(datafile)
    vehicles = {v for v in parking.vehicles}
    owners = set()
    for v in parking.prime_vehicles:
        if not v.still_subscribed():
            time_passed = (datetime.now() - v.subscription_end).days
            print(f"L'abonnement du véhicule immatriculé {v.licence_plate} est expiré depuis {time_passed} jour(s)")
            if time_passed > 30:
                print("Son abonnement étant expiré depuis plus d'un mois, le véhicule est donc supprimé")
                continue
            else:
                print(f"Son propriétaire est {str(v.owner)} et son adresse mail est {v.owner.email}")
        vehicles.add(v)
        owners.add(v.owner)
    return (parking, vehicles, owners)


def main():
    try:
        parking, vehicles, owners = init()
        while True:
            action = input(
                "Créer un client (c)/ Gérer les véhicules (v)/ Gérer le parking (p)/ Quitter le programme (q) : ")
            if action == "c":
                nom = input("nom : ")
                prenom = input("prénom : ")
                mail = input("mail : ")
                owners.add(Owner(prenom, nom, mail))
            elif action == "v":
                manage_vehicles(vehicles, owners, parking)
            elif action == "p":
                manage_parking(parking, vehicles)
            elif action == "q":
                break
            elif action == "r":
                print("Cette action effaceras toute les données sur le parking")
                action = input("Voulez-vous continuez ? (oui/non) : ")
                if action == "oui":
                    parking = reset_parking()
            else:
                print("Mauvaise entrée")
    except FileNotFoundError:
        print("ERREUR : mauvais nom de fichier ou fichier non-existant")
    except Exception:
        with open("data.pickle", "wb") as f:
            pickle.dump(parking, f, protocol=pickle.HIGHEST_PROTOCOL)
        print_exc()
    else:
        with open("data.pickle", "wb") as f:
            pickle.dump(parking, f, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
