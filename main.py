import customtkinter as ctk
from MyWidgets import PandasTableView, ClientForm
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
        self.rowconfigure(index=(1,2), weight=10, uniform='a')
        self.columnconfigure(index=(0,1), weight=1, uniform='a')

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
