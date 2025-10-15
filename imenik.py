import tkinter as tk
from tkinter import messagebox
import csv
import os

class Kontakt:
    def __init__(self, ime, email, telefon):
        self.ime = ime
        self.email = email
        self.telefon = telefon

    def __str__(self):
        return f"{self.ime}, {self.email}, {self.telefon}"

class ImenikApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Imenik kontakata")
        self.kontakti = []

        frame_gornji=tk.Frame(root, padx=10, pady=10)
        frame_gornji.grid(row=0, column=0, sticky="ew")

        frame_srednji=tk.Frame(root, padx=10, pady=10)
        frame_srednji.grid(row=1, column=0, sticky="ew")

        tk.Label(frame_gornji, text='Ime i Prezime:').grid(row=0, column=0, sticky="e")
        tk.Label(frame_gornji, text='Email:').grid(row=1, column=0, sticky="e")
        tk.Label(frame_gornji, text='Telefon:').grid(row=2, column=0, sticky="e")

        self.entry_ime = tk.Entry(frame_gornji, width=30)
        self.entry_email = tk.Entry(frame_gornji, width=30)
        self.entry_telefon = tk.Entry(frame_gornji, width=30)
    
        self.entry_ime.grid(row=0, column=1, padx=5, pady=2)
        self.entry_email.grid(row=1, column=1, padx=5, pady=2)
        self.entry_telefon.grid(row=2, column=1, padx=5, pady=2)

        tk.Button(frame_gornji, text='Dodaj kontakt', command=self.dodaj_kontakt).grid(row=3, column=0, columnspan=2, pady=5)
    
        self.listbox_kontakti = tk.Listbox(frame_srednji, width=50, height=10)
        self.scrollbar = tk.Scrollbar(frame_srednji, orient="vertical", command=self.listbox_kontakti.yview)
        self.listbox_kontakti.config(yscrollcommand=self.scrollbar.set)

        self.listbox_kontakti.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        frame_srednji.rowconfigure(0, weight=1)
        frame_srednji.columnconfigure(0, weight=1)

        tk.Button(frame_srednji, text="Spremi kontakte", command=self.spremi_kontakte).grid(row=0, column=0, padx=5)
        tk.Button(frame_srednji, text="Učitaj kontakte", command=self.ucitaj_kontakte).grid(row=0, column=1, padx=5)
        tk.Button(frame_srednji, text="Obriši kontakt", command=self.obrisi_kontakt).grid(row=0, column=2, padx=5)

        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)
 
        self.ucitaj_kontakte()

    def dodaj_kontakt(self):
        ime = self.entry_ime.get().strip()
        email = self.entry_email.get().strip()
        telefon = self.entry_telefon.get().strip()

        if not ime or not email or not telefon:
            messagebox.showwarning("Greška", "Sva polja moraju biti ispunjena!")
            return

        novi_kontakt = Kontakt(ime, email, telefon)
        self.kontakti.append(novi_kontakt)
        self.osvjezi_listbox()

        self.entry_ime.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefon.delete(0, tk.END)

    def osvjezi_listbox(self):
        self.listbox_kontakti.delete(0, tk.END)
        for kontakt in self.kontakti:
            self.listbox_kontakti.insert(tk.END, str(kontakt))
    
    def spremi_kontakte(self):
        with open("kontakti.csv","w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for kontakt in self.kontakti:
                writer.writerow([kontakt.ime, kontakt.email, kontakt.telefon])
        messagebox.showinfo("Uspjeh", "Kontakti su uspješno spremljeni.")

    def ucitaj_kontakte(self):
        self.kontakti.clear()
        try:
            with open("kontakti.csv","r", encoding= 'utf-8') as f:
                reader = csv.reader(f)
                for red in reader:
                    if len(red) == 3:
                        ime, email, telefon = red
                        self.kontakti.append(Kontakt(ime, email, telefon))
            self.osvjezi_listbox()
        except FileNotFoundError:
            pass

    def obrisi_kontakt(self):
        selekcija = self.listbox_kontakti.curselection()
        if not selekcija:
            messagebox.showwarning("Greška", "Odaberite kontakt za brisanje!")
            return
        index = selekcija[0]
        kontakt = self.kontakti[index]
 
        if messagebox.askyesno("Potvrda", f"Želite li obrisati kontakt {kontakt.ime}?"):
            self.kontakti.pop(index)
            self.osvjezi_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImenikApp(root)
    root.mainloop()