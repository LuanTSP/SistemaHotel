import ttkbootstrap as ttk
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.dialogs import Messagebox
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

        self.consumption_form = Consumption_Form(master=self, con=con, table_name='consumos', integrated_table=table, text='Consumos')
        self.consumption_form.grid(row=0, column=1, sticky='nswe', padx=5, pady=5)


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
        self.var_quantity = ttk.StringVar(value='')
        
        self.declare_variables([
            self.var_numapto,
            self.var_produto,
            self.var_prod_id,
        ])

        self.declare_aditional_varibles(add_vars=[
            self.var_quantity,
        ])

        # widgets
        label_numapto = ttk.Label(master=self, text='APTO.')
        entry_numapto = ttk.Entry(master=self, textvariable=self.var_numapto)

        label_prod_id = ttk.Label(master=self, text='PROD. ID')
        entry_prod_id = ttk.Entry(master=self, textvariable=self.var_prod_id)

        label_quantity = ttk.Label(master=self, text='QUANT.')
        entry_quantity = ttk.Entry(master=self, textvariable=self.var_quantity)

        btn_register = self.register_button(master=self)
        btn_register.configure(command=self.register_multiple)

        btn_delete = self.delete_button(master=self)
        btn_edit = self.edit_button(master=self)
        btn_save_edit = self.save_edit_button(master=self)
        btn_clear = self.clear_form_button(master=self)

        # validation
        self.form_validation.validate_numeric(widget=entry_numapto, textvariable=self.var_numapto, required=True)
        self.form_validation.validate_numeric(widget=entry_prod_id, textvariable=self.var_prod_id, required=True)
        self.form_validation.validate_range(widget=entry_quantity, textvariable=self.var_quantity, start=0, end=1000, required=True)

        # place
        label_numapto.grid(row=0, column=0, sticky='nswe')
        entry_numapto.grid(row=0, column=1, sticky='nswe', padx=5, pady=5)

        label_prod_id.grid(row=0, column=2, sticky='nswe')
        entry_prod_id.grid(row=0, column=3, sticky='nswe', padx=5, pady=5)

        label_quantity.grid(row=1, column=0, sticky='nswe')
        entry_quantity.grid(row=1, column=1, sticky='nswe', padx=5, pady=5)

        btn_delete.grid(row=5, column=0, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_clear.grid(row=6, column=0, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_edit.grid(row=6, column=3, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_save_edit.grid(row=5, column=3, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_register.grid(row=6, column=5, columnspan=2, sticky='nswe', padx=5, pady=5)
    
    def register_multiple(self):
        """
            Add form data to the database in multiple times
        """
        # check if form is valid and display toast notification
        if not self.form_validation.check_validation():
            toast = ToastNotification(title="Invalid Form", message="Please fill all fields required.", bootstyle='danger', icon='', duration=3000, position=(0,0,'nw'))
            toast.show_toast()
            return
        
        # user confirmation input
        ans = Messagebox().yesno(message=f"Confirm operation: \n insert data into {self.table_name} ?", title='Confirm', bootstyle='warning', parent=self)
        if not ans == 'Yes':
            toast = ToastNotification(title="Info", message="Operation Canceled.", bootstyle='info', icon='', duration=3000, position=(0,0,'nw'))
            toast.show_toast()
            return
        
        # check produtos
        if not self.product_is_avaliable():
            toast = ToastNotification(title="Error", message="Product Not Found or Quantity Not Enought.", bootstyle='danger', icon='', duration=3000, position=(0,0,'nw'))
            toast.show_toast()
            return
        
        # check reservation
        if not self.reservation_is_avaliable():
            toast = ToastNotification(title="Error", message="Reservation Not Found.", bootstyle='danger', icon='', duration=3000, position=(0,0,'nw'))
            toast.show_toast()
            return
        
        # get name of product
        results = self.con.execute(f"SELECT produto FROM produtos WHERE rowid = {self.var_prod_id.get()}")
        self.var_produto.set(list(results)[0][0])

        # insert values into database
        columns, data, _ = self.get_form_data()
        q = int(self.var_quantity.get())
        values = data
        if q > 0:
            for _ in range(q - 1):
                values += ', ' + data
            
            cursor = self.con.cursor()
            cursor.execute(f"INSERT INTO {self.table_name} {columns} VALUES {values}")
            self.con.commit()
        
        # update quantity data in produtos
        quantity = int(list(self.con.execute(f"SELECT quantidade FROM produtos WHERE rowid = {self.var_prod_id.get()}"))[0][0])
        self.con.execute(f"UPDATE produtos SET quantidade = {quantity - q} WHERE rowid = {self.var_prod_id.get()}")
        self.linked_table.update_table()

        # display toast notification if success
        toast = ToastNotification(title="Success", message="Data added to database.", bootstyle='success', icon='', duration=3000, position=(0,0,'nw'))
        toast.show_toast()

        # updates pandas table if there is pandas table connected
        if isinstance(self.integrated_table, Integrated_Table_View):
            self.integrated_table.update_table()
        
        # clear form
        self.clear_form()

    def product_is_avaliable(self):
        """
            Checks if product is avalible to be consumed
        """
        results = list(self.con.execute(f"SELECT quantidade FROM produtos WHERE rowid = {self.var_prod_id.get()}"))
        if len(results) == 0:
            return False        
        
        q = int(results[0][0])
        if int(self.var_quantity.get()) > q:
            return False
        
        return True

    def reservation_is_avaliable(self):
        result = list(self.con.execute(f"SELECT numapto FROM reservas WHERE numapto = {self.var_numapto.get()}"))

        if len(result) == 0:
            return False
        return True