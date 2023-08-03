import CTkTable
import pandas as pd
import numpy as np
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import add_range_validation, add_regex_validation, add_text_validation
import sqlite3

# WIDGETS
class Table(CTkTable.CTkTable):
    """
        A Table that inherits from CTkTable and can acccept data from
        pandas.DataFrames and dicts on the format 
        {"key1": [value1, value2, ...], "Key2": [valu3, value4, ...], ...}
    """
    def __init__(self, master, values, command=lambda event: event):
        # initial setup
        self.values = values
        
        self.values_to_list()
        
        super().__init__(
            master=master,
            values=self.values,
            font=('Arial', 12, 'bold'),
            hover=True,
            hover_color="#1f1f1f",
            header_color="#5f5f5f",
            command=command,
            corner_radius=0)
    
    def values_to_list(self):
        """
            Checks if the values input is pd.DataFrame or dict and parses to list
        """
        if isinstance(self.values, pd.DataFrame):
            new_data = self.values.to_numpy().tolist()
            new_data.insert(0, self.values.columns.values.tolist())
            self.values = new_data
        if isinstance(self.values, dict): 
            header = list(self.values.keys())
            new_data = []
            for key in header:
                new_data.append(self.values[key])
            new_data = np.array(new_data).T.tolist()
            new_data.insert(0, header)
            self.values = new_data


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
        
        # Checks if row data is pandas dataframe
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


class ClientForm(ttk.Labelframe):
    def __init__(self, master, con: sqlite3.Connection, table_name: str, pandas_table=None):
        # initial setup
        self.con = con
        self.table_name = table_name
        self.pandas_table = pandas_table
        super().__init__(master=master, text='Cadastro de Clientes')

        # layout
        self.rowconfigure(index=(0,1,2,3,4,5,6,7), weight=1, uniform='a')
        self.columnconfigure(index=(0,1,2,3,4,5,6,7), weight=1, uniform='a')
        
        # Nome, Sobrenome, Idade, cpf,
        self.var_nome = ttk.StringVar()
        label_nome = ttk.Label(master=self, text='Nome')
        entry_nome = ttk.Entry(master=self, textvariable=self.var_nome)
        add_text_validation(entry_nome, when='focusout')
        label_nome.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)
        entry_nome.grid(row=0, column=1, columnspan=2, sticky='nswe', padx=5, pady=5)

        self.var_sobrenome = ttk.StringVar()
        label_sobrenome = ttk.Label(master=self, text='sobrenome')
        entry_sobrenome = ttk.Entry(master=self, textvariable=self.var_sobrenome)
        add_text_validation(entry_sobrenome, when='focusout')
        label_sobrenome.grid(row=0, column=3, sticky='nswe', padx=5, pady=5)
        entry_sobrenome.grid(row=0, column=4, columnspan=4, sticky='nswe', padx=5, pady=5)

        self.var_idade = ttk.StringVar()
        label_idade = ttk.Label(master=self, text='idade')
        entry_idade = ttk.Entry(master=self, textvariable=self.var_idade)
        add_range_validation(entry_idade, startrange=0, endrange=120, when='focusout')
        label_idade.grid(row=1, column=0, sticky='nswe', padx=5, pady=5)
        entry_idade.grid(row=1, column=1, columnspan=1, sticky='nswe', padx=5, pady=5)

        self.var_cpf = ttk.StringVar()
        label_cpf = ttk.Label(master=self, text='cpf')
        entry_cpf = ttk.Entry(master=self, textvariable=self.var_cpf)
        add_regex_validation(entry_cpf, pattern='^[0-9]{11}$', when='focusout')
        label_cpf.grid(row=1, column=2, sticky='nswe', padx=5, pady=5)
        entry_cpf.grid(row=1, column=3, columnspan=2, sticky='nswe', padx=5, pady=5)

        self.vars = [self.var_nome, self.var_sobrenome, self.var_cpf, self.var_idade]

        # adicionar ao bando de dados
        btn_cadastrar = ttk.Button(master=self, text='Cadastrar', command=self.add_to_database)
        btn_cadastrar.grid(row=7, column=6, columnspan=2,sticky='nswe', padx=5, pady=5)

    def add_to_database(self):
        cursor = self.con.cursor()
        cursor.execute(f"INSERT INTO {self.table_name} (nome, sobrenome, cpf, idade) VALUES ('{self.var_nome.get()}', '{self.var_sobrenome.get()}', {str(self.var_cpf.get())}, {str(self.var_idade.get())})")
        self.con.commit()

        if self.pandas_table and isinstance(self.pandas_table, PandasTableView):
            values = [self.var_nome.get(), self.var_sobrenome.get(), self.var_cpf.get(), self.var_idade.get()]
            self.pandas_table.insert_row(index='end', values=values)
            self.pandas_table.load_table_data(clear_filters=True)
            self.clear_form()
    
    def clear_form(self):
        for var in self.vars:
            var.set(value='')

                    
class MenuBar(ttk.Frame):
    def __init__(self, master):
        # initial setup
        super().__init__(master=master, bootstyle="dark")
    
    def add_button(self, master, text: str, command=lambda x:x):
        btn = ttk.Button(master=master, text=text, command=command)
        btn.pack(side='left', fill='y', padx=5, pady=5)
        return btn



