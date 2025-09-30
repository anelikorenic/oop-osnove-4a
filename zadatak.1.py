class Knjiga:
    """Klasa koja dokumentira knjige sa osnovnim podacima."""
    def __init__(self, naslov, autor, godina_izdanja):
        """Konstruktor za klasu knjiga"""
        self.naslov = naslov
        self.autor = autor
        self.godina_izdanja = godina_izdanja

knjiga1 = Knjiga("Hamlet", "William Shakespeare", 1603)
knjiga2 = Knjiga("Gospodar prstenova", "J. R. R. Tolkien", 1954)

print(f"Naslov: {knjiga1.naslov}, Autor: {knjiga1.autor}, Godina izdavanja: {knjiga1.godina_izdanja}")
print(f"Naslov: {knjiga2.naslov}, Autor: {knjiga2.naslov}, Godina izdavanja: {knjiga2.godina_izdanja}")

