import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from vehicle import Vehicle, Owner


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

        # Report tab content - Empty for now, because I don't know what to do exactly on this tab yet

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

        parking_capacity_label = tk.Label(self.parking_tab, text="Nombre de places disponibles : ", font=("Arial", 15, "bold"))
        parking_capacity_label.pack()

        parking_capacity_number_label = tk.Label(self.parking_tab, text=f"{self.parking.nbr_parking_spot_free}/{self.parking.nbr_parking_spot}",
                                           font=("Arial", 12), fg='red')
        parking_capacity_number_label.pack()

        self._create_floor_selection_buttons()

        floor_label = tk.Label(self.parking_tab, text="Étage sélectionné :", font=("Arial", 12, "bold"))
        floor_label.pack()

        self._create_parking_overview()

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
                                         self._sort_by_column(self.subscriber_tree,_col,False))

        # Collection of the data
        data = []
        for v in self.parking.prime_vehicles:   # v = vehicle
            owner = v.owner
            data.append((v.licence_plate, owner.first_name, owner.last_name, owner.email, "Voiture Mensuel",
                         v.subscription_end, "Parking RA1"))

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
        sub_time = (1 if form_data["subscription_duration"] == "Month" else 12)
        new_vehicle = Vehicle(form_data["license_plate"], owner, True, sub_time, self.parking)
        place = self.parking.find_place(form_data["selected_place"])
        place.switch_state()
        new_vehicle.reserved_place = place
        self.parking.prime_vehicles.add(new_vehicle)
        data = [form_data["first_name"], form_data["last_name"], form_data["email"], form_data["license_plate"],
                "Voiture Mensuel", new_vehicle.subscription_end, place]
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


        # Select Place (Dropdown)
        tk.Label(form_frame, text="Place de parking réservée").grid(row=5, column=0, sticky="w", pady=5)
        places = []
        for z in self.parking.parking[0].display:
            for p in z:
                if p.is_free():
                    places.append(str(p))
        place_var = tk.StringVar(value=places[0])
        place_menu = ttk.Combobox(form_frame, textvariable=place_var, values=places, state="readonly")
        place_menu.grid(row=5, column=1, pady=5)
        print(place_var)

        # Submit Button
        submit_button = tk.Button(new_window, text="Soumettre", command=lambda: self.collect_form_data_and_close(
            license_plate_entry.get(),
            first_name_entry.get(),
            last_name_entry.get(),
            email_entry.get(),
            subscription_var.get(),
            place_var.get(),
            form_data,
            new_window
        ))
        submit_button.pack(pady=10)

        # Use wait_window to pause until the new window is closed
        self.root.wait_window(new_window)

        # Return the collected form data
        return form_data

    def collect_form_data_and_close(self, license_plate, first_name, last_name, email, duration, place, form_data, window):
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
            "selected_place": place
        })

        # Show a success message (optional)
        messagebox.showinfo("Form Submitted", "Le véhicule est maintenant abonné")

        # Close the new window and re-enable the main window
        self.close_new_window(window)


    def close_new_window(self, new_window):
        """
        Re-enables the main window and destroys the new window.
        """
        self.root.attributes("-disabled", False)
        new_window.grab_release()
        new_window.destroy()

    def client_entry(self):
        start_time = datetime.now()
        licence_plate = self.search_entry.get().strip()
        print(licence_plate)
        self.parking.add_vehicle(Vehicle(licence_plate))
        self.client_entry_exit_base_window()
        messagebox.showinfo("ENTREE", f"Le véhicule immatriculé {licence_plate} est rentré le {start_time.strftime('%d/%m/%Y')} à {start_time.strftime('%H:%M')}, il reste {self.parking.nbr_parking_spot_free} place dans le parking")

    def client_exit(self):
        try:
            start_time = datetime.now()
            licence_plate = self.search_entry.get().strip()
            self.parking.remove_vehicle(licence_plate)
            messagebox.showinfo("SORTIE", f"Le véhicule immatriculé {licence_plate} est sorti le {start_time.strftime('%d/%m/%Y')} à {start_time.strftime('%H:%M')}, il reste {self.parking.nbr_parking_spot_free} place dans le parking")
        except KeyError:
            messagebox.showinfo("ERREUR", "Le véhicle n'as pas été trouvé dans le parking")
        finally:
            self.client_entry_exit_base_window(exit=True)

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


