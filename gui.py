import tkinter as tk
from tkinter import ttk, messagebox


class GUI:
    def __init__(self):
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
        self.parking_overview_frame = None # Added this to be able to manipulate the parking overview
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
        parking_title_label.pack(pady=10)

        parking_capacity_label = tk.Label(self.parking_tab, text="Capacité du parking :", font=("Arial", 15, "bold"))
        parking_capacity_label.pack()

        parking_capacity_number_label = tk.Label(self.parking_tab, text="NUMBER",
                                           font=("Arial", 12), fg='red')
        parking_capacity_number_label.pack()

        self._create_floor_selection_buttons()

        floor_label = tk.Label(self.parking_tab, text="Étage sélectionné :", font=("Arial", 12, "bold"))
        floor_label.pack()

        self._create_parking_overview()

    def _create_floor_selection_buttons(self):
        button_frame = tk.Frame(self.parking_tab)
        button_frame.pack()

        for floor in self.floors:
            button = tk.Button(button_frame, text=floor, font=("Arial", 12),
                               command=lambda f=floor: self._on_floor_select(f))
            button.pack(side=tk.LEFT, padx=5, pady=5)

    def _create_parking_overview(self):
        self.selected_floor_label = tk.Label(self.parking_tab, text= self.selected_floor, font=("Arial", 12, "bold"))
        self.selected_floor_label.pack(pady=10)

        self.parking_overview_frame = tk.Frame(self.parking_tab)
        self.parking_overview_frame.pack()

        for i in range(5):
            line_label = tk.Label(self.parking_overview_frame, text=self.line_labels[i], font=("Arial", 15))
            line_label.grid(row=i, column=0)

            for j in range(10):
                parking_space_number = (i, j)
                parking_space = tk.Button(self.parking_overview_frame,
                                          text=f"{self.line_labels[i]}- {j + 1}", font=("Arial", 10, "bold"),
                                          width=15, height=5, borderwidth=1, relief="solid",
                                          command=lambda line = i, column = j: self.open_parking_space_window(line, column)) # For now, it only gives the parking spot but not the floor
                parking_space.grid(row=i, column=j + 1)
                # parking_space.configure(background="lightgreen") example how we could change the colors of the parking spaces and
                # add more functionality to parking spaces like color coding, click events, etc


    def _on_floor_select(self, floor):
        self.selected_floor = floor
        self._reload_parking_overview()

    def _reload_parking_overview(self):
        self.selected_floor_label.destroy()
        self.parking_overview_frame.destroy()
        self._create_parking_overview()

    def open_parking_space_window(self, line, col):
        new_window = tk.Toplevel(self.root)
        new_window.title(f"Parking {self.line_labels[line]}- {col + 1} sur {self.selected_floor}")

        self.center_window(new_window)

        # Content of the new window, here we will add the vehicles plate number and if it's a subscriber then also name, & so on .. maybe
        label = tk.Label(new_window, text=f"This is parking space {self.line_labels[line]}- {col + 1} sur {self.selected_floor}")
        label.pack(pady=20, padx=20)

    def _create_subscriber_tab_content(self):
        subscriber_title_label = tk.Label(self.subscriber_tab, text="Gestionnaire des Abonnements", font=("Arial", 20))
        subscriber_title_label.pack(pady=10)

        # Search bar for the subscribers
        self.search_entry = tk.Entry(self.subscriber_tab)
        self.search_entry.pack(pady=10)

        subscriber_top_button_frame = tk.Frame(self.subscriber_tab)
        subscriber_top_button_frame.pack()

        self.subscriber_search_button = tk.Button(subscriber_top_button_frame, text="Rechercher", command=self.search_subscriber)
        self.subscriber_search_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.subscriber_add_button = tk.Button(subscriber_top_button_frame, text="Ajouter")
        self.subscriber_add_button.pack(side=tk.LEFT, padx=5, pady=5)


        # Create the Treeview for subscribers
        columns = ("Nom", "Prénom", "Mail", "Plaque", "Type d'abo", "Expiration")
        self.subscriber_tree = ttk.Treeview(self.subscriber_tab, columns=columns, show="headings")

        # Configure columns and make all of them sortable
        for column in columns:
            self.subscriber_tree.heading(column, text=column,
                                         command=lambda _col=column:
                                         self._sort_by_column(self.subscriber_tree,_col,False))

        # Sample data (will be replaced with the actual data)
        data = [
            ("Dupont", "Jean", "jean.dupont@exemple.com", "AB-123-CD", "Mensuel", "2024-12-31"),
            ("A", "A", "A.A@A.COM", "AA-AAA-AA", "A - A", "2000-01-01")
        ]

        # Insertion of the data
        for line in data:
            self.subscriber_tree.insert("", "end", values=line)

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
            if search_term.lower() in self.subscriber_tree.item(item)['values'][3].lower():
                self.subscriber_tree.selection_set(item)
                self.subscriber_tree.focus(item)
                item_id = self.subscriber_tree.get_children().index(item)
                self.subscriber_tree.yview_moveto(item_id / self.subscriber_tree.get_children().__len__())
                found = True
                break

        if not found:
            messagebox.showinfo("Recherche", "Aucun abonné trouvé avec cette plaque.")

GUI()