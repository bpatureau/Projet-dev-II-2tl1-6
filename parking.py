from datetime import datetime


class Node:
    def __init__(self):
        self.__free = True
        self.premium = False
        self.two_wheels = False

    def get_free(self):
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
                zone.append(Node())
            self.display.append(zone)

    def __str__(self):
        res = ""
        for zone in self.display:
            for j in zone:
                res += str(int(j.get_free()))
            res += "\n"
        return res

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

    def __str__(self):
        """
        Utiliser lors des print()
        """
        res = "matricule\t| client\t| date\n"
        for v in self.vehicles:
            res += v.licence_plate + "\t\t\t\t"
            if v.owner:
                res += v.owner.last_name + "\t\t"
            else:
                res += "aucun\t\t"
            res += str(v.start_time) + "\n"

        return res

    def create_parking(self, nbr_floor: int):
        """

        :param nbr_floor: prend un int qui représente le nombres d'étages
        :return: une liste d'objet Floor (étage)
        """
        parking = []
        for i in range(nbr_floor):
            parking.append(Floor(i, 10, 5))
        return parking

    def get_price(self):
        """
        :return: le tarif par heure
        """
        return self.__price_parking_spot

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
        rajoute un véhicule dans le parking
        :param vehicle: le véhicule à rajouter
        """
        if vehicle in self.vehicles:
            print("le véhicule est déjà dans le parking")
            return None
        self.vehicles.append(vehicle)
        self.nbr_parking_spot_free -= 1
        vehicle.start_time = datetime.now()
        print(
            f"Le véhicule immatriculé {vehicle.licence_plate} est rentré le {vehicle.subscription_end.strftime('%d/%m/%Y')} à {vehicle.subscription_end.strftime('%H:%M')}, il reste {self.nbr_parking_spot_free} place dans le parking")

    def remove_vehicle(self, vehicle):
        """
        Retire un véhicule du parking
        :param vehicle: le véhicule qui s'en va
        """
        now = datetime.now()
        if vehicle.still_subscribed():
            return print(f"Le véhicule immatriculé {vehicle.licence_plate} est sorti le {now.strftime('%d/%m/%Y')} à {now.strftime('%H:%M')}. Ce véhicule est abonné et ne paye donc pas le tarif")
        self.vehicles.remove(vehicle)
        self.nbr_parking_spot_free += 1
        prix = self.calc_price(now - vehicle.start_time)
        print(
            f"Le véhicule immatriculé {vehicle.licence_plate} est sorti à {now} et est resté pendant {now - vehicle.start_time} pour un tarif total de {prix}€, il reste {self.nbr_parking_spot_free} place dans le parking")

    def remove_prime_vehicle(self, vehicle):
        """
        retire un ancien véhicule abonné de la liste des abonnés
        si il ne se trouve pas dans le parking lors de la fermeture du programme,
        il sera effacer de façon permanente (sauf si on le recrée)
        :param vehicle: le véhicule à retirer
        :return: True ou False
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

