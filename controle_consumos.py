import ttkbootstrap as ttk
import sqlite3
from MyWidgets import Integrated_Register_Form, Integrated_Table_View



class Controle_Consumos(ttk.Frame):
    def __init__(self, master, con: sqlite3.Connection, table_name: str):
        # initial setup
        super().__init__(
            master=master,
        )
    
        # layout
        self.rowconfigure(index=(0,1), weight=1, uniform='a')
        self.columnconfigure(index=(0,1), weight=1, uniform='a')

        # widgets
        table = Integrated_Table_View(master=self, con=con, table_name=table_name, paginated=True)
        table.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)