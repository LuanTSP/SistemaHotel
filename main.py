import customtkinter as ctk
from MyWidgets import PandasTableView, ClientForm, MenuBar
import pandas as pd
import sqlite3


class App(ctk.CTk):
    def __init__(self):
        # initial setup
        super().__init__()
        ctk.set_appearance_mode('light')
        self.title('Sistema Hotel')
        self.geometry('1280x720')

        # layout
        self.rowconfigure(index=0, weight=1, uniform='a')
        self.rowconfigure(index=(1,2), weight=8, uniform='a')
        self.columnconfigure(index=(0,1), weight=1, uniform='a')

        # WIDGETS ->

        # menu bar
        menu = MenuBar(master=self)
        file_btn = menu.add_button(master=menu, text="File", command=lambda: print("File Button"))
        settings_btn = menu.add_button(master=menu, text="Settings", command=lambda: print("Settings Button"))
        menu.grid(row=0, column=0, columnspan=2, sticky='nswe')

        # connection to database
        con = sqlite3.connect('MyDb.db')
        
        # searchfield
        df = pd.read_sql("SELECT * FROM clientes", con=con)
        
        table = PandasTableView(master=self, rowdata=df)
        table.grid(row=1, column=1, rowspan=2, sticky='nswe')

        # client form
        client_form = ClientForm(master=self, con=con, table_name='clientes', pandas_table=table)
        client_form.grid(row=1, column=0, sticky='nswe')

        # run
        self.mainloop()





App()
