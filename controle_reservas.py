from MyWidgets import Integrated_Form, Integrated_Table_View
import ttkbootstrap as ttk
import sqlite3

class Controle_Reservas(ttk.Frame):
    def __init__(self, master, con: sqlite3.Connection, table_name: str):
        # initial setup
        self.con = con
        self.table_name = table_name
        super().__init__(master=master)

        # layout
        self.rowconfigure(index=(0,1), weight=1, uniform='a')
        self.columnconfigure(index=(0,1), weight=1, uniform='a')

        # WIDGETS

        # integrated table
        table = Integrated_Table_View(master=self, con=self.con, table_name='reservas', paginated=True)
        table.grid(row=0, column=0, rowspan=2, sticky='nswe')

        # reservation form
        reservation_form = Reservation_Form(master=self, con=self.con, table_name='reservas', integrated_table=table, text='Reservation Form')
        reservation_form.grid(row=0, column=1, sticky='nswe')


class Reservation_Form(Integrated_Form):
    def __init__(self, master, con: sqlite3.Connection, table_name: str, integrated_table: str, text='Table'):
        super().__init__(
            master=master,
            con=con,
            table_name=table_name,
            integrated_table=integrated_table,
            text=text
        )

        # layout
        self.rowconfigure(index=(0,1,2,3,4,5), weight=1, uniform='a')
        self.columnconfigure(index=(0,1,2,3,4,5), weight=1, uniform='a')

        # VARIABLES
        var_nome = ttk.StringVar(value='')

        self.vars = [
            var_nome,
        ]

        # WIDGETS
        
        # create widgets
        label_nome = ttk.Label(master=self, text='NOME')
        entry_nome = ttk.Entry(master=self, textvariable=var_nome)



        btn_register = self.register_button(master=self)
        btn_edit = self.edit_button(master=self)
        btn_save_edit = self.save_edit_button(master=self)
        btn_clear_form = self.clear_form_button(master=self)
        btn_delete = self.delete_button(master=self)

        # place
        label_nome.grid(row=0, column=0, sticky='nswe')
        entry_nome.grid(row=0, column=1, columnspan=2, sticky='nswe')

        btn_register.grid(row=0, column=5, sticky='nswe', padx=5, pady=5)
        btn_edit.grid(row=1, column=5, sticky='nswe', padx=5, pady=5)
        btn_save_edit.grid(row=2, column=5, sticky='nswe', padx=5, pady=5)
        btn_clear_form.grid(row=3, column=5, sticky='nswe', padx=5, pady=5)
        btn_delete.grid(row=4, column=5, sticky='nswe', padx=5, pady=5)
        
