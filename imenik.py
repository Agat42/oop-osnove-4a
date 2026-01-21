import sqlite3


def inicijalizacija():
    conn = sqlite3.connect("Imenik.db")
    cur = conn.cursor()

    sql = """
    CREATE TABLE IF NOT EXISTS Kontakti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ime_prezime TEXT NOT NULL,
        broj_mobitela TEXT NOT NULL
    );
    """
    cur.execute(sql)
    conn.commit()
    conn.close()



def unesi_kontakt():
    ime = input("Unesi ime i prezime: ")
    broj = input("Unesi broj mobitela: ")

    conn = sqlite3.connect("Imenik.db")
    cur = conn.cursor()

    sql = "INSERT INTO Kontakti (ime_prezime, broj_mobitela) VALUES (?, ?)"
    cur.execute(sql, (ime, broj))

    conn.commit()
    conn.close()
    print("✅ Kontakt uspješno dodan!")



def ispisi_kontakte():
    conn = sqlite3.connect("Imenik.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM Kontakti")
    kontakti = cur.fetchall()

    print("\n--- TELEFONSKI IMENIK ---")
    print(f"{'ID':<5} | {'IME I PREZIME':<25} | BROJ")
    print("-" * 50)

    for k in kontakti:
        print(f"{k[0]:<5} | {k[1]:<25} | {k[2]}")

    conn.close()



def obrisi_kontakt():
    ispisi_kontakte()
    id_brisanje = input("\nUnesi ID kontakta za brisanje: ")

    conn = sqlite3.connect("Imenik.db")
    cur = conn.cursor()

    sql = "DELETE FROM Kontakti WHERE id = ?"
    cur.execute(sql, (id_brisanje,))

    if cur.rowcount > 0:
        print("🗑️ Kontakt obrisan.")
    else:
        print("❌ Ne postoji kontakt s tim ID-em.")

    conn.commit()
    conn.close()



def izbornik():
    while True:
        print("""
--- TELEFONSKI IMENIK ---
1. Unos novog kontakta
2. Ispis svih kontakata
3. Brisanje kontakta
4. Izlaz
""")

        izbor = input("Odaberi opciju: ")

        if izbor == "1":
            unesi_kontakt()
        elif izbor == "2":
            ispisi_kontakte()
        elif izbor == "3":
            obrisi_kontakt()
        elif izbor == "4":
            print("👋 Izlaz iz programa.")
            break
        else:
            print("❌ Neispravan odabir!")



inicijalizacija()
izbornik()
