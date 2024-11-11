from datetime import datetime  # Pour gérer les temps et dates
from traceback import print_exc  # Pour avoir le message d'erreur en entier
import pickle  # Pour stocker les données


class Owner:
    def __init__(self, first_name: str, last_name: str, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __str__(self):
        return self.first_name + " " + self.last_name


class Vehicle:
    def __init__(self, licence_plate: str, owner: Owner = None, subscribed: bool = False, sub_time: int = 0):
        self.licence_plate = licence_plate
        self.owner = owner
        self.start_time = None
        self.__subscribed = subscribed
        if subscribed:
            self.last_subscription, self.subscription_end = self.calc_sub_time(sub_time)
        else:
            self.last_subscription = None
            self.subscription_end = None

    def __str__(self):
        if self.__subscribed:
            return f"Plaque d'immatriculation : {self.licence_plate}\nPropriétaire du véhicule : {self.owner}\nAbonnement valide jusqu'au {self.subscription_end.strftime('%d/%m/%Y')} à {self.subscription_end.strftime('%H:%M')}"
        else:
            return f"Plaque d'immatriculation : {self.licence_plate}\nDurée de stationnement actuelle : {(datetime.now() - self.start_time).seconds // 60} minutes"

    def __repr__(self):
        return str({self.licence_plate})

    def calc_sub_time(self, sub_time):
        date = datetime.now()
        last_subscription = date
        year = date.year + sub_time // 12
        month = date.month + sub_time % 12
        if month > 12:
            month = 1
            year += 1
        subscription_end = datetime(year, month, date.day, date.hour, date.minute, date.second,
                                         date.microsecond)
        return (last_subscription, subscription_end)

    def still_subscribed(self):
        return self.subscription_end > datetime.now()


    def become_subscribed(self, sub_time):
        if self.__subscribed:
            print(f"Déjà abonné jusqu'au {self.subscription_end.strftime('%d/%m/%y')} à {self.subscription_end.strftime('%H:%M')}")
        else:
            self.__subscribed = True
            self.last_subscription, self.subscription_end = self.calc_sub_time(sub_time)

    def revoke_subscribed(self):
        if not self.__subscribed:
            print("Ce véhicule n'est actuellement pas abonné")
        else:
            self.__subscribed = False
            self.subscription_end = None

    def detail_owner(self):
        print(self.owner)


class Parking:
    def __init__(self, nbr_parking_spot_tot: int, price_parking_spot: float):
        self.nbr_parking_spot = nbr_parking_spot_tot
        self.nbr_parking_spot_free = nbr_parking_spot_tot
        self.__price_parking_spot = price_parking_spot
        self.vehicles = []
        self.prime_vehicles = set()

    def __str__(self):
        res = "matricule\t| client\t| date\n"
        for v in self.vehicles:
            res += v.licence_plate + "\t\t\t\t"
            if v.owner:
                res += v.owner.last_name + "\t\t"
            else:
                res += "aucun\t\t"
            res += str(v.start_time) + "\n"

        return res

    def get_price(self):
        return self.__price_parking_spot

    def change_price(self, new_price: float):
        if type(new_price) == "int" and new_price > 0:
            self.__price_parking_spot = new_price

        else:
            print("Mauvais encodage de prix, veuillez entrer un nombre positif non-null")

    def calc_price(self, time):
        return self.__price_parking_spot * (time.seconds // 60) #Par minutes pour la démo

    def add_vehicle(self, vehicle):
        if vehicle in self.vehicles:
            print("le véhicule est déjà dans le parking")
            return None
        self.vehicles.append(vehicle)
        self.nbr_parking_spot_free -= 1
        vehicle.start_time = datetime.now()
        print(
            f"Le véhicule immatriculé {vehicle.licence_plate} est rentré à {vehicle.start_time}, il reste {self.nbr_parking_spot_free} place dans le parking")

    def remove_vehicle(self, vehicle):
        now = datetime.now()
        self.vehicles.remove(vehicle)
        self.nbr_parking_spot_free += 1
        prix = self.calc_price(now - vehicle.start_time)
        print(
            f"Le véhicule immatriculé {vehicle.licence_plate} est sorti à {now} et est resté pendant {now - vehicle.start_time} pour un tarif total de {prix}€, il reste {self.nbr_parking_spot_free} place dans le parking")

    def remove_prime_vehicle(self, vehicle):
        if vehicle in self.prime_vehicles:
            if vehicle.subscription_end < datetime.now():
                print("Ce véhicule n'est actuellement plus abonné")
            else:
                temps_restant = (vehicle.subscription_end - datetime.now())
                res = ""
                if temps_restant.days // 365:
                    res += str(temps_restant.days // 365) + " an(s) "
                if temps_restant.days % 365 // 30:
                    res += str(temps_restant.days % 365 // 30) + " mois "
                if temps_restant.days % 30:
                    res += str(temps_restant.days % 30) + " jour(s) "
                res += f"et {temps_restant.seconds // 3600} heure(s)"
                temps_restant = res
                print(f"Ce véhicule est encore abonné jusqu'au {vehicle.subscription_end.strftime('%d/%m/%y à %H:%M')}, il lui reste donc {temps_restant}")
            if input("Voulez-vous vraiment supprimer ce véhicule ?") == "oui":
                self.prime_vehicles.remove(vehicle)
                print(f"Le véhicule immatriculé {vehicle.licence_plate} a bien été supprimer")
                return True
            else:
                return print("Suppression annulée")
        else:
            return False

def manage_vehicles(vehicles, owners, parking):
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
                    new_vehicle = Vehicle(plaque, owner, True, abonnement)
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
    action = input("Entrée (e)/ sortie (s)/ info (i) : ")
    if action == "i":
        print(parking)
    elif action == "r":
        print("Cette action effaceras toute les données sur le parking")
        action = input("Voulez-vous continuez ? (oui/non) : ")
        if action == "oui":
            parking = reset_parking()
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
    except TypeError:
        print("Veuillez entrer des nombres entiers")
    else:
        new_parking = Parking(nbr_spot, price)
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
