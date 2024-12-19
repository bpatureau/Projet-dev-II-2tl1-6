from datetime import datetime
from vehicle import Car, Motorcycle

class Node:
    def __init__(self, location: str, premium = False, two_wheels = False):
        self.__free = True
        self.location = location
        self.two_wheels = two_wheels

    def __str__(self):
        return self.location

    def is_free(self):
        return self.__free

    def switch_state(self):
        if self.__free:
            self.__free = False
        else:
            self.__free = True


class Floor:
    def __init__(self, floor_number, nbr_places_zone, nbr_zones):
        self.floor_number = floor_number
        self.display = []
        for i in range(nbr_zones):
            zone = []
            for j in range(nbr_places_zone):
                location = ("R" + chr(i+65) + str(j))
                if floor_number == 0:
                    if i < 3:
                        zone.append(Node(location, two_wheels=True))
                    else:
                        zone.append(Node(location, premium=True))
                else:
                    zone.append(Node((location + chr(i+65) + str(j))))
            self.display.append(zone)

    def __getitem__(self, item):
        return self.display[item]


class Parking:
    """
    Classe principale du programme
    nbr_parking_spot_tot --> le nombre total de place (occuppé ou non)
    nbr_parking_spot_free --> le nombre de place encore libre
    price_parking_spot (privé) --> tarif d'une place de parking par heure
    vehicles --> liste des véhicules garé dans le parking
    prime_vehicles --> liste des véhicules abonnés
    """
    def __init__(self, nbr_parking_spot_tot: int, price_parking_spot: float, nbr_floor: int):
        self.parking = self.create_parking(nbr_floor)
        self.nbr_parking_spot = nbr_parking_spot_tot
        self.nbr_parking_spot_free = nbr_parking_spot_tot
        self.__price_parking_spot = price_parking_spot
        self.vehicles = []
        self.prime_vehicles = set()
        self.exited_vehicles = []
    def __str__(self):
        """
        Utiliser lors des print()
        """
        res = "matricule | client |  date  | heure\n"
        for v in self.vehicles:
            res += "  " + v.licence_plate + "\t\t"
            if v.owner:
                res += v.owner.last_name + "\t"
            else:
                res += "aucun\t\t"
            res += f"{v.start_time.strftime('%d-%m-%y')}  {v.start_time.strftime('%H:%M')}\n"

        return res
    @property
    def price_parking_spot(self):
        return self.__price_parking_spot
    @price_parking_spot.setter
    def set_price_parking_spot(self, change):
        if isinstance(change, float):
            self.__price_parking_spot = change
        else:
            raise ValueError("La valeur que vous avez entrée n'est pas valide.")
    def create_parking(self, nbr_floor: int):
        """

        :param nbr_floor: prend un int qui représente le nombres d'étages
        :return: une liste d'objet Floor (étage)
        """
        parking = []
        for i in range(nbr_floor):
            parking.append(Floor(i, 10, 5))
        return parking
    

    def find_place(self, place: str):
        """
        pre:
            place est un string qui permet de savoir quelle type de vehicule rentre dans le parking
        post:nous indique quelle est la premiere place disponible
        """
        if place[0].upper() == "R":
            place = "0" + place[1:]
        return self.parking[int(place[0])][ord(place[1])-65][int(place[2])]


    def get_price(self):
        """
        :return: le tarif par heure
        """
        return self.price_parking_spot

    def change_price(self, new_price: float):
        """
        change le tarif par heure
        :param new_price: le nouveau tarif
        """
        if type(new_price) == "int" and new_price > 0:
            self.__price_parking_spot = new_price

        else:
            print("Mauvais encodage de prix, veuillez entrer un nombre positif non-null")

    def calc_price(self, time):
        """
        calcule le prix en fonction du temps pour les non-abonnés
        :param time: la durée que le véhicule est resté dans le parking
        :return: le montant à payer
        """
        return self.__price_parking_spot * (time.seconds // 60) #Par minutes pour la démo

    def add_vehicle(self, vehicle):
        """
        Ajoute un véhicule au parking après avoir vérifié son type.
        :param vehicle: le véhicule à rajouter (Car ou Motorcycle)
        """
        # Vérifie si le véhicule est déjà dans le parking
        if self.is_vehicle_present(vehicle.license_plate):
            print(f"Le véhicule immatriculé {vehicle.license_plate} est déjà dans le parking.")
            return None

        # Ajoute le véhicule
        self.vehicles.append(vehicle)
        self.nbr_parking_spot_free -= 1
        vehicle.start_time = datetime.now()

        # Vérification du type de véhicule
        if isinstance(vehicle, Car):
            print(
                f"La voiture immatriculée {vehicle.license_plate} est entrée le {vehicle.start_time.strftime('%d/%m/%Y')} "
                f"à {vehicle.start_time.strftime('%H:%M')}. Il reste {self.nbr_parking_spot_free} places disponibles."
            )
        elif isinstance(vehicle, Motorcycle):
            print(
                f"La moto immatriculée {vehicle.license_plate} est entrée le {vehicle.start_time.strftime('%d/%m/%Y')} "
                f"à {vehicle.start_time.strftime('%H:%M')}. Il reste {self.nbr_parking_spot_free} places disponibles."
            )
        else:
            print(f"Véhicule non reconnu, immatriculé {vehicle.license_plate}.")

        return vehicle

    def remove_vehicle(self, license_plate):
        """
        Retire un véhicule du parking.
        :param license_plate: La plaque d'immatriculation du véhicule à retirer.
        """
        vehicle = self.find_vehicle(license_plate)
        vehicle.exit_time = datetime.now()
        self.exited_vehicles.append(vehicle)
        # Vérifiez si le véhicule est abonné, ne focntionne pas
        if vehicle.still_subscribed():
            print(
                f"Le véhicule immatriculé {vehicle.license_plate} est sorti le {vehicle.exit_time.strftime('%d/%m/%Y')} à {vehicle.exit_time.strftime('%H:%M')}. "
                f"Ce véhicule est abonné et ne paye donc pas le tarif."
            )
        else:
            duration = vehicle.exit_time - vehicle.start_time
            prix = self.calc_price(duration)

            if isinstance(vehicle, Car):
                print(
                    f"La voiture immatriculée {vehicle.license_plate} est sortie à {vehicle.exit_time.strftime('%d/%m/%Y %H:%M')} "
                    f"après {duration} pour un tarif total de {prix:.2f}€. "
                    f"Il reste {self.nbr_parking_spot_free + 1} places dans le parking."
                )
            elif isinstance(vehicle, Motorcycle):
                print(
                    f"La moto immatriculée {vehicle.license_plate} est sortie à {vehicle.exit_time.strftime('%d/%m/%Y %H:%M')} "
                    f"après {duration} pour un tarif total de {prix:.2f}€. "
                    f"Il reste {self.nbr_parking_spot_free + 1} places dans le parking."
                )

        self.vehicles.remove(vehicle)
        self.nbr_parking_spot_free += 1

    def remove_prime_vehicle(self, vehicle):
        """
        Supprime un véhicule abonné de la liste des abonnés.

        PRE :
            - `vehicle` : objet de type Vehicle et est un véhicule abonné

        POST :
            - Retire le véhicule de l'ensemble `prime_vehicles` du parking si l'utilisateur confirme.
            - Affiche un message indiquant le résultat de l'opération.
            - Retourne une valeur booléenne.
        """
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
                print("Suppression annulée")
        return False

    def find_vehicle(self, license_plate):
        """
        Recherche un véhicule dans le parking.
        :param license_plate: La plaque d'immatriculation à rechercher.
        :return: L'objet véhicule trouvé.
        """
        for v in self.vehicles:
            if v.license_plate == license_plate:
                return v
        raise KeyError(f"Véhicule avec la plaque {license_plate} introuvable.")

    def is_vehicle_present(self, license_plate):
        """
        Vérifie si un véhicule est déjà présent dans le parking.
        :param license_plate: La plaque d'immatriculation à vérifier.
        :return: True si le véhicule est présent, sinon False.
        """
        return any(v.license_plate == license_plate for v in self.vehicles)
