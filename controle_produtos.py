import ttkbootstrap as ttk
import sqlite3
from MyWidgets import Integrated_Table_View, Integrated_Register_Form


class Controle_Produtos(ttk.Frame):
    
    def __init__(self, master, con: sqlite3.Connection, table_name: str):
        # initial setup
        super().__init__(master=master)
        self.con = con
        self.table_name = table_name

        # layout
        self.rowconfigure(index=(0,1), weight=1, uniform='a')
        self.columnconfigure(index=(0,1), weight=1, uniform='a')

        # WIDGETS

        table = Integrated_Table_View(master=self, con=self.con, table_name=self.table_name)
        table.grid(row=0, column=0, sticky='nswe')

        self.products_form = Products_Form(master=self, con=self.con, table_name=self.table_name, integrated_table=table)
        self.products_form.grid(row=0, column=1, sticky='nswe')


class Products_Form(Integrated_Register_Form):

    def __init__(self, master, con: sqlite3.Connection, table_name: str, integrated_table:Integrated_Table_View=None, text='Produtos'):
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
        self.columnconfigure(index=(0,1,2,3,4,5), weight=1, uniform='a')

        # variables
        var_produto = ttk.StringVar(value='')
        var_descr = ttk.StringVar(value='')
        var_valor = ttk.StringVar(value='')
        var_quantidade = ttk.StringVar(value='')

        self.declare_variables([
            var_produto,
            var_descr,
            var_valor,
            var_quantidade
        ])

        # fields
        label_produto = ttk.Label(master=self, text='PRODUTO')
        entry_produto = ttk.Entry(master=self, textvariable=var_produto)

        label_descr = ttk.Label(master=self, text='DESCR.')
        entry_descr = ttk.Entry(master=self, textvariable=var_descr)

        label_valor = ttk.Label(master=self, text='VALOR')
        entry_valor = ttk.Entry(master=self, textvariable=var_valor)

        label_quantidade = ttk.Label(master=self, text='QUANT.')
        entry_quantidade = ttk.Entry(master=self, textvariable=var_quantidade)

        btn_register = self.register_button(master=self)
        btn_edit = self.edit_button(master=self)
        btn_save_edit = self.save_edit_button(master=self)
        btn_clear = self.clear_form_button(master=self)
        btn_delete = self.delete_button(master=self)

        # validation
        self.form_validation.validate_text(widget=entry_produto, textvariable=var_produto, required=True)
        self.form_validation.validate_text(widget=entry_descr, textvariable=var_descr)
        self.form_validation.validate_numeric(widget=entry_valor, textvariable=var_valor, required=True)
        self.form_validation.validate_numeric(widget=entry_quantidade, textvariable=var_quantidade, required=True)

        # place
        label_produto.grid(row=0, column=0, sticky='nswe')
        entry_produto.grid(row=0, column=1, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_descr.grid(row=0, column=3, sticky='nswe')
        entry_descr.grid(row=0, column=4, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_valor.grid(row=1, column=0, sticky='nswe')
        entry_valor.grid(row=1, column=1, columnspan=1, sticky='nswe', padx=5, pady=5)

        label_quantidade.grid(row=1, column=2, sticky='nswe')
        entry_quantidade.grid(row=1, column=3, columnspan=1, sticky='nswe', padx=5, pady=5)

        btn_register.grid(row=5, column=5, sticky='nswe', padx=5, pady=5)
        btn_edit.grid(row=5, column=4, sticky='nswe', padx=5, pady=5)
        btn_save_edit.grid(row=4, column=4, sticky='nswe', padx=5, pady=5)
        btn_clear.grid(row=5, column=0, sticky='nswe', padx=5, pady=5)
        btn_delete.grid(row=4, column=0, sticky='nswe', padx=5, pady=5)


