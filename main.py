class Vehicle:
    def __init__(self, lisence_plate:str, owner:object, subscribed:bool, is_in_lot:bool):
        self.lisence_plate = lisence_plate
        self.owner = owner
        self.__subscribed = subscribed
        self.__is_in_lot = is_in_lot

    def enter_lot(self):
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
            self.__subscribed = True

    def detail_owner(self):
        print(self.owner)


class Cars(Vehicle):
    def __init__(self, field, lisence_plate:str, owner:object, subscribed:bool=False, is_in_lot:bool=False):
        super().__init__(lisence_plate, owner, subscribed, is_in_lot)
        self.field = field


class Bike(Vehicle):
    def __init__(self, field, lisence_plate:str, owner:object, subscribed:bool=False, is_in_lot:bool=False):
        super().__init__(lisence_plate, owner, subscribed, is_in_lot)
        self.field = field


class Owner:
    def __init__(self, first_name:str, last_name:str, email:str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


class ParkingLot:
    def __init__(self, nbr_parking_spot_car:int, nbr_parking_spot_bike:int, price_paking_spot:float):
        self.nbr_parking_spot_car = nbr_parking_spot_car
        self.nbr_parking_spot_bike = nbr_parking_spot_bike
        self.__price_paking_spot = price_paking_spot

    def get_price(self):
        return self.__price_paking_spot

    def change_price(self, new_price:float):
        if type(new_price) == "int" and new_price > 0:
            self.__price_paking_spot = new_price

        else:
            print("Mauvais encodage de prix, veuillez entrer un nombre positif non-null")