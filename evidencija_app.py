import tkinter as tk
from tkinter import messagebox


class Ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred

    def __str__(self):
        return f"{self.prezime} {self.ime} ({self.razred})"



class EvidencijaApp:
    def __init__(self, root):
        self.root = root
        root.title("Evidencija učenika")
        root.geometry("600x400")

        self.ucenici = []
        self.odabrani_ucenik_index = None
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        
        unos_frame = tk.Frame(root, padx=10, pady=10, bg="#e9ecef")
        unos_frame.grid(row=0, column=0, sticky="EW")
        
        prikaz_frame = tk.Frame(root, padx=10, pady=10, bg="#f8f9fa")
        prikaz_frame.grid(row=1, column=0, sticky="NSEW")

        unos_frame.columnconfigure(1, weight=1)
        prikaz_frame.rowconfigure(0, weight=1)
        prikaz_frame.columnconfigure(0, weight=1)
        
        tk.Label(unos_frame, text="Ime:", bg="#e9ecef").grid(row=0, column=0, sticky="W", pady=2)
        self.ime_entry = tk.Entry(unos_frame)
        self.ime_entry.grid(row=0, column=1, sticky="EW", pady=2)

        tk.Label(unos_frame, text="Prezime:", bg="#e9ecef").grid(row=1, column=0, sticky="W", pady=2)
        self.prezime_entry = tk.Entry(unos_frame)
        self.prezime_entry.grid(row=1, column=1, sticky="EW", pady=2)

        tk.Label(unos_frame, text="Razred:", bg="#e9ecef").grid(row=2, column=0, sticky="W", pady=2)
        self.razred_entry = tk.Entry(unos_frame)
        self.razred_entry.grid(row=2, column=1, sticky="EW", pady=2)
       
        self.dodaj_btn = tk.Button(unos_frame, text="Dodaj učenika", command=self.dodaj_ucenika)
        self.dodaj_btn.grid(row=0, column=2, rowspan=3, padx=10, sticky="NS")

        self.uredi_btn = tk.Button(unos_frame, text="Spremi izmjene", command=self.spremi_izmjene)
        self.uredi_btn.grid(row=0, column=3, rowspan=3, padx=5, sticky="NS")
        
        self.lista_ucenika = tk.Listbox(prikaz_frame)
        self.lista_ucenika.grid(row=0, column=0, sticky="NSEW")

        scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=self.lista_ucenika.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.lista_ucenika.config(yscrollcommand=scrollbar.set)

        self.lista_ucenika.bind('<<ListboxSelect>>', self.odaberi_ucenika)

    
    def dodaj_ucenika(self):
        ime = self.ime_entry.get().strip()
        prezime = self.prezime_entry.get().strip()
        razred = self.razred_entry.get().strip()

        if not ime or not prezime or not razred:
            messagebox.showwarning("Upozorenje", "Molimo unesite sve podatke!")
            return

        novi = Ucenik(ime, prezime, razred)
        self.ucenici.append(novi)
        self.osvjezi_prikaz()
        self.ocisti_unos()

    
    def osvjezi_prikaz(self):
        self.lista_ucenika.delete(0, tk.END)
        for u in self.ucenici:
            self.lista_ucenika.insert(tk.END, str(u))

    
    def odaberi_ucenika(self, event):
        odabrani = self.lista_ucenika.curselection()
        if not odabrani:
            return
        self.odabrani_ucenik_index = odabrani[0]
        u = self.ucenici[self.odabrani_ucenik_index]

        # popuni polja
        self.ime_entry.delete(0, tk.END)
        self.ime_entry.insert(0, u.ime)

        self.prezime_entry.delete(0, tk.END)
        self.prezime_entry.insert(0, u.prezime)

        self.razred_entry.delete(0, tk.END)
        self.razred_entry.insert(0, u.razred)

    
    def spremi_izmjene(self):
        if self.odabrani_ucenik_index is None:
            messagebox.showinfo("Info", "Prvo odaberite učenika za uređivanje.")
            return

        ime = self.ime_entry.get().strip()
        prezime = self.prezime_entry.get().strip()
        razred = self.razred_entry.get().strip()

        if not ime or not prezime or not razred:
            messagebox.showwarning("Upozorenje", "Sva polja moraju biti ispunjena!")
            return

        u = self.ucenici[self.odabrani_ucenik_index]
        u.ime = ime
        u.prezime = prezime
        u.razred = razred

        self.osvjezi_prikaz()
        self.ocisti_unos()
        self.odabrani_ucenik_index = None

    
    def ocisti_unos(self):
        self.ime_entry.delete(0, tk.END)
        self.prezime_entry.delete(0, tk.END)
        self.razred_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = EvidencijaApp(root)
    root.mainloop()
