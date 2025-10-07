#Definicija klase
class Ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred

    def __str__ (self):
        return f"{self.prezime}, {self.ime}, ({self.razred})"
        print(f"Učenik: {self.ime}, {self.prezime}, razred: {self.razred}")

class EvidencijaApp:
    def __init__ (self, root):
        self.root.title("Evidencija učenika")
        self.root.geometry("500x400")

    self.root.columnconfigure(0, weight=1)
    self.root.rowconfigure(1, weight=1)


    unos_frame = tk.Frame(self.root, padx=10, pady=10)
    unos_frame.grid(row=0, column=0, sticky="EW")

    prikaz_frame = tk.Frame(self.root, padx=10, pady=10)
    prikaz_frame.grid(row=1, column=0, sticky="NSEW")

    prikaz_frame.columnconfigure(0, weight=1)
    prikaz_frame.rowconfigure(0, weight=1)


    tk.Label(unos_frame, text="Ime:").grid(row=0, column=0, padx=5, pady=5, sticky="W")
    self.ime_entry = tk.Entry(unos_frame)
    self.ime_entry.grid(row=0, column=1, padx=5, pady=5, sticky="EW")


    tk.Label(unos_frame, text="Prezime:").grid(row=1, column=0, padx=5, pady=5, sticky="W")
    self.prezime_entry = tk.Entry(unos_frame)
    self.prezime_entry.grid(row=1, column=1, padx=5, pady=5, sticky="EW")


    tk.Label(unos_frame, text="Razred:").grid(row=2, column=0, padx=5, pady=5, sticky="W")
    self.razred_entry = tk.Entry(unos_frame)
    self.razred_entry.grid(row=2, column=1, padx=5, pady=5, sticky="EW")


    self.dodaj_gumb = tk.Button(unos_frame, text="Dodaj učenika")
    self.dodaj_gumb.grid(row=3, column=0, padx=5, pady=10)

    self.spremi_gumb = tk.Button(unos_frame, text="Spremi izmjene")
    self.spremi_gumb.grid(row=3, column=1, padx=5, pady=10, sticky="W")


    self.listbox = tk.Listbox(prikaz_frame)
    self.listbox.grid(row=0, column=0, sticky="NSEW")


    scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=self.listbox.yview)
    scrollbar.grid(row=0, column=1, sticky="NS")
    self.listbox.config(yscrollcommand=scrollbar.set)



