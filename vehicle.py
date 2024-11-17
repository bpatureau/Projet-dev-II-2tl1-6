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
    license_plate --> la plaque d'immatriculation du véhicule utilisé comme identifiant unique
    owner --> un propriétaire n'est nécessaire qu'en cas d'abonnement et vaut None par défaut
    subscribed (privé) -->  True si le véhicule est encore abonné, False si non
                            (vérifié au démarrage du programme et lorsqu'il rentre ou sors du parking)
    sub_time --> le temps de l'abonnement en mois lors de la création du véhicule
    last_subscription --> la dernière fois qu'un abonnemnt à été payer (None si jamais abonné)
    subscription_end --> la date et l'heure de l'expiration de l'abonnement (None si jamais abonné)
    """
    def __init__(self, licence_plate: str, owner: Owner = None, subscribed: bool = False, sub_time: int = 0, parking: object = None):
        self.licence_plate = licence_plate
        self.owner = owner
        self.start_time = None
        self.__subscribed = subscribed
        self.last_subscription = None
        self.subscription_end = None
        if subscribed:
            self.become_subscribed(sub_time, parking)
        self.reserved_place = None

    def __str__(self):
        """
        Utiliser lors des print()
        """
        if self.still_subscribed():
            return f"Plaque d'immatriculation : {self.licence_plate}\nPropriétaire du véhicule : {self.owner}\nAbonnement valide jusqu'au {self.subscription_end.strftime('%d/%m/%Y')} à {self.subscription_end.strftime('%H:%M')}\n"
        else:
            return f"Plaque d'immatriculation : {self.licence_plate}\nDurée de stationnement actuelle : {(datetime.now() - self.start_time).seconds // 60} minutes\n"

    def __repr__(self):
        return str({self.licence_plate})

    def calc_sub_time(self, sub_time):
        """
        Calcule la date de fin de l'abonnement
        :param sub_time: le temps en mois de l'abonnement
        :return: un tuple composeé du dernier abonnement (aujourd'hui si le véhicule n'était pas abonné)
                 et de la date de fin de l'abonnement
        """
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
        subscription_end = datetime(year, month, date.day, date.hour, date.minute, date.second,
                                         date.microsecond)
        return (last_subscription, subscription_end)

    def still_subscribed(self):
        """
        Vérifie si le véhicule est abonné et si c'est le cas, si il est encore valide
        :return: True ou False
        """
        if self.subscription_end == None:
            return False
        if not (self.__subscribed and self.subscription_end > datetime.now()):
            self.__subscribed = False
            self.subscription_end = None
        return self.__subscribed


    def become_subscribed(self, sub_time: int, parking: object):
        """
        Commence l'abonnement du véhicule
        :param parking: le parking
        :param sub_time: la durée de l'abonnement en mois
        """
        if self.still_subscribed():
            print(f"Déjà abonné jusqu'au {self.subscription_end.strftime('%d/%m/%y')} à {self.subscription_end.strftime('%H:%M')}")
        else:
            res = ""
            print(parking.parking[0])
            for z in parking.parking[0].display:
                for p in z:
                    if p.premium and p.is_free():
                        res += str(p) + " - "
            res = res[:-3]
            print("Places disponibles : " + res)
            place = input("Quelle place voulez-vous ? : ")
            while not (place in res and place.isalnum()):
                print("Place déjà occupée ou mauvais encodage")
                place = input("Quelle place voulez-vous ? : ")
            place = parking.find_place(place)
            place.switch_state()
            self.reserved_place = place
            self.__subscribed = True
            self.last_subscription, self.subscription_end = self.calc_sub_time(sub_time)

    def revoke_subscribed(self):
        """
        Révoque l'abonnement d'un véhicule
        """
        if not self.still_subscribed():
            print("Ce véhicule n'est actuellement pas abonné")
        else:
            self.__subscribed = False
            self.subscription_end = None

    def detail_owner(self):
        print(self.owner)
