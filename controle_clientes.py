import sqlite3
from MyWidgets import Integrated_Form, Integrated_Table_View
from random import choice, randint
from ttkbootstrap.toast import ToastNotification
import ttkbootstrap as ttk


class Controle_Clientes(ttk.Frame):

    def __init__(self, master, con: sqlite3.Connection, table_name: str):
        # initial setup
        super().__init__(master=master)
        self.con = con
        self.table_name = table_name

        # layout
        self.rowconfigure(index=(0,1), weight=1, uniform='a')
        self.columnconfigure(index=(0,1), weight=1, uniform='a')

        self.make_sample_data() # add 100 sample records to database

        # integrated table
        table = Integrated_Table_View(master=self, con=self.con, table_name='clientes', paginated=True)
        table.grid(row=0, column=1, rowspan=2, sticky='nswe')

        # client form
        self.client_form = Client_Form(master=self, con=self.con, table_name=self.table_name, integrate_table=table, text='Client Form')
        self.client_form.grid(row=0, column=0, sticky='nswe')

    def make_sample_data(self):

        nomes = ['Fabio', 'Carlos', 'Ana', 'Felipe', 'Justilho', 'Caxias', 'Jacinto', 'Luan', 'Sergio', 'Luis', 'Janaina', 'Kleber']
        sobrenomes = ['Matos', 'Silva', 'Silveira', 'Rocha', 'Prado', 'Camargo', 'Justo', 'Hortêncio', 'das Dores', 'Pinto']
        deficiencias = ['', 'Cadeirante', 'Paraplegico', 'Mental']
        escolaridades = ['Não Tem', 'Fundamental', 'Médio', 'Superior', 'Mestrado', 'Ph.D']
        enderecos = ['R. Duque de Caxias, 6471', 'R. Campos Sales, 335', 'R. Condessa do pinhal, 6491', 'Cond. Nova Canaã. R. filadéfia, 345']
        cargos = ['Não Tem', 'Chefe', 'Secretário', 'Gerente', 'Diretor']
        profissoes = ['Médico', 'Advogado', 'Piloto', 'Pedreiro', 'Padre', 'Servidor Público', 'Soldado']
        paises = ['Brasil', 'Argentina', 'Uruguay', 'Paraguay', 'Chile', 'Venezuela', 'Inglaterra', 'Alemanha', 'Madagascar', 'Argélia', 'Marrocos', 'Nova Zelândia']
        cidades = ['Porto Velho', 'Manaus', 'Boa Vista', 'Rio Branco', 'Porto Alegre', 'Belo Horizonte', 'Brasília']
        estados = ['Rondônia', 'Roraima', 'Amazonas', 'Acre', 'Amapá', 'Tocantins', 'Maranhão', 'Ceará', 'Rio Grande do Norte']
        sexos = ['M', 'F', 'Não Declarado']
        empresas = ['Odebrecht', 'Utaú', 'Banco do Brasil', 'Gazin', 'Casas Bahia', 'Americanas', 'Nike', 'Adidas']

        for _ in range(100):
            nome = choice(nomes) + " " + choice(sobrenomes)
            rg = randint(1000000, 9999999)
            cpf = randint(10000000000, 99999999999)
            endereco = choice(enderecos)
            cidade = choice(cidades)
            estado = choice(estados)
            pais = choice(paises)
            cep = randint(10000000, 99999999)
            nasc = str(randint(1, 31)) + '/' + str(randint(1, 12)) + '/' + str(randint(1950, 2023))
            sexo = choice(sexos)
            celular = f"({randint(10, 99)}) 9{randint(10000000, 99999999)}"
            email = f"{nome}@gmail.com"
            empresa = choice(empresas)
            cargo = choice(cargos)
            escolaridade = choice(escolaridades)
            profis = choice(profissoes)
            defic = choice(deficiencias)
            
            values = f"('{nome}', '{rg}', '{cpf}', '{endereco}', '{cidade}', '{estado}', '{pais}', '{cep}', '{nasc}', '{sexo}', '{celular}', '{email}', '{empresa}', '{cargo}', '{escolaridade}', '{profis}', '{defic}')"
            self.con.execute(f"INSERT INTO clientes (nome, rg, cpf, endereco, cidade, estado, pais, cep, nasc, sexo, celular, email, empresa, cargo, escolaridade, profis, defic) VALUES {values}")
            self.con.commit()


class Client_Form(Integrated_Form):

    def __init__(self, master, con: sqlite3.Connection, table_name: str, integrate_table: Integrated_Table_View, text='Table'):
        super().__init__(
            master=master,
            con=con,
            table_name=table_name,
            integrated_table=integrate_table,
            text=text
        )

        # layout
        self.rowconfigure(index=(0,1,2,3,4,5,6,7), weight=1, uniform='a')
        self.columnconfigure(index=(0,1,2,3,4,5,6,7,8,9), weight=1, uniform='a')
        
        # VARIABLES
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

        # WIDGETS

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

        btn_register = self.register_button(master=self)
        btn_edit = self.edit_button(master=self)
        btn_save_edit =  self.save_edit_button(master=self)
        btn_clear_form = self.clear_form_button(master=self)
        btn_delete = self.delete_button(master=self)
        btn_reservation = self.btn_reservation(master=self)
        
        # validation
        self.form_validation.validate_text(widget=entry_nome, textvariable=self.var_nome, required=True)
        self.form_validation.validate_numeric(widget=entry_rg, textvariable=self.var_rg)
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

        btn_register.grid(row=7, column=8, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_edit.grid(row=7, column=6, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_save_edit.grid(row=6, column=6, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_clear_form.grid(row=7, column=0, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_delete.grid(row=6, column=0, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_reservation.grid(row=7, column=4, columnspan=2, sticky='nswe', padx=5, pady=5)
    
    def btn_reservation(self, master):

        def func():
            # checks if user didn't select more than one row
            rows = self.integrated_table.get_rows(selected=True)
            if len(rows) > 1:
                toast = ToastNotification(title="Error", message="Please select one row at a time", bootstyle='danger', duration=3000, icon='', position=(0,0,'nw'))
                toast.show_toast()
                return
            
            # getting data
            row_data = rows[0].values
            # set values to reservation 
            self.linked_form[0].set(row_data[1]) # set nome
            self.linked_form[1].set(row_data[3]) # set cpf
            self.linked_form[2].set(row_data[9]) # set nasc
            self.linked_form[3].set(row_data[11]) # set celular
            self.linked_form[4].set(row_data[12]) # set email
            self.linked_form[5].set(row_data[13]) # set empresa

            toast = ToastNotification(title="Info", message="Data copyed to reservation panel.", bootstyle='Info', duration=3000, icon='', position=(0,0,'nw'))
            toast.show_toast()

        btn = ttk.Button(master=master, text='Reservation', bootstyle='warning', command=func)
        return btn

