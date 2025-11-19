import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date, datetime, timedelta
import xml.etree.ElementTree as ET
import os
import uuid

#Konstante
APP_NAME = "ConnectSphere"
VERSION = "1.0"
AUTHOR = "Aneli"
DATA_FILE = "connectsphere_data.xml"

#Klase
class Kontakt:
    def __init__(self, ime, prezime="", telefoni=None, emailovi=None, datum_rodjenja=None, grupa="Nepoznato", tvrtka=None, cid=None):
        self.ime = ime
        self.prezime = prezime
        self.telefoni = telefoni or []
        self.emailovi = emailovi or []
        self.datum_rodjenja = datum_rodjenja  # datetime.date objekt
        self.grupa = grupa
        self.tvrtka = tvrtka
        self.cid = cid if cid else str(uuid.uuid4())

    def to_xml(self):
        el = ET.Element("kontakt", attrib={"cid": self.cid})
        ET.SubElement(el, "ime").text = self.ime
        ET.SubElement(el, "prezime").text = self.prezime
        ET.SubElement(el, "grupa").text = self.grupa
        if self.datum_rodjenja:
            ET.SubElement(el, "datum_rodjenja").text = self.datum_rodjenja.isoformat()
        if self.tvrtka:
            ET.SubElement(el, "tvrtka").text = self.tvrtka

        phones_el = ET.SubElement(el, "telefoni")
        for t in self.telefoni:
            ET.SubElement(phones_el, "telefon").text = t

        emails_el = ET.SubElement(el, "emailovi")
        for e in self.emailovi:
            ET.SubElement(emails_el, "email").text = e

        return el

    #@staticmethod
    def from_xml(el):
        ime = el.find("ime").text
        prezime = el.find("prezime").text
        grupa = el.find("grupa").text
        datum_rodjenja_el = el.find("datum_rodjenja")
        datum_rodjenja = datetime.fromisoformat(datum_rodjenja_el.text).date() if datum_rodjenja_el is not None else None
        tvrtka_el = el.find("tvrtka")
        tvrtka = tvrtka_el.text if tvrtka_el is not None else None
        telefoni = [t.text for t in el.find("telefoni").findall("telefon")]
        emailovi = [e.text for e in el.find("emailovi").findall("email")]
        cid = el.attrib.get("cid")
        return Kontakt(ime, prezime, telefoni, emailovi, datum_rodjenja, grupa, tvrtka, cid)

    def __str__(self):
        return f"{self.ime} {self.prezime} ({self.grupa})"

class PrivatniKontakt(Kontakt):
    def __init__(self, ime, prezime="", telefoni=None, emailovi=None, datum_rodjenja=None, grupa="Obitelj"):
        super().__init__(ime, prezime, telefoni, emailovi, datum_rodjenja, grupa)

class PoslovniKontakt(Kontakt):
    def __init__(self, ime, prezime="", telefoni=None, emailovi=None, datum_rodjenja=None, grupa="Posao", tvrtka=None):
        super().__init__(ime, prezime, telefoni, emailovi, datum_rodjenja, grupa, tvrtka)

