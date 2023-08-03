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
            pagesize=100,
            stripecolor=("#efefef", None)
        )
        self.autofit_columns()


class ClientForm(ttk.Labelframe):
    def __init__(self, master, con: sqlite3.Connection, table_name: str, pandas_table=None):
        # initial setup
        self.con = con
        self.table_name = table_name
        self.pandas_table = pandas_table
        super().__init__(master=master, text='Cadastro de Clientes')

        # layout
        self.rowconfigure(index=(0,1,2,3,4,5,6,7), weight=1, uniform='a')
        self.columnconfigure(index=(0,1,2,3,4,5,6,7,8,9), weight=1, uniform='a')
        
        # varibles
        self.var_nome = ttk.StringVar(value='')
        self.var_rg = ttk.StringVar(value='')
        self.var_cpf = ttk.StringVar(value='')
        self.var_endereco = ttk.StringVar(value='')
        self.var_cidade = ttk.StringVar(value='')
        self.var_estado = ttk.StringVar(value='')
        self.var_pais = ttk.StringVar(value='')
        self.var_cep = ttk.StringVar(value='')
        self.var_nasc = ttk.StringVar(value='')
        self.var_sexo = ttk.StringVar(value='')
        self.var_celular = ttk.StringVar(value='')
        self.var_email = ttk.StringVar(value='')
        self.var_empresa = ttk.StringVar(value='')
        self.var_cargo = ttk.StringVar(value='')
        self.var_escolaridade = ttk.StringVar(value='')
        self.var_profis = ttk.StringVar(value='')
        self.var_defic = ttk.StringVar(value='')

        self.vars = [
            self.var_nome, 
            self.var_rg, 
            self.var_cpf, 
            self.var_endereco,
            self.var_cidade,
            self.var_estado,
            self.var_pais,
            self.var_cep,
            self.var_nasc,
            self.var_sexo,
            self.var_celular,
            self.var_email,
            self.var_empresa,
            self.var_cargo,
            self.var_escolaridade,
            self.var_profis,
            self.var_defic,
        ]

        # create widgets
        label_nome = ttk.Label(master=self, text='NOME')
        entry_nome = ttk.Entry(master=self, textvariable=self.var_nome)

        label_rg = ttk.Label(master=self, text='RG')
        entry_rg = ttk.Entry(master=self, textvariable=self.var_rg)
        
        label_cpf = ttk.Label(master=self, text='CPF')
        entry_cpf = ttk.Entry(master=self, textvariable=self.var_cpf)

        label_endereco = ttk.Label(master=self, text='ENDER.')
        entry_endereco = ttk.Entry(master=self, textvariable=self.var_endereco)

        label_cidade = ttk.Label(master=self, text='CIDADE')
        entry_cidade = ttk.Entry(master=self, textvariable=self.var_cidade)

        label_estado = ttk.Label(master=self, text='ESTADO')
        entry_estado = ttk.Entry(master=self, textvariable=self.var_estado)

        label_pais = ttk.Label(master=self, text='PAIS')
        entry_pais = ttk.Entry(master=self, textvariable=self.var_pais)

        label_cep = ttk.Label(master=self, text='CEP')
        entry_cep = ttk.Entry(master=self, textvariable=self.var_cep)

        label_nasc = ttk.Label(master=self, text='NASC')
        entry_nasc = ttk.Entry(master=self, textvariable=self.var_nasc)

        label_sexo = ttk.Label(master=self, text='SEXO')
        entry_sexo = ttk.Entry(master=self, textvariable=self.var_sexo)

        label_celular = ttk.Label(master=self, text='CELULAR')
        entry_celular = ttk.Entry(master=self, textvariable=self.var_celular)

        label_email = ttk.Label(master=self, text='E-MAIL')
        entry_email = ttk.Entry(master=self, textvariable=self.var_email)

        label_empresa = ttk.Label(master=self, text='EMPRESA')
        entry_empresa = ttk.Entry(master=self, textvariable=self.var_empresa)
        
        label_cargo = ttk.Label(master=self, text='CARGO')
        entry_cargo = ttk.Entry(master=self, textvariable=self.var_cargo)

        label_escolaridade = ttk.Label(master=self, text='ESCOL.')
        entry_escolaridade = ttk.Entry(master=self, textvariable=self.var_escolaridade)

        label_profis = ttk.Label(master=self, text='PROF.')
        entry_profis = ttk.Entry(master=self, textvariable=self.var_profis)

        label_defic = ttk.Label(master=self, text='DEFIC.')
        entry_defic = ttk.Entry(master=self, textvariable=self.var_defic)

        btn_cadastrar = ttk.Button(master=self, text='Cadastrar', command=self.add_to_database)
        btn_limpar_formulario = ttk.Button(master=self, text='Limpar', command=self.clear_form, bootstyle='warning')
        btn_remover_clientes = ttk.Button(master=self, text='Deletar', command=lambda: print('Deletando Cliente...'), bootstyle='danger')
        btn_editar_clientes = ttk.Button(master=self, text='Editar Dados', command=lambda: print('Editando Dados'))

        # validation
        add_text_validation(entry_nome, when='focusout')
        add_text_validation(entry_rg, when='focusout')
        add_regex_validation(entry_cpf, pattern='^[0-9]{11}$', when='focusout')

        # place
        label_nome.grid(row=0, column=0, sticky='nswe')
        entry_nome.grid(row=0, column=1, columnspan=6, sticky='nswe', padx=5, pady=5)

        label_rg.grid(row=0, column=7, sticky='nswe')
        entry_rg.grid(row=0, column=8, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_cpf.grid(row=1, column=0, sticky='nswe')
        entry_cpf.grid(row=1, column=1, columnspan=2, sticky='nswe', padx=5, pady=5)
        
        label_endereco.grid(row=1, column=3, sticky='nswe')
        entry_endereco.grid(row=1, column=4, columnspan=6, sticky='nswe', padx=5, pady=5)

        label_cidade.grid(row=2, column=0, sticky='nswe')
        entry_cidade.grid(row=2, column=1, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_estado.grid(row=2, column=3, sticky='nswe')
        entry_estado.grid(row=2, column=4, columnspan=1, sticky='nswe', padx=5, pady=5)

        label_pais.grid(row=2, column=5, sticky='nswe')
        entry_pais.grid(row=2, column=6, columnspan=1, sticky='nswe', padx=5, pady=5)

        label_cep.grid(row=2, column=7, sticky='nswe')
        entry_cep.grid(row=2, column=8, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_nasc.grid(row=3, column=0, sticky='nswe')
        entry_nasc.grid(row=3, column=1, columnspan=1, sticky='nswe', padx=5, pady=5)

        label_sexo.grid(row=3, column=2, sticky='nswe')
        entry_sexo.grid(row=3, column=3, columnspan=1, sticky='nswe', padx=5, pady=5)
        
        label_celular.grid(row=3, column=4, sticky='nswe')
        entry_celular.grid(row=3, column=5, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_email.grid(row=3, column=7, sticky='nswe')
        entry_email.grid(row=3, column=8, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_empresa.grid(row=4, column=0, sticky='nswe')
        entry_empresa.grid(row=4, column=1, columnspan=3, sticky='nswe', padx=5, pady=5)
        
        label_cargo.grid(row=4, column=4, sticky='nswe')
        entry_cargo.grid(row=4, column=5, columnspan=2, sticky='nswe', padx=5, pady=5)
        
        label_escolaridade.grid(row=4, column=7, sticky='nswe')
        entry_escolaridade.grid(row=4, column=8, columnspan=2, sticky='nswe', padx=5, pady=5)
        
        label_profis.grid(row=5, column=0, sticky='nswe')
        entry_profis.grid(row=5, column=1, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_defic.grid(row=5, column=3, sticky='nswe')
        entry_defic.grid(row=5, column=4, columnspan=3, sticky='nswe', padx=5, pady=5)

        btn_remover_clientes.grid(row=7, column=0, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_limpar_formulario.grid(row=7, column=2, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_editar_clientes.grid(row=7, column=6, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_cadastrar.grid(row=7, column=8, columnspan=2, sticky='nswe', padx=5, pady=5)
        

    def add_to_database(self):
        columns, data = self.get_form_data()
        cursor = self.con.cursor()
        cursor.execute(f"INSERT INTO {self.table_name} {columns} VALUES {data}")
        self.con.commit()

        if self.pandas_table and isinstance(self.pandas_table, PandasTableView):
            values = [var.get() for var in self.vars]
            self.pandas_table.insert_row(index='end', values=values)
            self.pandas_table.load_table_data(clear_filters=True)
            self.clear_form()


    def get_form_data(self):
        data = "("
        columns = "("
        
        cursor = self.con.cursor()
        description = cursor.execute(f"SELECT * FROM {self.table_name}").description
        table_columns = list(map(lambda x: x[0], description))
        for var, desc in zip(self.vars, table_columns):
            data += f"'{var.get()}',"
            columns += f"{desc},"
        data = data[:-1] + ')'
        columns = columns[:-1] + ')'
        return columns, data
        
    
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



