from MyWidgets import MenuBar
from controle_clientes import Controle_Clientes
import ttkbootstrap as ttk
import sqlite3
import os

class App(ttk.Window):
    def __init__(self):
        # initial setup
        super().__init__(themename='solar')
        self.title('Sistema Hotel')
        self.geometry('2000x2000')

        # Connect to databases
        self.con = self.make_connection()


        # layout
        self.rowconfigure(index=0, weight=1, uniform='a')
        self.rowconfigure(index=1, weight=13, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')

        # WIDGETS

        # menu bar
        menu = MenuBar(master=self)
        menu.add_button(master=menu, text="File", command=lambda: print("File Button"))
        menu.add_button(master=menu, text="Settings", command=lambda: print("Settings Button"))
        menu.grid(row=0, column=0, sticky='nswe')

        # tabs
        notebook = ttk.Notebook(master=self)
        notebook.grid(row=1, column=0, sticky='nswe', padx=5, pady=5)

        # Systems
        controle_clientes = Controle_Clientes(master=notebook, con=self.con, table_name='clientes')
        controle_clientes.pack(fill='both', expand=True)

        # adding to notebook
        notebook.add(child=controle_clientes, text='Clientes')

        # run
        self.mainloop()

    def make_connection(self):
        """
            Makes Connection to Database
            if database does not exist, creates it
            along with table 'clientes' and default columns
        """
        data_path = './Database/'
        filename = 'base.db'
        os.makedirs(data_path, exist_ok=True)
        con = sqlite3.connect(database=data_path + filename)
        
        # create table clientes
        con.execute("""
            CREATE TABLE IF NOT EXISTS clientes
                (client_id INTEGER PRIMARY KEY,
                nome TEXT,
                rg TEXT,
                cpf TEXT,
                endereco TEXT,
                cidade TEXT,
                estado TEXT,
                pais TEXT,
                cep TEXT,
                nasc TEXT,
                sexo TEXT,
                celular TEXT,
                email TEXT,
                empresa TEXT,
                cargo TEXT,
                escolaridade TEXT,
                profis TEXT,
                defic TEXT)
            """)
        
        # create table reservas
        # ... TO DO
        return con


App()
