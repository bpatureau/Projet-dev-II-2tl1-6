import tkinter as tk
from tkinter import ttk, messagebox


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.state('zoomed')  # Fullscreen the window
        self.root.title('Parking de M. Antoine Stationneur')

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
        self._create_parking_tab_content()

        # Subscriber tab content
        self._create_subscriber_tab_content()

        # Report tab content - Empty for now, because I don't know what to do exactly on this tab yet

        self.root.mainloop()

    def _create_tab(self, title):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        return frame

    def _create_parking_tab_content(self):
        parking_title_label = tk.Label(self.parking_tab, text="Gestionnaire du Parking", font=("Arial", 20))
        parking_title_label.pack(pady=10)

        parking_capacity_label = tk.Label(self.parking_tab, text="Capacité du parking :", font=("Arial", 15))
        parking_capacity_label.pack()

        parking_capacity_number = tk.Label(self.parking_tab, text="NUMBER NEEDS TO BE ADDED HERE example: 2/250",
                                            font=("Arial", 12), fg='red')
        parking_capacity_number.pack()

        self._create_floor_selection_buttons()

        memo_label = tk.Label(self.parking_tab, text="Buttons do nothing for now", font=("Arial", 12), fg="red")
        memo_label.pack(pady=10)

        # Create parking overview (function for cleaner code)
        self._create_parking_overview()

    def _create_floor_selection_buttons(self):
        button_frame = tk.Frame(self.parking_tab)
        button_frame.pack()

        floors = ("Rez de chaussée", "Étage 1", "Étage 2", "Étage 3", "Étage 4")
        for i, floor in enumerate(floors):
            button = tk.Button(button_frame, text=floor, font=("Arial", 12))
            button.pack(side=tk.LEFT, padx=5, pady=5)

    def _create_parking_overview(self):
        parking_overview_frame = tk.Frame(self.parking_tab)
        parking_overview_frame.pack()

        row_labels = ["A ", "B ", "C ", "D ", "E "]
        for i in range(5):
            row_label = tk.Label(parking_overview_frame, text=row_labels[i], font=("Arial", 15))
            row_label.grid(row=i, column=0)

            for j in range(10):
                parking_space = tk.Button(parking_overview_frame,
                                          text=f"{row_labels[i]}- {j+1}", font=("Arial", 10, "bold"),
                                          width=15, height=5, borderwidth=1, relief="solid")
                parking_space.grid(row=i, column=j+1)

    def _create_subscriber_tab_content(self):
        subscriber_title_label = tk.Label(self.subscriber_tab, text="Gestionnaire des Abonnements", font=("Arial", 20))
        subscriber_title_label.pack(pady=10)

        # Search bar
        self.search_entry = tk.Entry(self.subscriber_tab)
        self.search_entry.pack(pady=10)

        subscriber_top_button_frame = tk.Frame(self.subscriber_tab)
        subscriber_top_button_frame.pack()

        self.subscriber_search_button = tk.Button(subscriber_top_button_frame, text="Rechercher", command=self.search_subscriber)
        self.subscriber_search_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.subscriber_add_button = tk.Button(subscriber_top_button_frame, text="Ajouter") # Add Subscribers, but i'm not sure how exactly
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

        for row in data:
            self.subscriber_tree.insert("", "end", values=row)

        self.subscriber_tree.pack(fill="both", expand=True)

    def _sort_by_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(key=lambda t: str(t[0]), reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda _col=col: self._sort_by_column(tv, _col, not reverse))

    def search_subscriber(self):
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