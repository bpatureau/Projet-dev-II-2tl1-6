import argparse
from datetime import datetime


class Owner:
    def __init__(self, first_name:str, last_name:str, email:str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

class Vehicle:
    def __init__(self, licence_plate:str, owner:Owner):
        self.licence_plate = licence_plate
        self.owner = owner
        self.start_time = None

    """def enter_lot(self):
        if self.__is_in_lot:
            print("Already in lot")
        else:
            self.__is_in_lot = True

    def exit_lot(self):
        if not self.__is_in_lot:
            print("Not in lot")
        else:
            self.__is_in_lot = False

    def become_subscribed(self):
        if self.__subscribed:
            print("Already subscribed")
        else:
            self.__subscribed = True

    def revoke_subscribed(self):
        if not self.__subscribed:
            print("Not subscribed")
        else:
            self.__subscribed = True"""

    def detail_owner(self):
        print(self.owner)

    def __repr__(self):
        return f"{self.owner.last_name} - {self.licence_plate}"

"""class Cars(Vehicle):
    def __init__(self, field, lisence_plate:str, owner:object, subscribed:bool=False, is_in_lot:bool=False):
        super().__init__(lisence_plate, owner, "car", subscribed, is_in_lot)
        self.field = field


class Bike(Vehicle):
    def __init__(self, field, lisence_plate:str, owner:object, subscribed:bool=False, is_in_lot:bool=False):
        super().__init__(lisence_plate, owner, "bike", subscribed, is_in_lot)
        self.field = field
"""




class Parking:
    def __init__(self, nbr_parking_spot:int, price_parking_spot:float):
        self.nbr_parking_spot = nbr_parking_spot
        self.nbr_parking_spot_free = nbr_parking_spot
        self.plate_id = set()
        self.__price_parking_spot = price_parking_spot
        self.vehicles = []

    def get_price(self):
        return self.__price_parking_spot

    def change_price(self, new_price:float):
        if type(new_price) == "int" and new_price > 0:
            self.__price_parking_spot = new_price

        else:
            print("Mauvais encodage de prix, veuillez entrer un nombre positif non-null")

    def calc_price(self, time):
        return self.__price_parking_spot * time.seconds

    def add_vehicle(self, vehicle):
        if vehicle in self.vehicles:
            print("le véhicule est déjà dans le parking")
            return None
        self.vehicles.append(vehicle)
        self.nbr_parking_spot_free -= 1
        vehicle.start_time = datetime.now()
        print(f"Le véhicule de {vehicle.owner.first_name} est rentré à {vehicle.start_time}, il reste {self.nbr_parking_spot_free} place dans le parking")


    def remove_vehicle(self, vehicle):
        now = datetime.now()
        self.vehicles.remove(vehicle)
        self.nbr_parking_spot_free += 1
        prix = self.calc_price(now - vehicle.start_time)
        print(f"Le véhicule de {vehicle.owner.first_name} est sorti à {now} et est resté pendant {now - vehicle.start_time} pour un tarif total de {prix}€, il reste {self.nbr_parking_spot_free} place dans le parking")



def add_car():
    pass


def create_parameters():
    params = argparse.ArgumentParser(description="Action à faire")
    params.add_argument("--add_owner", nargs=3, type=str, help="first_name last_name email")
    params.add_argument("--add_car", nargs=3, type=str, help="license_plate owner vehicle_type")
    #params.add_argument("--info_parking", type=bool, default=False, action="store_true", help="donne les informations sur le parking")
    params.add_argument("--park_car", type=str, help="plate_id")
    params.add_argument("--exit_parking", type=str, help="plate_id")
    return params.parse_args()

def main():
    parking = Parking(100, 5)
    owners = []
    vehicles = []
    while True:
        action = input("Créer un client (c)/ Créer un véhicule (v)/ Gérer le parking (p), Quitter le programme (q) : ")
        if action == "c":
            nom = input("nom : ")
            prenom = input("prénom : ")
            mail = input("mail : ")
            owners.append(Owner(prenom, nom, mail))
        elif action == "v":
            plaque = input("plaque d'immatriculation : ")
            name = input("nom du propriétaire : ")
            owner = None
            for i in owners:
                if name == i.last_name:
                    owner = i
            if owner == None:
                print("le propriétaire n'as pas été trouver")
            else:
                vehicles.append(Vehicle(plaque, owner))
        elif action == "p":
            plaque = input("Plaque d'immatriculation du véhicule : ")
            vehicle = None
            for i in vehicles:
                if plaque == i.licence_plate:
                    vehicle = i
            if vehicle == None:
                print("le véhicule n'as pas été trouver")
            else:
                action = input("Entrée ou sortie (e/s) : ")
                if action == "e":
                    parking.add_vehicle(vehicle)
                elif action == "s":
                    try:
                        parking.remove_vehicle(vehicle)
                    except ValueError:
                        print("le véhicule n'est pas dans le parking")
        elif action == "q":
            break
        else:
            print("mauvaise entrée")





if __name__ == "__main__":
    main()
