class BankovniRacun:
    def __init__(self, ime_prezime, broj_racuna):
        self.ime_prezime= ime_prezime
        self.broj_racuna= broj_racuna
        self.stanje= 0.0
    
    def uplati(self,iznos):
        if iznos>0:
            self.stanje += iznos
            print(f"Uplata od: {iznos:.2f}, EUR na račun: {self.broj_racuna}, je uspješna.")
        else:
            print("Neispravam iznos za uplatu. Iznos mora biti pozitivan.")

    def isplati(self,iznos):
        if iznos<0:
            print("Greška: Iznos za isplatu mora biti pozitivan.")
        elif self.stanje >= iznos:
            self.stanje -= iznos
            print(f"Isplata od {iznos:.2f} EUR uspješna. Novo stanje: {self.stanje:.2f} EUR.")
        else:
            print(f"Isplata nije moguća. nedovoljno sredstva (Stanje: {self.stanje:.2f}) EUR.")

    def info(self):
        print(f"Vlasnik računa: {self.ime_prezime}")
        print(f"Broj računa: {self.broj_racuna}")
        print(f"Stanje računa: {self.stanje:.2f}")

račun1=BankovniRacun("Pia Kovačić","HR1234567890123456789")

račun1.stanje=100000000000000
račun1.isplati(3475839)
račun1.info()