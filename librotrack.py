import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import datetime
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Publication:
    id: int
    type: str
    title: str
    author_or_publisher: str
    year: str
    available: bool = True
    borrowed_to: str = ''
    borrow_date: str = ''
    history: List[Dict] = field(default_factory=list)

    def display_label(self) -> str:
        status = '[POSUĐENO]' if not self.available else ''
        return f"{status} {self.title} — {self.author_or_publisher} ({self.year})"

    def to_xml_element(self) -> ET.Element:
        el = ET.Element('publication', attrib={'id': str(self.id), 'type': self.type})
        ET.SubElement(el, 'title').text = self.title
        ET.SubElement(el, 'author_or_publisher').text = self.author_or_publisher
        ET.SubElement(el, 'year').text = self.year
        ET.SubElement(el, 'available').text = '1' if self.available else '0'
        ET.SubElement(el, 'borrowed_to').text = self.borrowed_to
        ET.SubElement(el, 'borrow_date').text = self.borrow_date
        hist_el = ET.SubElement(el, 'history')
        for h in self.history:
            entry = ET.SubElement(hist_el, 'entry')
            ET.SubElement(entry, 'user').text = h.get('user','')
            ET.SubElement(entry, 'date').text = h.get('date','')
            ET.SubElement(entry, 'action').text = h.get('action','')
        return el
    @staticmethod
    def from_xml_element(el: ET.Element):
        id = int(el.attrib.get('id','0'))
        type = el.attrib.get('type','Knjiga')
        title = el.findtext('title','')
        aop = el.findtext('author_or_publisher','')
        year = el.findtext('year','')
        available = el.findtext('available','1') == '1'
        borrowed_to = el.findtext('borrowed_to','')
        borrow_date = el.findtext('borrow_date','')
        history = []
        hist_el = el.find('history')
        if hist_el is not None:
            for entry in hist_el.findall('entry'):
                history.append({
                    'user': entry.findtext('user',''),
                    'date': entry.findtext('date',''),
                    'action': entry.findtext('action','')
                })
        return Publication(id, type, title, aop, year, available, borrowed_to, borrow_date, history)


