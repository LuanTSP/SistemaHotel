import customtkinter as ctk
from MyWidgets import Table
from CTkToolTip import CTkToolTip
import sqlite3
import pandas as pd

class App(ctk.CTk):
    def __init__(self):
        # initial setup
        super().__init__()
        self.geometry("500x500")
        self.title("Sistema de Cadastro")

        # layout
        self.rowconfigure(index=(0,1), weight=1, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')
        self.columnconfigure(index=1, weight=2, uniform='a')
        

        # widgets    
        search = SearchInDataBase(master=self)
        search.grid(row=0, column=1, sticky='nswe')

        # run
        self.mainloop()


class SearchInDataBase(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.nome = ctk.StringVar()

        # layout
        self.rowconfigure(index=0, weight=1, uniform='a')
        self.rowconfigure(index=1, weight=5, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')

        # widgets
        
        # Search Field
        frame1 = ctk.CTkFrame(master=self)
        
        frame1.rowconfigure(index=0, weight=1, uniform='a')
        frame1.columnconfigure(index=0, weight=4, uniform='a')
        frame1.columnconfigure(index=1, weight=1, uniform='a')

        frame1.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)

        entry = ctk.CTkEntry(master=frame1, placeholder_text='Enter a Name', textvariable=self.nome)
        entry.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)

        btn = ctk.CTkButton(master=frame1, text="Search", command=lambda: self.update_query(table=table, con=con))
        btn.grid(row=0, column=1, sticky='nswe', padx=5, pady=5)

        # Table
        frame2 = ctk.CTkScrollableFrame(master=self)
        frame2.grid(row=1, column=0, sticky='nswe')
        
        con = sqlite3.connect('MyDb.db')
        query = pd.read_sql("SELECT * FROM clientes", con=con)
        
        table = Table(master=frame2, values=query) 
        table.pack(fill='both', expand=True)

        # tooltips
        CTkToolTip(widget=btn, message="search by name")
        CTkToolTip(widget=entry, message="name")

    
    def update_query(self, table: Table, con):
        query = pd.read_sql(f"SELECT nome, idade FROM clientes WHERE nome LIKE '%{self.nome.get()}%'", con=con)
        new_data = query.to_numpy().tolist()
        new_data.insert(0, query.columns.values.tolist())
        table.update_values(new_data)



App()
