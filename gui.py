import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from vehicle import Vehicle, Owner, Car, Motorcycle
import os

class GUI:
    def __init__(self, parking):
        self.parking = parking

        self.root = tk.Tk()
        self.root.state('zoomed')  # Fullscreen the window
        self.root.title('Parking de M. Antoine Stationneur')

        self.floors = ("Rez de chaussée", "Étage 1", "Étage 2", "Étage 3", "Étage 4")
        self.selected_floor = self.floors[0]

        self.line_labels = ["A ", "B ", "C ", "D ", "E "]

        # Configure tab style
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Arial', 12)) #I did this mostly for increasing the font size

        # Create notebook / They are used for the tabs
        self.notebook = ttk.Notebook(self.root, style='TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.parking_tab = self._create_tab("Gestionnaire du Parking")
        self.subscriber_tab = self._create_tab("Abonnement")
        self.report_tab = self._create_tab("Rapport")

        # Parking tab content
        self.parking_overview_frame = None  # Added this to be able to manipulate the parking overview
        self.client_license_plate = None
        self._create_parking_tab_content()

        # Subscriber tab content
        self._create_subscriber_tab_content()

        # Report tab content
        self._create_report_tab_content()

        self.root.mainloop()

    def center_window(self, window):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (window.winfo_reqwidth() / 2)
        y = (screen_height / 2) - (window.winfo_reqheight() / 2)
        window.geometry(f"+{int(x)}+{int(y)}")

    def _create_tab(self, title):
        """
        Crée un nouvel onglet dans le notebook.

        PRE :
            title (str): Le titre de l'onglet.

        POST :
            returns : ttk.Frame: Le frame créé pour l'onglet.
        """
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        return frame

    def _create_parking_tab_content(self):
        parking_title_label = tk.Label(self.parking_tab, text="Gestionnaire du Parking", font=("Arial", 20, "bold"))
        parking_title_label.pack(pady=5)

        self._create_entry_exit_buttons()

        parking_capacity_label = tk.Label(self.parking_tab, text="Nombre de places disponibles : ",
                                          font=("Arial", 15, "bold"))
        parking_capacity_label.pack()

        # Créez l'étiquette comme un attribut de la classe pour pouvoir la mettre à jour dynamiquement
        self.parking_capacity_number_label = tk.Label(self.parking_tab,
                                                      text=f"{self.parking.nbr_parking_spot_free}/{self.parking.nbr_parking_spot}",
                                                      font=("Arial", 12), fg='red')
        self.parking_capacity_number_label.pack()

        self._create_floor_selection_buttons()

        floor_label = tk.Label(self.parking_tab, text="Étage sélectionné :", font=("Arial", 12, "bold"))
        floor_label.pack()

        self._create_parking_overview()

    def update_parking_capacity_display(self):
        """
        Met à jour l'affichage du nombre de places restantes.
        """
        self.parking_capacity_number_label.config(
            text=f"{self.parking.nbr_parking_spot_free}/{self.parking.nbr_parking_spot}"
        )

    def _create_entry_exit_buttons(self):
        button_frame = tk.Frame(self.parking_tab)
        button_frame.pack()

        button_entry = tk.Button(button_frame, text="Entrée", width=10, font=("Arial", 15, "bold"),
                                  command=self.client_entry)
        button_exit = tk.Button(button_frame, text="Sortie", width=10, font=("Arial", 15, "bold"),
                                command=self.client_exit)
        button_entry.pack(side=tk.LEFT, padx=5, pady=5)
        button_exit.pack(side=tk.LEFT, padx=5, pady=5)

    def _create_floor_selection_buttons(self):
        button_frame = tk.Frame(self.parking_tab)
        button_frame.pack()

        for floor in self.floors:
            button = tk.Button(button_frame, text=floor, font=("Arial", 12),
                               command=lambda f=floor: self._on_floor_select(f))
            button.pack(side=tk.LEFT, padx=5, pady=5)

    def _create_parking_overview(self):
        self.selected_floor_label = tk.Label(self.parking_tab, text=self.selected_floor, font=("Arial", 12, "bold"))
        self.selected_floor_label.pack(pady=10)

        self.parking_overview_frame = tk.Frame(self.parking_tab)
        self.parking_overview_frame.pack()

        # chr(65) --> 'A'
        for zone in range(len(self.parking.parking)):
            row_label = tk.Label(self.parking_overview_frame, text=chr(zone + 65), font=("Arial", 15))
            row_label.grid(row=zone, column=0)

            for spot in range(10):
                parking_space = tk.Button(self.parking_overview_frame, text=f"{chr(zone + 65)}{spot + 1}",
                                          font=("Arial", 10, "bold"), width=15, height=5, borderwidth=1, relief="solid",
                                          command=lambda line = zone, column = spot: self.open_parking_space_window(line, column)) # For now, it only gives the parking spot but not the floor)
                parking_space.grid(row=zone, column=spot + 1)
                # parking_space.configure(background="lightgreen") example how we could change the colors of the parking spaces and
                # add more functionality to parking spaces like color coding, click events, etc
    def _create_report_tab_content(self):
        """
        Creates content for the report tab, including a centered 'hello' button
        that prints 'hello' when clicked.
        """
        report_frame = tk.Frame(self.report_tab)
        report_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        files_label = tk.Label(report_frame, text="Daily Reports", font=("Arial", 15, "bold"))
        files_label.pack(pady=(0, 10))
        columns = ("Filename",)
        self.report_files_tree = ttk.Treeview(report_frame, columns=columns, show="headings")
        self.report_files_tree.heading("Filename", text="File Name")
        self.report_files_tree.pack(expand=True, fill=tk.BOTH)
        reports_dir = os.path.join(os.path.dirname(__file__), "daily-reports")
        try:
            # Ensure the directory exists
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            # List and insert files
            files = os.listdir(reports_dir)
            for file in files:
                self.report_files_tree.insert("", "end", values=(file,))
        except Exception as e:
            print(f"Error reading daily-reports directory: {e}")
                
        report_button = tk.Button(report_frame, text="Créer un rapport", command=self.create_report, 
                                font=("Arial", 15), width=10)
        report_button.pack()
        
        
    def _on_floor_select(self, floor):
        self.selected_floor = floor
        self._reload_parking_overview()

    def open_parking_space_window(self, line, col):
        new_window = tk.Toplevel(self.root)
        new_window.title(f"Parking {self.line_labels[line]}- {col + 1} sur {self.selected_floor}")
        self.center_window(new_window)
        # Content of the new window, here we will add the vehicles plate number and if it's a subscriber then also name, & so on .. maybe
        label = tk.Label(new_window, text=f"This is parking space {self.line_labels[line]}- {col + 1} sur {self.selected_floor}")
        label.pack(pady=20, padx=20)

    def _reload_parking_overview(self):
        self.selected_floor_label.destroy()
        self.parking_overview_frame.destroy()
        self._create_parking_overview()

    def _create_subscriber_tab_content(self):
        subscriber_title_label = tk.Label(self.subscriber_tab, text="Gestionnaire des Abonnements", font=("Arial", 20))
        subscriber_title_label.pack(pady=10)

        # Search bar for the subscribers by plate number
        tk.Label(self.subscriber_tab, text="Recherche est fait par plaque d'immatriculation :").pack()
        self.search_entry = tk.Entry(self.subscriber_tab)
        self.search_entry.pack(pady=10)

        subscriber_top_button_frame = tk.Frame(self.subscriber_tab)
        subscriber_top_button_frame.pack()

        self.subscriber_search_button = tk.Button(subscriber_top_button_frame, text="Rechercher", command=self.search_subscriber)
        self.subscriber_search_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.subscriber_add_button = tk.Button(subscriber_top_button_frame, text="Ajouter", command=self.add_subscriber)
        self.subscriber_add_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create the Treeview for subscribers
        columns = ("Plaque", "Nom", "Prénom", "Mail", "Type d'abo", "Expiration", "Place de parking réservée")
        self.subscriber_tree = ttk.Treeview(self.subscriber_tab, columns=columns, show="headings")

        # Configure columns and make all of them sortable
        for column in columns:
            self.subscriber_tree.heading(column, text=column,
                                         command=lambda _col=column:
                                         self._sort_by_column(self.subscriber_tree, _col, False))

        # Collection of the data
        data = []
        for v in self.parking.prime_vehicles:  # v = vehicle
            owner = v.owner
            data.append((v.license_plate, owner.first_name, owner.last_name, owner.email,
                         "Voiture Mensuel" if isinstance(v, Car) else "Moto Mensuel",
                         v.subscription_end.strftime("%d/%m/%Y") if v.subscription_end else "Non défini",
                         v.reserved_place if v.reserved_place else "Aucune"))

        # Insertion of the data
        for row in data:
            self.subscriber_tree.insert("", "end", values=row)

        self.subscriber_tree.pack(fill="both", expand=True)


    def _sort_by_column(self, tv, col, reverse):
        """
        Trie les éléments du Treeview par rapport à une colonne donnée.

        PRE :
            - tv : est initialisé et contient des données
            - col : existe dans le Treeview
            - reverse : valeur booléenne

        POST :
            - Les éléments du Treeview sont triés par rapport à la colonne spécifiée.
            - Le sens du tri est inversé à chaque clic sur l'en-tête de colonne.
        """
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(key=lambda t: str(t[0]), reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda _col=col: self._sort_by_column(tv, _col, not reverse))

    def search_subscriber(self):
        """
        Recherche un abonné dans le Treeview "subsciber_tree" en fonction de sa plaque d'immatriculation.

        PRE :
            - search_term : n'est pas vide.
            - subscriber_tree : est correctement initialisé et contient des données.

        POST :
            - Si l'abonné est trouvé, il est sélectionné et mis en évidence dans le Treeview "subscriber_tree".
            - Si l'abonné n'est pas trouvé, un message d'erreur est affiché.
        """
        search_term = self.search_entry.get().strip()

        if not search_term:
            self.subscriber_tree.selection_remove(*self.subscriber_tree.selection())
            return

        found = False
        for item in self.subscriber_tree.get_children():
            if search_term.lower() in self.subscriber_tree.item(item)['values'][0].lower():
                self.subscriber_tree.selection_set(item)
                self.subscriber_tree.focus(item)
                item_id = self.subscriber_tree.get_children().index(item)
                self.subscriber_tree.yview_moveto(item_id / self.subscriber_tree.get_children().__len__())
                found = True
                break

        if not found:
            messagebox.showinfo("Recherche", "Aucun abonné trouvé avec cette plaque.")

    def add_subscriber(self):
        form_data = self.add_subscriber_window()
        owner = Owner(form_data["first_name"], form_data["last_name"], form_data["email"])

        # Déterminez la durée de l'abonnement
        sub_time = 1 if form_data["subscription_duration"] == "Month" else 12

        # Créez un véhicule en fonction du type choisi
        if form_data["vehicle_type"] == "Car":
            new_vehicle = Car(form_data["license_plate"], owner, True, sub_time, self.parking)
        else:
            new_vehicle = Motorcycle(form_data["license_plate"], owner, True, sub_time, self.parking)

        # Attribuez une place de parking
        place = self.parking.find_place(form_data["selected_place"])
        place.switch_state()
        new_vehicle.reserved_place = place
        self.parking.prime_vehicles.add(new_vehicle)

        # Déterminez le type d'abonnement (Mensuel ou Annuel)
        subscription_type = "Mensuel" if sub_time == 1 else "Annuel"

        # Ajoutez les données dans le tableau
        data = [
            form_data["license_plate"],
            form_data["first_name"],
            form_data["last_name"],
            form_data["email"],
            f"{form_data['vehicle_type']} {subscription_type}",
            new_vehicle.subscription_end.strftime("%d/%m/%Y") if new_vehicle.subscription_end else "Non défini",
            str(place)
        ]
        self.subscriber_tree.insert("", "end", values=data)

    def add_subscriber_window(self):
        """
        Opens a new window for subscribing a vehicle.
        Returns the data submitted via the form.
        """
        # Data container
        form_data = {}

        # Create a new top-level window
        new_window = tk.Toplevel(self.root)
        new_window.title("Ajouter un abonné")
        self.center_window(new_window)

        # Disable the main window
        self.root.attributes("-disabled", True)
        new_window.grab_set()

        new_window.protocol("WM_DELETE_WINDOW", lambda: self.close_new_window(new_window))

        # Form Labels and Entry Fields
        form_frame = tk.Frame(new_window, padx=10, pady=10)
        form_frame.pack()

        # License Plate
        tk.Label(form_frame, text="Plaque d'immatriculation :").grid(row=0, column=0, sticky="w", pady=5)
        license_plate_entry = tk.Entry(form_frame, width=30)
        license_plate_entry.grid(row=0, column=1, pady=5)
        license_plate_entry.focus_set()

        # First Name
        tk.Label(form_frame, text="Prénom :").grid(row=1, column=0, sticky="w", pady=5)
        first_name_entry = tk.Entry(form_frame, width=30)
        first_name_entry.grid(row=1, column=1, pady=5)

        # Last Name
        tk.Label(form_frame, text="Nom :").grid(row=2, column=0, sticky="w", pady=5)
        last_name_entry = tk.Entry(form_frame, width=30)
        last_name_entry.grid(row=2, column=1, pady=5)

        # Email
        tk.Label(form_frame, text="Email :").grid(row=3, column=0, sticky="w", pady=5)
        email_entry = tk.Entry(form_frame, width=30)
        email_entry.grid(row=3, column=1, pady=5)

        # Subscription Duration (Radio Buttons)
        tk.Label(form_frame, text="Durée de l'abonnement :").grid(row=4, column=0, sticky="w", pady=5)
        subscription_var = tk.StringVar(value="Month")
        tk.Radiobutton(form_frame, text="1 mois", variable=subscription_var, value="Month").grid(row=4, column=1,
                                                                                                 sticky="w")
        tk.Radiobutton(form_frame, text="1 an", variable=subscription_var, value="Year").grid(row=4, column=1,
                                                                                              sticky="e")

        # Vehicle Type (Radio Buttons)
        tk.Label(form_frame, text="Type de véhicule :").grid(row=5, column=0, sticky="w", pady=5)
        vehicle_type_var = tk.StringVar(value="Car")  # Default to "Car"
        tk.Radiobutton(form_frame, text="Voiture", variable=vehicle_type_var, value="Car").grid(row=5, column=1,
                                                                                                sticky="w")
        tk.Radiobutton(form_frame, text="Moto", variable=vehicle_type_var, value="Motorcycle").grid(row=5, column=1,
                                                                                                    sticky="e")

        # Select Place (Dropdown)
        tk.Label(form_frame, text="Place de parking réservée").grid(row=6, column=0, sticky="w", pady=5)
        places = []
        for z in self.parking.parking[0].display:
            for p in z:
                if p.is_free():
                    places.append(str(p))
        place_var = tk.StringVar(value=places[0])
        place_menu = ttk.Combobox(form_frame, textvariable=place_var, values=places, state="readonly")
        place_menu.grid(row=6, column=1, pady=5)

        # Submit Button
        submit_button = tk.Button(new_window, text="Soumettre", command=lambda: self.collect_form_data_and_close(
            license_plate_entry.get(),
            first_name_entry.get(),
            last_name_entry.get(),
            email_entry.get(),
            subscription_var.get(),
            vehicle_type_var.get(),  # Passez ici la sélection de type de véhicule
            place_var.get(),
            form_data,
            new_window  # Passez également l'argument `window`
        ))
        submit_button.pack(pady=10)

        # Use wait_window to pause until the new window is closed
        self.root.wait_window(new_window)

        # Return the collected form data
        return form_data

    def collect_form_data_and_close(self, license_plate, first_name, last_name, email, duration, vehicle_type, place,
                                    form_data, window):
        """
        Validates and collects form data. If any field is missing, it shows an error message.
        """
        # Validation: Check for empty fields
        if not license_plate.strip():
            messagebox.showerror("Validation Error", "License Plate is required!")
            return
        if not first_name.strip():
            messagebox.showerror("Validation Error", "First Name is required!")
            return
        if not last_name.strip():
            messagebox.showerror("Validation Error", "Last Name is required!")
            return
        if not email.strip():
            messagebox.showerror("Validation Error", "Email is required!")
            return
        if not place.strip():
            messagebox.showerror("Validation Error", "Place is required!")
            return

        # Store form data
        form_data.update({
            "license_plate": license_plate,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "subscription_duration": duration,
            "vehicle_type": vehicle_type,
            "selected_place": place
        })

        # Show a success message (optional)
        messagebox.showinfo("Form Submitted", f"Le véhicule {vehicle_type} est maintenant abonné")

        # Close the new window and re-enable the main window
        self.close_new_window(window)

    def client_entry(self):
        """
        Gère l'entrée d'un véhicule dans le parking.
        Demande à l'utilisateur de saisir une plaque d'immatriculation et de sélectionner le type de véhicule.
        """
        # Crée une nouvelle fenêtre pour demander les informations
        entry_window = tk.Toplevel(self.root)
        entry_window.title("Entrée d'un véhicule")
        self.center_window(entry_window)

        # Désactive la fenêtre principale pendant l'ouverture
        self.root.attributes("-disabled", True)
        entry_window.grab_set()

        # Étiquette et champ de saisie pour la plaque
        tk.Label(entry_window, text="Plaque d'immatriculation :").pack(pady=5)
        license_plate_entry = tk.Entry(entry_window, width=30)
        license_plate_entry.pack(pady=5)
        license_plate_entry.focus_set()

        # Sélection du type de véhicule
        tk.Label(entry_window, text="Type de véhicule :").pack(pady=5)
        vehicle_type_var = tk.StringVar(value="Car")  # Par défaut : Voiture
        tk.Radiobutton(entry_window, text="Voiture", variable=vehicle_type_var, value="Car").pack(pady=2)
        tk.Radiobutton(entry_window, text="Moto", variable=vehicle_type_var, value="Motorcycle").pack(pady=2)

        # Bouton pour valider l'entrée
        submit_button = tk.Button(
            entry_window,
            text="Soumettre",
            command=lambda: self.validate_entry(license_plate_entry.get(), vehicle_type_var.get(), entry_window)
        )
        submit_button.pack(pady=10)

        # Permet de fermer la fenêtre proprement
        entry_window.protocol("WM_DELETE_WINDOW", lambda: self.close_new_window(entry_window))

        # Attendre la fermeture de la fenêtre
        self.root.wait_window(entry_window)

    def validate_entry(self, license_plate, vehicle_type, entry_window):
        """
        Valide l'entrée du véhicule en fonction de sa plaque et de son type.
        """
        # Vérifie si la plaque est vide
        if not license_plate.strip():
            messagebox.showerror("Erreur", "Veuillez entrer une plaque d'immatriculation.")
            return

        # Vérifie si le véhicule est déjà dans le parking
        if self.parking.is_vehicle_present(license_plate):
            messagebox.showerror("Erreur", "Le véhicule est déjà dans le parking.")
            self.close_new_window(entry_window)
            return

        # Crée un véhicule en fonction du type sélectionné
        if vehicle_type == "Car":
            vehicle = Car(license_plate)  # Pas besoin de wheels ici
        elif vehicle_type == "Motorcycle":
            vehicle = Motorcycle(license_plate)  # Pas besoin de wheels ici
        else:
            messagebox.showerror("Erreur", "Type de véhicule invalide.")
            return

        # Ajoute le véhicule au parking
        start_time = datetime.now()
        vehicle.start_time = start_time
        self.parking.add_vehicle(vehicle)

        messagebox.showinfo(
            "Entrée réussie",
            f"Le véhicule {vehicle_type} immatriculé {license_plate} est entré à {start_time.strftime('%H:%M')}."
        )

        self.update_parking_capacity_display()

        # Ferme la fenêtre d'entrée
        self.close_new_window(entry_window)

    def close_new_window(self, window):
        """
        Ferme une fenêtre contextuelle et réactive la fenêtre principale.
        """
        self.root.attributes("-disabled", False)
        window.grab_release()
        window.destroy()

    def client_exit(self):
        """
        Gère la sortie d'un véhicule du parking.
        """
        exit_window = tk.Toplevel(self.root)
        exit_window.title("Sortie d'un véhicule")
        self.center_window(exit_window)

        self.root.attributes("-disabled", True)
        exit_window.grab_set()

        tk.Label(exit_window, text="Plaque d'immatriculation :").pack(pady=5)
        license_plate_entry = tk.Entry(exit_window, width=30)
        license_plate_entry.pack(pady=5)
        license_plate_entry.focus_set()

        submit_button = tk.Button(
            exit_window,
            text="Soumettre",
            command=lambda: self.validate_exit(license_plate_entry.get(), exit_window)
        )
        submit_button.pack(pady=10)

        exit_window.protocol("WM_DELETE_WINDOW", lambda: self.close_new_window(exit_window))

        self.root.wait_window(exit_window)

    def validate_exit(self, license_plate, exit_window):
        """
        Valide la sortie d'un véhicule du parking.
        :param license_plate: La plaque d'immatriculation saisie.
        :param exit_window: La fenêtre de sortie.
        """
        if not license_plate.strip():
            messagebox.showerror("Erreur", "Veuillez entrer une plaque d'immatriculation.")
            return

        try:
            # ne fonctionne pas, surement pcq en sortie on ne verifie pas le difference entre moto et voiture
            vehicle = self.parking.find_vehicle(license_plate)

            # ne fonctionne pas
            if vehicle.still_subscribed():
                messagebox.showinfo(
                    "Sortie réussie",
                    f"Le véhicule immatriculé {license_plate} a quitté le parking. "
                    f"Aucun montant n'est dû car le véhicule est abonné."
                )
            else:
                end_time = datetime.now()
                duration = (end_time - vehicle.start_time).total_seconds() / 3600  # Convertit en heures
                hourly_rate = self.parking.get_price()
                amount_due = round(duration * hourly_rate, 2)

                messagebox.showinfo(
                    "Sortie réussie",
                    f"Le véhicule immatriculé {license_plate} a quitté le parking.\n"
                    f"Durée : {duration:.2f} heures\n"
                    f"Montant à payer : {amount_due:.2f} €"
                )

            self.parking.remove_vehicle(license_plate)
            self.update_parking_capacity_display()

        except KeyError:
            messagebox.showerror("Erreur", f"Aucun véhicule trouvé avec la plaque {license_plate}.")
        finally:
            self.close_new_window(exit_window)

    def client_entry_exit_base_window(self, exit=False):
        client_license_plate = ""
        new_window = tk.Toplevel(self.root)
        new_window.title("Entrée")
        new_window.protocol("WM_DELETE_WINDOW", lambda: self.close_new_window(new_window))
        self.center_window(new_window)
        self.root.attributes("-disabled", True)
        new_window.grab_set()


        form_frame = tk.Frame(new_window, padx=10, pady=10)
        form_frame.pack()

        tk.Label(form_frame, text="Plaque d'immatriculation :").grid(row=0, column=0, sticky="w", pady=5)
        license_plate_entry = tk.Entry(form_frame, width=30)
        license_plate_entry.grid(row=0, column=1, pady=5)
        license_plate_entry.focus_set()

        submit_button = tk.Button(new_window, text="Soumettre",
                                  command=lambda: self.set_client_plate_number(new_window, license_plate_entry))
        submit_button.pack()

        self.root.wait_window(new_window)

    def set_client_plate_number(self, window, license_plate_entry):
        self.client_license_plate = license_plate_entry.get()
        self.close_new_window(window)
        
    def create_report(self):
        """
        Crée un rapport en JSON dans le dossier daily-reports
        le rapport contient:
        - Le nombre de voitures qui sont sortient du parking
        - Le nombre de moto qui sont sortient du parking
        - La quantité d'argent que ces véhicules sortant ont généré
        - La date du rapport
        Pre: /
        Post: Si le dossier daily-reports existe, crée un fichier JSON avec les données récoltées depuis le dernier rapport
        """
        # Déterminer le nom du prochain rapport
        reports_dir = os.path.join(os.path.dirname(__file__), "daily-reports")
        os.makedirs(reports_dir, exist_ok=True)
        existing_reports = [f for f in os.listdir(reports_dir) if f.startswith("report") and f.endswith(".json")]
        if existing_reports:
            report_numbers = [int(f.replace("report", "").replace(".json", "")) for f in existing_reports]
            next_report_number = max(report_numbers) + 1
        else:
            next_report_number = 1
        
        # initialisation des variables
        cars_exited = 0
        motorcycles_exited = 0
        total_revenue = 0.0
        
        # récupération des données collectées
        for vehicle in self.parking.exited_vehicles:
            if isinstance(vehicle, Car):
                cars_exited += 1
            elif isinstance(vehicle, Motorcycle):
                motorcycles_exited += 1
            if not vehicle.still_subscribed():
                duration = (vehicle.exit_time - vehicle.start_time).total_seconds() / 3600
                total_revenue += round(duration * self.parking.get_price(), 2)
        
        # format du rapport
        report_data = {
            "report_number": next_report_number,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cars_exited": cars_exited,
            "motorcycles_exited": motorcycles_exited,
            "total_revenue": total_revenue
        }
        
        report_filename = f"report{next_report_number}.json"
        report_path = os.path.join(reports_dir, report_filename)
        
        # Création du rapport
        try:
            with open(report_path, 'w') as f:
                json.dump(report_data, f, indent=4)
            
            self.report_files_tree.insert("", "end", values=(report_filename,))
            
            messagebox.showinfo("Rapport", f"Rapport {report_filename} créé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de créer le rapport : {str(e)}")