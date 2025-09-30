# Zadatak 2: Bankovni račun

class BankovniRacun:
    """Klasa koja modelira jednostavan bankovni račun."""
    def __init__(self, ime_prezime, broj_racuna):
        """Konstruktor za BankovniRačun."""
        self.ime_prezime = ime_prezime
        self.broj_racuna = broj_racuna
        self.stanja = 0.0
        
    def uplati(self, iznos):
        """Metoda za uplatu novca na računu."""
        if iznos > 0:
            self.stanje += iznos
            print(f"Uplata od {iznos:.2f} EUR na račun {self.broj_racuna} je uspješna.")
            #.2f - dvije decimale
        else:
            print("Neispravan iznos za uplatu. Iznos mora biti pozitivan.")

    def isplati(self, iznos):
        """Smanjuje stanje na računu ako ima dovoljno sredtsva."""
        if iznos <= 0:
            print("Greška: Iznos za isplatu mora biti pozitivan.")
        elif self.stanje >= iznos:
            self.stanje -= iznos
            print(f"Isplata od {iznos:.2f} EUR uspješna. Novo stanje: {self.stanje:.2f} EUR.")
        else:
            print(f"isplata nije moguća. Nedovoljno sredstva (Stanje: {self.stanje:.2f} EUR.)")

    #Ispis podataka o računu.
    def info(self):
        """Ispisuje informacije o računu."""
        print("-" * 25)
        print(f"Vlasnik: {self.ime_vlasnika}")
        print(f"Broj računa: {self.broj_racuna}")
        print(f"Stanje: {self.stanje:.2f} kn")
        print("-" * 25)

#Testiranje klase
racun1 = BankovniRacun ("Pero Perić", "HR123456789")
racun1.info()
racun1.uplati(1000)
racun1.isplati(250)
racun1.isplati(800) # Pokušaj isplate prevelikog iznosa
racun1.uplati(-50) # Pokušaj uplate negativnog iznosa
racun1.info()
print("\n" + "=" * 30 + "\n")

