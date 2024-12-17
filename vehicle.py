from datetime import datetime

class Owner:
    """
    Uniquement pour les véhicules ayant un abonnement
    Un propriétaire (owner) peut avoir plusieurs véhicules mais chaque véhicule a un abonnement distinct
    """
    def __init__(self, first_name: str, last_name: str, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __str__(self):
        return self.first_name + " " + self.last_name


class Vehicle:
    """
    Classe parent représentant un véhicule générique.

    Attributs :
    - license_plate : str --> la plaque d'immatriculation du véhicule (identifiant unique)
    - owner : Owner (par défaut None) --> le propriétaire du véhicule
    - wheels : int --> le nombre de roues
    - subscribed (privé) : bool --> True si le véhicule est abonné, False sinon
    - sub_time : int --> durée de l'abonnement en mois
    - last_subscription : datetime --> dernière date de souscription
    - subscription_end : datetime --> date et heure d'expiration de l'abonnement
    """

    def __init__(self, license_plate: str, wheels: int, owner: object = None, subscribed: bool = False,
                 sub_time: int = 0, parking: object = None):
        self.license_plate = license_plate
        self.owner = owner
        self.wheels = wheels
        self.start_time = None
        self.__subscribed = subscribed
        self.last_subscription = None
        self.subscription_end = None
        self.exit_time = None
        if subscribed:
            if not isinstance(sub_time, int):
                raise ValueError(f"sub_time doit être un entier, reçu : {type(sub_time)}")
            self.become_subscribed(sub_time, parking)
        self.reserved_place = None

    def __str__(self):
        if self.still_subscribed():
            return (f"Plaque d'immatriculation : {self.license_plate}\n"
                    f"Propriétaire du véhicule : {self.owner}\n"
                    f"Abonnement valide jusqu'au {self.subscription_end.strftime('%d/%m/%Y')} à {self.subscription_end.strftime('%H:%M')}\n"
                    f"Nombre de roues : {self.wheels}\n")
        else:
            return (f"Plaque d'immatriculation : {self.license_plate}\n"
                    f"Durée de stationnement actuelle : {(datetime.now() - self.start_time).seconds // 60} minutes\n"
                    f"Nombre de roues : {self.wheels}\n")

    def __repr__(self):
        return str({self.license_plate})

    def calc_sub_time(self, sub_time):
        if not isinstance(sub_time, int):
            raise TypeError(f"sub_time doit être un entier, reçu : {type(sub_time)}")

        if self.still_subscribed():
            date = self.subscription_end
            last_subscription = self.last_subscription
        else:
            date = datetime.now()
            last_subscription = date

        year = date.year + sub_time // 12
        month = date.month + sub_time % 12
        if month > 12:
            month = 1
            year += 1
        subscription_end = datetime(year, month, date.day, date.hour, date.minute, date.second, date.microsecond)
        return (last_subscription, subscription_end)

    def still_subscribed(self):
        if self.subscription_end is None:
            return False
        if not (self.__subscribed and self.subscription_end > datetime.now()):
            self.__subscribed = False
            self.subscription_end = None
        return self.__subscribed

    def become_subscribed(self, sub_time: int, parking: object):
        if self.still_subscribed():
            print(
                f"Déjà abonné jusqu'au {self.subscription_end.strftime('%d/%m/%y')} à {self.subscription_end.strftime('%H:%M')}")
        else:
            self.__subscribed = True
            self.last_subscription, self.subscription_end = self.calc_sub_time(sub_time)

    def revoke_subscribed(self):
        if not self.still_subscribed():
            print("Ce véhicule n'est actuellement pas abonné")
        else:
            self.__subscribed = False
            self.subscription_end = None

    def detail_owner(self):
        print(self.owner)


class Car(Vehicle):
    """
    Classe représentant une voiture.
    Hérite de Vehicle et spécifie :
    - Prix d'abonnement : 90 €/mois, 950 €/an
    """
    MONTHLY_SUBSCRIPTION_COST = 90
    ANNUAL_SUBSCRIPTION_COST = 950

    def __init__(self, license_plate: str, owner: object = None, subscribed: bool = False, sub_time: int = 0,
                 parking: object = None):
        super().__init__(license_plate, wheels=4, owner=owner, subscribed=subscribed, sub_time=sub_time,
                         parking=parking)

    def __str__(self):
        return super().__str__() + "Type : Voiture\n"


class Motorcycle(Vehicle):
    """
    Classe représentant une moto.
    Hérite de Vehicle et spécifie :
    - Prix d'abonnement : 50 €/mois, 500 €/an
    """
    MONTHLY_SUBSCRIPTION_COST = 50
    ANNUAL_SUBSCRIPTION_COST = 500

    def __init__(self, license_plate: str, owner: object = None, subscribed: bool = False, sub_time: int = 0,
                 parking: object = None):
        super().__init__(license_plate, wheels=2, owner=owner, subscribed=subscribed, sub_time=sub_time,
                         parking=parking)

    def __str__(self):
        return super().__str__() + "Type : Moto\n"
