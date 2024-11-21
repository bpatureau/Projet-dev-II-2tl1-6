import tkinter as tk
from tkinter import ttk, messagebox

class GUI:
    def __init__(self):
        def sort_by_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(key=lambda t: str(t[0]), reverse=reverse)

            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)

                # Reverse the sort order for the next click
            tv.heading(col, command=lambda _col=col: sort_by_column(tv, _col, not reverse))

        self.root = tk.Tk()
        self.root.state('zoomed') #Fullscreen the window
        self.root.title('Parking de M. Antoine Stationneur') #Simply giving the window a name

        # Setting the style for the tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Arial', 12))

        # Creating the tabs
        self.notebook = ttk.Notebook(self.root, style='TNotebook')
        self.notebook.pack(fill="both", expand=True)

        self.parking_tab = ttk.Frame(self.notebook)
        self.subscriber_tab = ttk.Frame(self.notebook)
        self.report_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.parking_tab, text="Gestionnaire du Parking")
        self.notebook.add(self.subscriber_tab, text="Abonnement")
        self.notebook.add(self.report_tab, text="Rapport")

        # Content of the Parking tab
        parking_title_label = tk.Label(self.parking_tab, text="Gestionnaire du Parking", font=("Arial", 20))
        parking_title_label.pack(pady=10)

        parking_capacity_label = tk.Label(self.parking_tab, text="Capacité du parking :", font=("Arial", 15))
        parking_capacity_label.pack()

        parking_capacity_number = tk.Label(self.parking_tab, text="NUMBER NEEDS TO BE ADDED HERE example: 2/250", font=("Arial", 12), fg='red')
        parking_capacity_number.pack()

        # Create a frame to hold the buttons for floor selection
        button_frame = tk.Frame(self.parking_tab)
        button_frame.pack()

        # Buttons to select each floor
        button1 = tk.Button(button_frame, text="Rez de chaussée", font=("Arial", 12))
        button1.pack(side=tk.LEFT, padx=5, pady=5)

        button2 = tk.Button(button_frame, text="Étage 1", font=("Arial", 12))
        button2.pack(side=tk.LEFT, padx=5, pady=5)

        button3 = tk.Button(button_frame, text="Étage 2", font=("Arial", 12))
        button3.pack(side=tk.LEFT, padx=5, pady=5)

        button4 = tk.Button(button_frame, text="Étage 3", font=("Arial", 12))
        button4.pack(side=tk.LEFT, padx=5, pady=5)

        button5 = tk.Button(button_frame, text="Étage 4", font=("Arial", 12))
        button5.pack(side=tk.LEFT, padx=5, pady=5)

        memo_label = tk.Label(self.parking_tab, text="Buttons do nothing for now", font=("Arial", 12), fg="red")
        memo_label.pack(pady=10)

        # Create a frame for the parking overview
        parking_overview_frame = tk.Frame(self.parking_tab)
        parking_overview_frame.pack()

        # Add parking spaces to the overview using grid layout
        row_labels = ["A ", "B ", "C ", "D ", "E "]
        for i in range(5):
            row_label = tk.Label(parking_overview_frame, text=row_labels[i], font=("Arial", 15))
            row_label.grid(row=i, column=0)

            for j in range(10):
                parking_space = tk.Button(parking_overview_frame, text=f"{row_labels[i]}- {j+1}", font=("Arial", 10, "bold"), width=15, height=5, borderwidth=1, relief="solid")
                parking_space.grid(row=i, column=j+1)


        # Content of the Subscribers tab
        subscriber_title_label = tk.Label(self.subscriber_tab, text="Gestionnaire des Abonnements", font=("Arial", 20))
        subscriber_title_label.pack(pady=10)

        # Frame, Textfield and buttons of the subscribers tab at the top

        # Entry Button
        self.search_entry = tk.Entry(self.subscriber_tab)
        self.search_entry.pack(pady=10)

        # Frame
        button_frame_sub_top = tk.Frame(self.subscriber_tab)
        button_frame_sub_top.pack()

        # Search Button
        self.sub_search_button = tk.Button(button_frame_sub_top, text="Rechercher", command=self.search_subscriber)
        self.sub_search_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Add Button
        self.sub_add_button = tk.Button(button_frame_sub_top, text="Ajouter")#, command=self.add_subscriber)
        self.sub_add_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Créer les colonnes de la grille
        columns = ("Nom", "Prénom", "Mail", "Plaque", "Type d'abo", "Expiration")

        # Créer un Treeview pour afficher les données
        self.tree = ttk.Treeview(self.subscriber_tab, columns=columns, show="headings")

        # Configurer les colonnes
        for column in columns:
            self.tree.heading(column, text=column)

        # Ajouter des données à la grille (exemple)
        data = [
            ("Dupont", "Jean", "jean.dupont@exemple.com", "AB-123-CD", "Voiture Mensuel", "2024-12-31"),
            ("Dupont", "Jean", "jean.dupont@exemple.com", "AA-123-AA", "Moto Mensuel", "2024-11-31")
        ]

        for row in data:
            self.tree.insert("", "end", values=row)

        # Afficher le Treeview
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("Expiration", text="Expiration",
                          command=lambda _col="Expiration": sort_by_column(self.tree, _col, False))

        # Content of the Report tab


        self.root.mainloop()
        # Functions that need to be declared in init





    def search_subscriber(self):
        search_term = self.search_entry.get().strip()

        if not search_term:
            self.tree.selection_remove(*self.tree.selection())
            return

        found = False
        for item in self.tree.get_children():
            if search_term.lower() in self.tree.item(item)['values'][3].lower():
                self.tree.selection_set(item)
                self.tree.focus(item)
                item_id = self.tree.get_children().index(item)
                self.tree.yview_moveto(item_id / self.tree.get_children().__len__())
                found = True
                break

        if not found:
            messagebox.showinfo("Recherche", "Aucun abonné trouvé avec cette plaque.")








GUI()