class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('LibroTrack — Školska knjižnica')
        self.geometry('900x540')

        self.publications: List[Publication] = []
        self.next_id = 1

        self.create_widgets()
        self.update_status_bar()

    def create_widgets(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Spremi...', command=self.save_xml)
        filemenu.add_command(label='Učitaj...', command=self.load_xml)
        filemenu.add_separator()
        filemenu.add_command(label='Izlaz', command=self.quit)
        menubar.add_cascade(label='Datoteka', menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label='O aplikaciji', command=self.show_about)
        menubar.add_cascade(label='Pomoć', menu=helpmenu)
        self.config(menu=menubar)

        left = ttk.Frame(self, padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left, text='Dodaj publikaciju', font=('Segoe UI', 12,'bold')).pack(anchor=tk.W)

        self.type_var = tk.StringVar(value='Knjiga')
        ttk.Radiobutton(left, text='Knjiga', variable=self.type_var, value='Knjiga').pack(anchor=tk.W)
        ttk.Radiobutton(left, text='Časopis', variable=self.type_var, value='Casopis').pack(anchor=tk.W)

        ttk.Label(left, text='Naslov:').pack(anchor=tk.W, pady=(8,0))
        self.title_entry = ttk.Entry(left, width=30)
        self.title_entry.pack(anchor=tk.W)

        ttk.Label(left, text='Autor / Izdavač:').pack(anchor=tk.W, pady=(6,0))
        self.aop_entry = ttk.Entry(left, width=30)
        self.aop_entry.pack(anchor=tk.W)

        ttk.Label(left, text='Godina:').pack(anchor=tk.W, pady=(6,0))
        self.year_entry = ttk.Entry(left, width=30)
        self.year_entry.pack(anchor=tk.W)

        ttk.Button(left, text='Dodaj publikaciju', command=self.add_publication).pack(pady=(10,0))

        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        ttk.Label(left, text='Filtri i pretraga', font=('Segoe UI', 11,'bold')).pack(anchor=tk.W)

        ttk.Label(left, text='Tip:').pack(anchor=tk.W, pady=(6,0))
        self.filter_type = tk.StringVar(value='Sve')
        ttk.Combobox(left, textvariable=self.filter_type, values=['Sve','Knjiga','Casopis'], state='readonly').pack(anchor=tk.W)

        ttk.Label(left, text='Status:').pack(anchor=tk.W, pady=(6,0))
        self.filter_status = tk.StringVar(value='Sve')
        ttk.Combobox(left, textvariable=self.filter_status, values=['Sve','Dostupno','Posuđeno'], state='readonly').pack(anchor=tk.W)

        ttk.Label(left, text='Traži (naslov / autor):').pack(anchor=tk.W, pady=(6,0))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(left, textvariable=self.search_var, width=30)
        search_entry.pack(anchor=tk.W)
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_list())

        ttk.Button(left, text='Primijeni filtre', command=self.refresh_list).pack(pady=(8,0))

        center = ttk.Frame(self, padding=10)
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(center, text='Publikacije', font=('Segoe UI', 12,'bold')).pack(anchor=tk.W)

        self.listbox = tk.Listbox(center, activestyle='none')
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-Button-1>', lambda e: self.show_history())

        btn_frame = ttk.Frame(center)
        btn_frame.pack(fill=tk.X, pady=8)

        ttk.Button(btn_frame, text='Posudi', command=self.borrow_selected).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text='Vrati', command=self.return_selected).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text='Povijest', command=self.show_history).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text='Izbriši', command=self.delete_selected).pack(side=tk.LEFT, padx=4)

        self.status_var = tk.StringVar()
        statusbar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=3)
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def add_publication(self):
        t = self.type_var.get()
        title = self.title_entry.get().strip()
        aop = self.aop_entry.get().strip()
        year = self.year_entry.get().strip()
        if not title:
            messagebox.showwarning('Greška', 'Naslov ne smije biti prazan')
            return
        pub = Publication(self.next_id, t, title, aop, year)
        self.next_id += 1
        self.publications.append(pub)
        self.title_entry.delete(0, tk.END)
        self.aop_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.refresh_list()
        self.update_status_bar()

    def get_selected_publication(self) -> Optional[Publication]:
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo('Info', 'Nijedna publikacija nije odabrana')
            return None
        idx = sel[0]
        filtered = self.get_filtered_publications()
        if idx >= len(filtered):
            return None
        return filtered[idx]

    def borrow_selected(self):
        pub = self.get_selected_publication()
        if not pub:
            return
        if not pub.available:
            messagebox.showinfo('Info', 'Publikacija je već posuđena')
            return
        user = simpledialog.askstring('Posudi', 'Unesite ime učenika/korisnika:')
        if not user:
            return
        today = datetime.date.today().isoformat()
        pub.available = False
        pub.borrowed_to = user
        pub.borrow_date = today
        pub.history.append({'user': user, 'date': today, 'action': 'posudba'})
        self.refresh_list()
        self.update_status_bar()

    def return_selected(self):
        pub = self.get_selected_publication()
        if not pub:
            return
        if pub.available:
            messagebox.showinfo('Info', 'Publikacija je već dostupna')
            return
        if not messagebox.askyesno('Potvrda', f'Potvrditi vraćanje: {pub.title}?'):
            return
        today = datetime.date.today().isoformat()
        user = pub.borrowed_to
        pub.available = True
        pub.borrowed_to = ''
        pub.borrow_date = ''
        pub.history.append({'user': user, 'date': today, 'action': 'vraćanje'})
        self.refresh_list()
        self.update_status_bar()

    def show_history(self):
        pub = self.get_selected_publication()
        if not pub:
            return
        hwin = tk.Toplevel(self)
        hwin.title(f'Povijest: {pub.title}')
        hwin.geometry('450x300')
        lbl = ttk.Label(hwin, text=f'Povijest posudbi za: {pub.title}', font=('Segoe UI', 11,'bold'))
        lbl.pack(anchor=tk.W, padx=8, pady=6)
        listbox = tk.Listbox(hwin)
        listbox.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
        if not pub.history:
            listbox.insert(tk.END, 'Prazna povijest')
        else:
            for e in pub.history:
                action = e.get('action','')
                user = e.get('user','')
                date = e.get('date','')
                listbox.insert(tk.END, f"{date} — {action} — {user}")
        ttk.Button(hwin, text='Zatvori', command=hwin.destroy).pack(pady=6)

    def delete_selected(self):
        pub = self.get_selected_publication()
        if not pub:
            return
        if not messagebox.askyesno('Brisanje', f'Želite li izbrisati: {pub.title}?'):
            return
        self.publications = [p for p in self.publications if p.id != pub.id]
        self.refresh_list()
        self.update_status_bar()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        filtered = self.get_filtered_publications()
        for p in filtered:
            self.listbox.insert(tk.END, p.display_label())

    def get_filtered_publications(self) -> List[Publication]:
        typ = self.filter_type.get()
        stat = self.filter_status.get()
        q = self.search_var.get().lower()
        res = []
        for p in self.publications:
            if typ != 'Sve' and p.type != typ:
                continue
            if stat == 'Dostupno' and not p.available:
                continue
            if stat == 'Posuđeno' and p.available:
                continue
            if q:
                if q not in p.title.lower() and q not in p.author_or_publisher.lower():
                    continue
            res.append(p)
        return res

    def update_status_bar(self):
        total = len(self.publications)
        available = sum(1 for p in self.publications if p.available)
        self.status_var.set(f'Ukupno: {total} | Dostupno: {available}')

    def show_about(self):
        messagebox.showinfo('O aplikaciji', 'LibroTrack — školska knjižnica\nVerzija: 1.0\nAutor: Agata Galant / 4.A')

    def save_xml(self):
        path = filedialog.asksaveasfilename(defaultextension='.xml', filetypes=[('XML files','*.xml')], title='Spremi knjižnicu')
        if not path:
            return
        root = ET.Element('library', attrib={'next_id': str(self.next_id)})
        for p in self.publications:
            root.append(p.to_xml_element())
        tree = ET.ElementTree(root)
        try:
            tree.write(path, encoding='utf-8', xml_declaration=True)
            messagebox.showinfo('Spremanje', 'Uspješno spremljeno')
        except Exception as e:
            messagebox.showerror('Greška', f'Ne mogu spremiti datoteku: {e}')

    def load_xml(self):
        path = filedialog.askopenfilename(filetypes=[('XML files','*.xml')], title='Učitaj knjižnicu')
        if not path:
            return
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            self.publications.clear()
            for el in root.findall('publication'):
                p = Publication.from_xml_element(el)
                self.publications.append(p)
            self.next_id = int(root.attrib.get('next_id', str(max((p.id for p in self.publications), default=0)+1)))
            self.refresh_list()
            self.update_status_bar()
            messagebox.showinfo('Učitavanje', 'Uspješno učitano')
        except Exception as e:
            messagebox.showerror('Greška', f'Ne mogu učitati datoteku: {e}')


if __name__ == '__main__':
    app = LibraryApp()
    app.mainloop()
