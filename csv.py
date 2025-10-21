import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import xml.etree.ElementTree as ET

class Ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred
        
    def __str__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred
        return f"{self.ime},{self.prezime},{self.razred}"
    
    class EvidencijaApp:
        if not self.ucenici:
            messagebox.showinfo("Info", "Nema učenika za izvoz.")
            return
        
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filepath:
            with open(filepath, "w", newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Ime", "Prezime", "Razred"])
                for ucenik in self.ucenici: #self.ucenici je OBJEKT, koji ćemo kreirati; lista učenika/lista objekata
                    writer.writerow([ucenik.ime, ucenik.prezime, ucenik.razred])
            messagebox.showinfo("Info", f"Učenici su uspješno izvezeni u {filepath}.")

    def ucitaj_iz_cvs(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            with open(filepath, "r", newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(file)
                self.ucenici = [Ucenik(row["Ime"], row["Prezime"], row["Razred"]) for row in reader]
            self.osvjezi_prikaz()
            messagebox.showinfo("Info", f"Učenici su uspješno učitani/vraćeni iz {filepath}.")

    def spremi_u_xml(self):
        if not self.ucenici:
            messagebox.showinfo("Info", "Nema učenika za izvoz.")
            return
        
        filepath = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if filepath:
            root = ET.Element("Ucenici")
            for ucenik in self.ucenici:
                ucenik_elem = ET.SubElement(root, "Ucenik")
                ET.SubElement(ucenik_elem, "Ime").text = ucenik.ime
                ET.SubElement(ucenik_elem, "Prezime").text = ucenik.prezime
                ET.SubElement(ucenik_elem, "Razred").text = ucenik.razred
            
            tree = ET.ElementTree(root)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            messagebox.showinfo("Info", f"Učenici su uspješno izvezeni u {filepath}.")


