import CTkTable
import pandas as pd
import numpy as np
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.dialogs.dialogs import Messagebox
import sqlite3
import re

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
            con: sqlite3.Connection,
            table_name: str,
            paginated=False,
            searchable=True,
            headers:list=[],
            bootstyle='litera',
        ):
        self.con = con
        self.table_name = table_name
        self.headers = headers
        self.rowdata = pd.read_sql(f"SELECT * FROM {self.table_name}", con=self.con)
        
        # Checks select columns to display on table
        if self.headers == []:
            self.headers = self.rowdata.columns.values
        self.rowdata  = self.rowdata[self.headers].to_numpy().tolist()
            

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
    
    def update_table(self):
        rowdata = pd.read_sql(f"SELECT * FROM {self.table_name}", con=self.con)
        rowdata = rowdata[self.headers].to_numpy().tolist()
        self.build_table_data(coldata=self.headers, rowdata=rowdata)
        self.autofit_columns()


class ClientForm(ttk.Labelframe):

    def __init__(self, master, con: sqlite3.Connection, table_name: str, pandas_table: PandasTableView=None):
        # initial setup
        self.con = con
        self.table_name = table_name
        self.pandas_table = pandas_table
        self.form_validation = Validate()
        self.id = ttk.StringVar(value='')
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
        self.btn_remover_clientes = ttk.Button(master=self, text='Deletar', command=self.deletar, bootstyle='danger')
        btn_editar_clientes = ttk.Button(master=self, text='Editar Dados', command=self.editar_dados, bootstyle="primary-outline")
        self.btn_savar_edicao = ttk.Button(master=self, text='Savar Edição', command=self.salvar_edicao, bootstyle='success', state='disabled')
        
        # tooltip
        ToolTip(widget=btn_cadastrar, text='Adiciona cliente ao bando de dados.', bootstyle=('dark', 'inverse'))
        ToolTip(widget=btn_editar_clientes, text='Preenche formulário com dados do cliente selecionado.', bootstyle=('dark', 'inverse'))
        ToolTip(widget=self.btn_remover_clientes, text='Deleta cliente selecionado do bando de dados.', bootstyle=('danger', 'inverse'))
        ToolTip(widget=self.btn_savar_edicao, text='Salva edição no bando de dados.', bootstyle=('success', 'inverse'))
        ToolTip(widget=btn_limpar_formulario, text='Limpa dados do formulário ou cancela edição.', bootstyle=('warning', 'inverse'))

        

        
        # validation
        
        self.form_validation.validate_text(widget=entry_nome, textvariable=self.var_nome, required=True)
        self.form_validation.validate_numeric(widget=entry_rg, textvariable=self.var_rg, required=True)
        self.form_validation.validate_cpf(widget=entry_cpf, textvariable=self.var_cpf)
        self.form_validation.validate_numeric(widget=entry_cep, textvariable=self.var_cep)
        self.form_validation.validate_date(widget=entry_nasc, textvariable=self.var_nasc)
        self.form_validation.validate_options(widget=entry_sexo, textvariable=self.var_sexo, options=['Masculino', 'Feminino'])
        self.form_validation.validate_phone_number(widget=entry_celular, textvariable=self.var_celular, required=True)
        self.form_validation.validate_contains(widget=entry_email, textvariable=self.var_email, text='@')
        self.form_validation.validate_options(widget=entry_escolaridade, textvariable=self.var_escolaridade, options=['Não tem', 'Fundamental','Médio', 'Superior'])

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

        self.btn_remover_clientes.grid(row=6, column=0, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_limpar_formulario.grid(row=7, column=0, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_editar_clientes.grid(row=7, column=6, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_cadastrar.grid(row=7, column=8, columnspan=2, sticky='nswe', padx=5, pady=5)
        self.btn_savar_edicao.grid(row=6, column=6, columnspan=2, sticky='nswe', padx=5, pady=5)
        
    def add_to_database(self):
        """
            Add form data to the database
        """
        # check if form is valid and display toast notification
        if not self.form_validation.check_validation():
            toast = ToastNotification(title="Invalid Form", message="Please fill all fields required.", bootstyle='danger', icon='', duration=3000, position=(0,0,'nw'))
            toast.show_toast()
            return

        # insert values into database
        columns, data, _ = self.get_form_data()
        cursor = self.con.cursor()
        cursor.execute(f"INSERT INTO {self.table_name} {columns} VALUES {data}")
        self.con.commit()

        # display toast notification if success
        toast = ToastNotification(title="Success", message="Client added to database.", bootstyle='success', icon='', duration=3000, position=(0,0,'nw'))
        toast.show_toast()

        # updates pandas table if there is pandas table connected
        if isinstance(self.pandas_table, PandasTableView):
            self.pandas_table.update_table()

    def get_form_data(self):
        """
            Get form filled data and table headers and returns them as formated string for SQL database insertion
        """
        data = "("
        columns = "("
        col_data = ""
        
        cursor = self.con.cursor()
        description = cursor.execute(f"SELECT * FROM {self.table_name}").description
        table_columns = list(map(lambda x: x[0], description))[1:] # discard id to be added automaticaly by sqlite3
        for var, desc in zip(self.vars, table_columns):
            data += f"'{var.get()}',"
            columns += f"{desc},"
            col_data += f"{desc}='{var.get()}', "
        data = data[:-1] + ')'
        columns = columns[:-1] + ')'
        col_data = col_data[:-2]
        
        return columns, data, col_data
        
    def clear_form(self):
        self.btn_savar_edicao.configure(state='disabled')
        self.btn_remover_clientes.configure(state='enabled')
        self.id.set('')
        for var in self.vars:
            var.set(value='')
       
    def fill_form(self):
        """
            Fills all form data with selected row of pandas table view
        """
        
        # checks if user didn't select more than one row
        rows = self.pandas_table.get_rows(selected=True)
        if len(rows) > 1:
            toast = ToastNotification(title="Error", message="Please select one row at a time", bootstyle='danger', duration=3000, icon='', position=(0,0,'nw'))
            toast.show_toast()
            return

        # fill form
        rows = rows[0].values
        for var , value, in zip(self.vars, rows[1:]): # discard id column
            var.set(value=value)
        
        # update current id
        self.id.set(rows[0])
        
    def editar_dados(self):
        # checks if pandas table is connected
        if not isinstance(self.pandas_table, PandasTableView):
            toast = ToastNotification(title="Warning", message="Please connect to a Pandas Table", bootstyle='warning', duration=3000, icon='', position=(0,0,'nw'))
            toast.show_toast()
            return

        self.fill_form()
        self.btn_savar_edicao.configure(state='enabled')
        self.btn_remover_clientes.configure(state='disabled')

    def salvar_edicao(self):
        # check if form is valid and display toast notification
        if not self.form_validation.check_validation():
            toast = ToastNotification(title="Invalid Form", message="Please fill all fields required.", bootstyle='danger', icon='', duration=3000, position=(0,0,'nw'))
            toast.show_toast()
            return
        
        # user confirmation input
        ans = Messagebox().yesno(message=f"Confirm operation: \n update data from {self.table_name} ?", title='Confirm', bootstyle='warning', parent=self)
        if not ans == 'Yes':
            toast = ToastNotification(title="Info", message="Operation Canceled.", bootstyle='info', icon='', duration=3000, position=(0,0,'nw'))
            toast.show_toast()
            return
        
        # updating data
        _, _, col_data = self.get_form_data()
        self.con.execute(f"UPDATE {self.table_name} SET {col_data} WHERE client_id = {self.id.get()}")
        self.con.commit()

        # diplay toast notification
        toast = ToastNotification(title="Success", message="Data updated with success.", bootstyle='success', icon='', duration=3000, position=(0,0,'nw'))
        toast.show_toast()

        # update display
        self.pandas_table.update_table()

        # clear form data
        self.clear_form()

    def deletar(self):
        # checks if pandas table is connected
        if not isinstance(self.pandas_table, PandasTableView):
            toast = ToastNotification(title="Warning", message="Please connect to a Pandas Table", bootstyle='warning', position=(0,0,'nw'), duration=3000, icon='')
            toast.show_toast()
            return
        
        # checks if user didn't select more than one row
        rows = self.pandas_table.get_rows(selected=True)
        if len(rows) > 1:
            toast = ToastNotification(title="Error", message="Please select one row at a time", bootstyle='danger', position=(0,0,'nw'), duration=3000, icon='')
            toast.show_toast()
            return
        
        rows = rows[0].values
        selected_id = rows[0]

        # user confirmation input
        ans = Messagebox().yesno(message=f"Confirm operation: \n Delete : {selected_id} from {self.table_name} ?", title='Confirm', bootstyle='warning', parent=self)
        if not ans == 'Yes':
            toast = ToastNotification(title="Info", message="Operation Canceled.", bootstyle='info', icon='', duration=3000, position=(0,0,'nw'))
            toast.show_toast()
            return
        
        # delete client
        self.con.execute(f"DELETE FROM {self.table_name} WHERE client_id = {selected_id}")
        self.con.commit()

        # diplay toast notification
        toast = ToastNotification(title="Success", message="Operation done with success.", bootstyle='success', icon='', duration=3000, position=(0,0,'nw'))
        toast.show_toast()

        # update display
        self.pandas_table.update_table()
    


class MenuBar(ttk.Frame):
    def __init__(self, master):
        # initial setup
        super().__init__(master=master, bootstyle="dark")
    
    def add_button(self, master, text: str, command=lambda x:x):
        btn = ttk.Button(master=master, text=text, command=command)
        btn.pack(side='left', fill='y', padx=5, pady=5)
        return btn


class Validate:
    def __init__(self):
        self.all_valid = []
        self.all_required = []

    def validate_cpf(self, widget, textvariable, required=False):
        """
            Returns True if field value is cpf formated xxxxxxxxxxx or xxx.xxx.xxx-xx
            Returns False otherwise
        """
        
        valid = ttk.BooleanVar(value=True)
        self.all_valid.append(valid)

        if required:
            valid.set(value=False)
            self.all_required.append(tuple((valid, widget)))
        
        def val(*args):
            if required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(False)
                return False
            
            if not required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True

            pattern = re.compile('^[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}-?[0-9]{2}')
            if not re.fullmatch(pattern=pattern, string=textvariable.get()) == None:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True
            widget.configure(bootstyle='danger')
            valid.set(False)
            return False
        textvariable.trace('w', val)

    def validate_cnpj(self, widget, textvariable, required=False):
        """
            Returns True if field value is cpf formated xxxxxxxxxxxxxx or xx.xxx.xxx/0001-xx
            Returns False otherwise
        """
        
        valid = ttk.BooleanVar(value=True)
        self.all_valid.append(valid)

        if required:
            valid.set(value=False)
            self.all_required.append(tuple((valid, widget)))
        
        def val(*args):
            if required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(False)
                return False
            
            if not required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True

            pattern = re.compile('^[0-9]{2}\.?[0-9]{3}\.?[0-9]{3}/?000[1-2]-?[0-9]{2}')
            if not re.fullmatch(pattern=pattern, string=textvariable.get()) == None:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True
            widget.configure(bootstyle='danger')
            valid.set(False)
            return False
        textvariable.trace('w', val)

    def validate_numeric(self, widget, textvariable, required=False):
        """
            Returns True if field value is numeric and is not empty.
            Returns False otherwise
        """
        
        valid = ttk.BooleanVar(value=True)
        self.all_valid.append(valid)

        if required:
            valid.set(value=False)
            self.all_required.append(tuple((valid, widget)))
        
        def val(*args):
            if required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(False)
                return False
            
            if not required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True
            
            try:
                float(textvariable.get())
                widget.configure(bootstyle='default')
                valid.set(True)
                return True
            except:
                widget.configure(bootstyle='danger')
                valid.set(False)
                return False
        textvariable.trace('w', val)

    def validate_text(self, widget, textvariable, required=False):
        """
            Returns True if field does not contains any numbers and is not empty.
            Returns False otherwise
        """
        valid = ttk.BooleanVar(value=True)
        self.all_valid.append(valid)

        if required:
            valid.set(value=False)
            self.all_required.append(tuple((valid, widget)))
        
        def val(*args):
            if required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(False)
                return False
            
            if not required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True
            
            pattern = re.compile('^[a-zA-Z0-9 ]+')
            if not re.fullmatch(pattern=pattern, string=textvariable.get()) == None:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True
            widget.configure(bootstyle='danger')
            valid.set(False)
            return False

        textvariable.trace('w', val)

    def validate_options(self, widget, textvariable, options: list, required=False):
        """
            Returns True if field contais one of options
        """
        valid = ttk.BooleanVar(value=True)
        self.all_valid.append(valid)

        if required:
            valid.set(value=False)
            self.all_required.append(tuple((valid, widget)))

        def val(*args, options=options):
            if required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(False)
                return False
            
            if not required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True

            options = [str(option) for option in options]
            if textvariable.get().strip() in options:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True
            widget.configure(bootstyle='danger')
            valid.set(False)
            return False
        textvariable.trace('w', val)

    def validate_phone_number(self, widget, textvariable ,required=False):
        valid = ttk.BooleanVar(value=True)
        self.all_valid.append(valid)

        if required:
            valid.set(value=False)
            self.all_required.append(tuple((valid, widget)))
        
        def val(*args):
            if required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(False)
                return False
            
            if not required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True

            pattern = re.compile("^1\d\d(\d\d)?$|^0800 ?\d{3} ?\d{4}$|^(\(0?([1-9a-zA-Z][0-9a-zA-Z])?[1-9]\d\) ?|0?([1-9a-zA-Z][0-9a-zA-Z])?[1-9]\d[ .-]?)?(9|9[ .-])?[2-9]\d{3}[ .-]?\d{4}$")
            if not re.fullmatch(pattern=pattern, string=textvariable.get()) == None:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True
            widget.configure(bootstyle='danger')
            valid.set(False)
            return False
        textvariable.trace('w', val)

    def validate_regex(self, widget, textvariable, pattern: str, required=False):
        valid = ttk.BooleanVar(value=True)
        self.all_valid.append(valid)

        if required:
            valid.set(value=False)
            self.all_required.append(tuple((valid, widget)))
        
        def val(*args, pattern=pattern):
            if required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(False)
                return False
            
            if not required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True

            pattern = re.compile(pattern=pattern)
            if not re.fullmatch(pattern=pattern, string=textvariable.get()) == None:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True
            widget.configure(bootstyle='danger')
            valid.set(False)
            return False
        textvariable.trace('w',val)

    def validate_range(self, widget, textvariable, start: float, end: float, required=False):
        """
            Returns True if field is numeric and is in the closed interval [start, end]
        """
        valid = ttk.BooleanVar(value=True)
        self.all_valid.append(valid)

        if required:
            valid.set(value=False)
            self.all_required.append(tuple((valid, widget)))

        def val(*args, start=start, end=end):
            if required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(False)
                return False
            
            if not required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True

            try:
                n = float(textvariable.get())
                if (start <= float(n)) and (float(n) <= end):
                    widget.configure(bootstyle='default')
                    valid.set(True)
                    return True
                widget.configure(bootstyle='danger')
                valid.set(False)
                return False
            except:
                widget.configure(bootstyle='danger')
                valid.set(False)
                return False
        textvariable.trace('w', val)

    def validate_contains(self, widget, textvariable, text: str, required=False):
        valid = ttk.BooleanVar(value=True)
        self.all_valid.append(valid)

        if required:
            valid.set(value=False)
            self.all_required.append(tuple((valid, widget)))
        
        def val(*args, text=text):
            if required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(False)
                return False
            
            if not required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True

            if text in textvariable.get():
                widget.configure(bootstyle='default')
                valid.set(True)
                return True
            widget.configure(bootstyle='danger')
            valid.set(False)
            return False
        textvariable.trace('w', val)

    def validate_not_contains(self, widget, textvariable, text: str, required=False):
        valid = ttk.BooleanVar(value=True)
        self.all_valid.append(valid)

        if required:
            valid.set(value=False)
            self.all_required.append(tuple((valid, widget)))
        
        def val(*args, text):
            if required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(False)
                return False
            
            if not required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True

            if text not in textvariable.get():
                widget.configure(bootstyle='default')
                valid.set(True)
                return True
            widget.configure(bootstyle='danger')
            valid.set(False)
            return False
        textvariable.trace('w', val)

    def validate_date(self, widget, textvariable, required=False):
        """
            Returns True if field value is date formated as xx/xx/xxxx or xx/xx/xx
            Returns False otherwise
        """
        
        valid = ttk.BooleanVar(value=True)
        self.all_valid.append(valid)

        if required:
            valid.set(value=False)
            self.all_required.append(tuple((valid, widget)))
        
        def val(*args):
            if required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(False)
                return False
            
            if not required and len(textvariable.get()) == 0:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True

            pattern1 = re.compile('^[0-9]{2}/[0-9]{2}/[0-9]{2}')
            pattern2 = re.compile('^[0-9]{2}/[0-9]{2}/[0-9]{4}')
            one = not re.fullmatch(pattern=pattern1, string=textvariable.get()) == None
            two = not re.fullmatch(pattern=pattern2, string=textvariable.get()) == None
            if one or two:
                widget.configure(bootstyle='default')
                valid.set(True)
                return True
            widget.configure(bootstyle='danger')
            valid.set(False)
            return False
        textvariable.trace('w', val)

    def check_validation(self):
        """
            Return True if all fields are validated else return False
        """
        if len(self.all_valid) == 0:
            return True
        
        all_filled = True
        for val, widget in self.all_required:
            text = str(widget.get())
            if len(text) == 0:
                all_filled = False
                widget.configure(bootstyle='warning')
                val.set(False)
        if not all_filled:
            return False
        
        for val in self.all_valid:
            if val.get() == False:
                return False
        return True
        
