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

        consumption_form = Consumption_Form(master=self, con=con, table_name='consumos', integrated_table=table, text='Consumos')
        consumption_form.grid(row=0, column=1, sticky='nswe', padx=5, pady=5)


class Consumption_Form(Integrated_Register_Form):
    def __init__(self, master, con, table_name, integrated_table, text):
        # initial setup
        super().__init__(
            master=master,
            con=con,
            table_name=table_name,
            integrated_table=integrated_table,
            text=text
        )

        # layout
        self.rowconfigure(index=(0,1,2,3,4,5), weight=1, uniform='a')
        self.columnconfigure(index=(0,1,2,3,4,5,6), weight=1, uniform='a')

        # variables
        self.var_numapto = ttk.StringVar(value='')
        self.var_produto = ttk.StringVar(value='')
        self.var_prod_id = ttk.StringVar(value='')
        
        self.declare_variables([
            self.var_numapto,
            self.var_produto,
            self.var_prod_id,
        ])

        # widgets
        label_numapto = ttk.Label(master=self, text='APTO.')
        entry_numapto = ttk.Entry(master=self, textvariable=self.var_numapto)

        label_prod_id = ttk.Label(master=self, text='PROD. ID')
        entry_prod_id = ttk.Entry(master=self, textvariable=self.var_prod_id)

        # validation
        self.form_validation.validate_numeric(widget=entry_numapto, textvariable=self.var_numapto, required=True)
        self.form_validation.validate_numeric(widget=entry_prod_id, textvariable=self.var_prod_id,required=True)

        # place
        label_numapto.grid(row=0, column=0, sticky='nswe')
        entry_numapto.grid(row=0, column=1, sticky='nswe', padx=5, pady=5)

        label_prod_id.grid(row=0, column=2, sticky='nswe')
        entry_prod_id.grid(row=0, column=3, sticky='nswe', padx=5, pady=5)
