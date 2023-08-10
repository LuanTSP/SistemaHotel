from MyWidgets import MenuBar
from controle_clientes import Controle_Clientes
from controle_reservas import Controle_Reservas
from controle_produtos import Controle_Produtos
from controle_consumos import Controle_Consumos
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
        
        controle_reservas = Controle_Reservas(master=notebook, con=self.con, table_name='reservas')
        controle_reservas.pack(fill='both', expand=True)

        controle_produtos = Controle_Produtos(master=notebook, con=self.con, table_name='produtos')
        controle_produtos.pack(fill='both', expand=True)

        controle_consumos = Controle_Consumos(master=notebook, con=self.con, table_name='consumos')
        controle_consumos.pack(fill='both', expand=True)
        
        # linking forms
        controle_clientes.client_form.link(integrated_form=controle_reservas.reservation_form)
        controle_consumos.consumption_form.link(integrated_form=controle_produtos.products_form)

        # adding to notebook
        notebook.add(child=controle_clientes, text='Clientes')
        notebook.add(child=controle_reservas, text='Reservas')
        notebook.add(child=controle_produtos, text='Produtos')
        notebook.add(child=controle_consumos, text='Consumos')

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
                (
                    client_id INTEGER PRIMARY KEY,
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
                    defic TEXT
                )
            """)
        
        # create table reservas
        con.execute("""
            CREATE TABLE IF NOT EXISTS reservas
            (
                reservation_id INTEGER PRIMARY KEY,
                nome TEXT,
                cpf TEXT,
                nasc TEXT,
                celular TEXT,
                email TEXT,
                empresa TEXT,
                dtinicio TEXT,
                dtfinal TEXT,
                diareserva TEXT,
                qthospede TEXT,
                numapto TEXT,
                nomeacp1 TEXT,
                rgacp1 TEXT,
                nomeacp2 TEXT,
                rgacp2 TEXT,
                nomeacp3 TEXT,
                rgacp3 TEXT,
                nomeacp4 TEXT,
                rgacp4 TEXT
            )
        """)

        # create table produtos
        con.execute("""
            CREATE TABLE IF NOT EXISTS produtos
            (
                prod_id INTEGER PRIMARY KEY,
                produto TEXT,
                descr TEXT,
                valor TEXT,
                quantidade TEXT
            )     
        """)

        # create table consumos
        con.execute("""
            CREATE TABLE IF NOT EXISTS consumos 
            (
                cons_id INTEGER PRIMARY KEY,
                numapto TEXT,
                produto TEXT,
                prod_id TEXT
            )
        """)

        return con


App()
