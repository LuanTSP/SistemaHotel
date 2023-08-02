import ttkbootstrap as ttk
import customtkinter as ctk
from ttkbootstrap.tableview import Tableview
import pandas as pd
import numpy as np
import sqlite3


class App(ctk.CTk):
    def __init__(self):
        # initial setup
        super().__init__()
        ctk.set_appearance_mode('light')
        self.title('Sistema Hotel')
        self.geometry('800x600')

        # layout
        self.rowconfigure(index=0, weight=1, uniform='a')
        self.rowconfigure(index=1, weight=9, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')

        # connection to database
        con = sqlite3.connect('MyDb.db')
        
        # searchfield
        df = pd.read_sql("SELECT * FROM clientes", con=con)
        # headers = ['nome', 'idade']
        
        table = PandasTableView(master=self, rowdata=df)
        table.grid(row=1, column=0, sticky='nswe')

        # run
        self.mainloop()



class PandasTableView(Tableview):
    def __init__(self,
            master, 
            rowdata=[],
            paginated=False,
            searchable=True,
            headers=[],
            bootstyle='litera',
        ):
        self.headers = headers
        self.rowdata = rowdata
        
        # Cheacks if row data is pandas dataframe
        if isinstance(rowdata, pd.DataFrame):
            if self.headers == []:
                self.headers = rowdata.columns.values
            self.rowdata  = rowdata[self.headers].to_numpy().tolist()
            

        # initial setup
        super().__init__(
            master=master,
            rowdata=self.rowdata,
            coldata=self.headers,
            paginated=paginated,
            searchable=searchable,
            bootstyle=bootstyle,
        )

App()