#Glavna aplikacija
class ConnectSphereApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("800x500")

        self.kontakti = []
        self.groups = ["Obitelj", "Prijatelji", "Posao"]

        self.create_menu()
        self.create_status_bar()
        self.create_ui()
        self.load_data()
        self.check_birthdays()
        self.update_status()

    #Menu
    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Spremi", command=self.save_data)
        file_menu.add_command(label="Učitaj", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Izlaz", command=self.root.quit)
        menu.add_cascade(label="Datoteka", menu=file_menu)

        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="O aplikaciji", command=self.show_about)
        menu.add_cascade(label="Pomoć", menu=help_menu)

    #Statusna traka
    def create_status_bar(self):
        self.status = tk.Label(self.root, text="", bd=1, relief=tk.SUNKEN, anchor="w")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self):
        self.status.config(text=f"Broj kontakata: {len(self.kontakti)} | Broj grupa: {len(self.groups)}")

    #UI
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)

        #Lijevi frame: Treeview (adresar)
        left = ttk.Frame(main_frame)
        left.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(left, columns=("Ime", "Prezime", "Grupa"), show="headings")
        self.tree.heading("Ime", text="Ime")
        self.tree.heading("Prezime", text="Prezime")
        self.tree.heading("Grupa", text="Grupa")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.show_details)

        #Desni frame: unos (adresar)
        right = ttk.Frame(main_frame)
        right.pack(side="right", fill="y", padx=5, pady=5)

        tk.Label(right, text="Ime:").pack(anchor="w")
        self.fn_entry = tk.Entry(right)
        self.fn_entry.pack(fill="x")

        tk.Label(right, text="Prezime:").pack(anchor="w")
        self.ln_entry = tk.Entry(right)
        self.ln_entry.pack(fill="x")

        tk.Label(right, text="Grupa:").pack(anchor="w")
        self.group_box = ttk.Combobox(right, values=self.groups)
        self.group_box.pack(fill="x")
        self.group_box.current(0)

        tk.Label(right, text="Datum rođenja (YYYY-MM-DD):").pack(anchor="w")
        self.bd_entry = tk.Entry(right)
        self.bd_entry.pack(fill="x")

        #Telefoni
        tk.Label(right, text="Telefoni:").pack(anchor="w")
        self.phone_frame = ttk.Frame(right)
        self.phone_frame.pack(fill="x")
        self.phone_entries = []
        self.add_phone_entry()
        ttk.Button(right, text="+", width=2, command=self.add_phone_entry).pack(anchor="w")

        #Emailovi
        tk.Label(right, text="Emailovi:").pack(anchor="w")
        self.email_frame = ttk.Frame(right)
        self.email_frame.pack(fill="x")
        self.email_entries = []
        self.add_email_entry()
        ttk.Button(right, text="+", width=2, command=self.add_email_entry).pack(anchor="w")

        #Dodaj gumb
        ttk.Button(right, text="Dodaj kontakt", command=self.add_contact).pack(pady=10)

        #Detalji
        tk.Label(right, text="Detalji kontakta:").pack(anchor="w", pady=(10,0))
        self.details_text = tk.Text(right, height=10, state="disabled")
        self.details_text.pack(fill="x")

    #Dodavanje dinamičkih polja
    def add_phone_entry(self):
        entry = tk.Entry(self.phone_frame)
        entry.pack(fill="x", pady=2)
        self.phone_entries.append(entry)

    def add_email_entry(self):
        entry = tk.Entry(self.email_frame)
        entry.pack(fill="x", pady=2)
        self.email_entries.append(entry)

    #Dodavanje kontakta
    def add_contact(self):
        ime = self.fn_entry.get().strip()
        prezime = self.ln_entry.get().strip()
        grupa = self.group_box.get()
        bd_text = self.bd_entry.get().strip()

        telefoni = [e.get().strip() for e in self.phone_entries if e.get().strip()]
        emailovi = [e.get().strip() for e in self.email_entries if e.get().strip()]

        if not ime:
            messagebox.showerror("Greška", "Ime je obavezno!")
            return

        datum_rodjenja = None
        if bd_text:
            try:
                datum_rodjenja = datetime.strptime(bd_text, "%Y-%m-%d").date()
            except:
                messagebox.showerror("Greška", "Neispravan datum!")
                return

        kontakt = Kontakt(ime, prezime, telefoni, emailovi, datum_rodjenja, grupa)
        self.kontakti.append(kontakt)
        self.refresh_tree()
        self.update_status()
        self.clear_entries()

    def clear_entries(self):
        self.fn_entry.delete(0, tk.END)
        self.ln_entry.delete(0, tk.END)
        self.bd_entry.delete(0, tk.END)
        for e in self.phone_entries: e.destroy()
        self.phone_entries.clear()
        self.add_phone_entry()
        for e in self.email_entries: e.destroy()
        self.email_entries.clear()
        self.add_email_entry()

    #Refresh treeview
    def refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for k in self.kontakti:
            self.tree.insert("", tk.END, iid=k.cid, values=(k.ime, k.prezime, k.grupa))

    #Detalji kontakta
    def show_details(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        cid = selection[0]
        kontakt = next((k for k in self.kontakti if k.cid == cid), None)
        if kontakt:
            self.details_text.config(state="normal")
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert(tk.END, f"Ime: {kontakt.ime}\nPrezime: {kontakt.prezime}\nGrupa: {kontakt.grupa}\n")
            self.details_text.insert(tk.END, f"Datum rođenja: {kontakt.datum_rodjenja}\n")
            self.details_text.insert(tk.END, "Telefoni:\n")
            for t in kontakt.telefoni:
                self.details_text.insert(tk.END, f"  - {t}\n")
            self.details_text.insert(tk.END, "Emailovi:\n")
            for e in kontakt.emailovi:
                self.details_text.insert(tk.END, f"  - {e}\n")
            if kontakt.tvrtka:
                self.details_text.insert(tk.END, f"Tvrtka: {kontakt.tvrtka}\n")
            self.details_text.config(state="disabled")

    #Spremanje/učitavanje
    def save_data(self):
        root_el = ET.Element("kontakti")
        for k in self.kontakti:
            root_el.append(k.to_xml())
        tree = ET.ElementTree(root_el)
        tree.write(DATA_FILE, encoding="utf-8", xml_declaration=True)
        messagebox.showinfo("Spremno", f"Podaci spremljeni u {DATA_FILE}")

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return
        tree = ET.parse(DATA_FILE)
        root_el = tree.getroot()
        self.kontakti = [Kontakt.from_xml(el) for el in root_el.findall("kontakt")]
        self.refresh_tree()
        self.update_status()

    #Rođendanski podsjetnik
    def check_birthdays(self):
        today = date.today()
        upcoming = []
        for k in self.kontakti:
            if k.datum_rodjenja:
                this_year = k.datum_rodjenja.replace(year=today.year)
                delta = (this_year - today).days
                if 0 <= delta <= 7:
                    upcoming.append(f"{k.ime} {k.prezime} - {this_year}")
        if upcoming:
            messagebox.showinfo("Rođendani", "Rođendani u sljedećih 7 dana:\n" + "\n".join(upcoming))

    #O aplikaciji
    def show_about(self):
        messagebox.showinfo("O aplikaciji", f"{APP_NAME}\nVerzija: {VERSION}\nAutor: {AUTHOR}")

#Pokretanje
if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectSphereApp(root)
    root.mainloop()