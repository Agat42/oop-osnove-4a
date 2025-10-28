class Zaposlenik:
    def __init__(self, ime, prezime, placa):
        self.ime=ime
        self.prezime=prezime
        self.placa=placa

    def prikaz_info(self):
        print(f"Ime i prezime: {self.ime} {self.prezime}, Plaća: {self.placa} EUR")

class Programer(Zaposlenik):
    def __init__(self, ime, prezime, placa, programski_jezici):
        super().__init__(ime, prezime, placa)
        self.programski_jezici=programski_jezici

    def prikaz_info(self):
        super().prikaz_info()
        print(f"Programski jezici: {', '.join(self.programski_jezici)}")

class Menadzer(Zaposlenik):
    def __init__(self, ime, prezime, placa, tim):
        super().__init__(ime, prezime, placa)
        self.tim=tim

    def prikaz_info(self):
        super().prikaz_info()
        print(f"Tim: {', '.join(self.tim)}")

if __name__=="__main__":
    z1 = Zaposlenik("Agata", "G", 1500)
    p1 = Programer("Pia", "K", 2000, ["Python", "JavaScript"])
    m1 = Menadzer("Lara", "P", 2500, ["Agata G", "Pia K"])

    print("--- Podaci o zaposleniku ---")
    z1.prikaz_info()

    print("\n--- Podaci o programeru ---")
    p1.prikaz_info()

    print("\n--- Podaci o menadžeru ---")
    m1.prikaz_info()