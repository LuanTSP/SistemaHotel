import ttkbootstrap as ttk
import sqlite3
from MyWidgets import Integrated_Table_View, Integrated_Register_Form



class Controle_Consumos(ttk.Frame):
    def __init__(self, master, con: sqlite3.Connection, table_name: str):
        # initial setup
        super().__init__(master=master)

        # layout
        self.rowconfigure(index=(0,1), weight=1, uniform='a')
        self.columnconfigure(index=(0,1), weight=1, uniform='a')

        # widgets
        table = Integrated_Table_View(master=self, con=con, table_name='consumos')
        table.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)

        self.consumption_form = Consumption_Form(master=self, con=con, table_name='consumos', integrated_table=table, text='Consumption form')
        self.consumption_form.grid(row=0, column=1, sticky='nswe', padx=5, pady=5)

class Consumption_Form(Integrated_Register_Form):
    def __init__(self, master, con: sqlite3.Connection, table_name: str, integrated_table: Integrated_Table_View, text: str):
        # initial setup
        super().__init__(
            master=master,
            con=con,
            table_name=table_name,
            integrated_table=integrated_table,
            text=text
        )

        # layout
        self.rowconfigure(index=(0,1,2,3,4), weight=1, uniform='a')
        self.columnconfigure(index=(0,1,2,3,4,5), weight=1, uniform='a')

        # variables
        var_numapto = ttk.StringVar(value='')
        var_produto = ttk.StringVar(value='')
        var_prod_id = ttk.StringVar(value='')

        self.declare_variables([
            var_numapto,
            var_produto,
            var_prod_id,
        ])

        # widgets

        label_numapto = ttk.Label(master=self, text='NUM. APTO.')
        entry_numapto = ttk.Entry(master=self, textvariable=var_numapto)

        label_prodid = ttk.Label(master=self, text='PRODUCT ID')
        entry_prodid = ttk.Entry(master=self, textvariable=var_prod_id)

        btn_register = self.register_button(master=self)
        btn_register.configure(command=self.add_to_database_batch)

        # validation
        self.form_validation.validate_numeric(widget=entry_numapto, textvariable=var_numapto, required=True)
        self.form_validation.validate_numeric(widget=entry_prodid, textvariable=var_prod_id, required=True)

        # place
        label_numapto.grid(row=0, column=0, sticky='nswe')
        entry_numapto.grid(row=0, column=1, sticky='nswe', padx=5, pady=5)

        label_prodid.grid(row=0, column=2, sticky='nswe')
        entry_prodid.grid(row=0, column=3, sticky='nswe', padx=5, pady=5)

        btn_register.grid(row=4, column=5, sticky='nswe', padx=5, pady=5)
    
    def reservation_exists(self):
        try:
            results = self.con.execute(f"SELECT * FROM reservas WHERE numapto = {self.vars[0].get()}") # not valid value
        except:
            return False
        
        results = list(results)

        if len(results) >= 1: # results = [x]
            return True
        
        return False # results = []

    def product_exists(self):
        try:
            results = self.con.execute(f"SELECT * FROM {self.table_name} WHERE rowid = {self.vars[2].get()}") # not valid value
        except:
            return False
        
        results = list(results)

        if len(results) == 1: # results = [x]
            return True
        
        return False # results = []
    
    def product_avaliable(self):
        """
            Checks if there are enought items in stock in order to register a consumption.
        """
        # get quantity of items in stock
        quantity = self.con.execute(f"SELECT quantidade FROM produtos WHERE prod_id = {self.vars[2].get()}")
        quantity = int(list(quantity)[0][0])

        # check if items are sufficient
        if quantity < int(self.var_quantity.get()):
            return False

        return True




