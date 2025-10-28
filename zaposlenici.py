class Zaposlenik:
    def __init__(self, ime, prezime, placa):
        self.ime = ime
        self.prezime = prezime
        self.placa = placa

    def prikazi_info(self):
        print(f"Ime i prezime: {self.ime} {self.prezime}, Placa: {self.placa} EUR")

class Programer(Zaposlenik):
    def __init__(self, ime, prezime, placa, programski_jezik):
        super().__init__(ime, prezime, placa)
        self.programski_jezik = programski_jezik

    def prikazi_info(self):
        super().prikazi_info
        print(f"Programski jezik: {self.programski_jezik}")

class Menadzer(Zaposlenik):
    def __init__(self, ime, prezime, placa, tim):
        super().__init__(ime, prezime, placa)
        self.tim = tim

    def prikazi_info(self):
        super().prikazi_info()
        if self.tim:
            print("Članovi tima:")
            for član in self.tim:
                print(f"- {član.ime} {član.prezime}")
        else:
            print("Trenutno nema članova tima.")

if __name__ == "__main__":

    z1 = Zaposlenik("Ana", "Anić", 1200)
    p1 = Programer("Petar", "Perić", 1800, ["Python", "JavaScript"])
    m1 = Menadzer("Iva", "Ivić", 2500, [z1, p1])

    print("Podaci o zaposleniku:")
    z1.prikazi_info()

    print("Podaci o programeru:")
    p1.prikazi_info()

    print("Podaci o menadžeru:")
    m1.prikazi_info()