import customtkinter as ctk
from MyWidgets import SearchInDatabase, Database
import sqlite3

class App(ctk.CTk):
    def __init__(self):
        # initial setup
        super().__init__()
        self.geometry("800x500")
        self.title("Sistema de Cadastro")

        # layout
        self.rowconfigure(index=(0,1), weight=1, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')
        self.columnconfigure(index=1, weight=2, uniform='a')
        

        # widgets
        con = sqlite3.connect('MyDb.db')
        search = SearchInDatabase(master=self, by='nome', con=con, table_name='clientes', display_table_cols=['nome', 'sobrenome', 'idade', 'cpf'])
        search.grid(row=0, column=1, sticky='nswe')

        database = Database(con=con)
        print(database.read("SELECT nome, idade FROM clientes WHERE nome = 'Ferdinando'", return_as='dict'))

        # run
        self.mainloop()


App()
