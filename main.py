import customtkinter as ctk
from MyWidgets import PandasTableView, ClientForm, MenuBar
import pandas as pd
import sqlite3
import os
from random import choice, randint

class App(ctk.CTk):
    def __init__(self):
        # initial setup
        super().__init__()
        ctk.set_appearance_mode('light')
        self.title('Sistema Hotel')
        self.geometry('1280x720')

        # layout
        self.rowconfigure(index=0, weight=1, uniform='a')
        self.rowconfigure(index=(1,2), weight=8, uniform='a')
        self.columnconfigure(index=(0,1), weight=1, uniform='a')

        # WIDGETS ->

        # menu bar
        menu = MenuBar(master=self)
        file_btn = menu.add_button(master=menu, text="File", command=lambda: print("File Button"))
        settings_btn = menu.add_button(master=menu, text="Settings", command=lambda: print("Settings Button"))
        menu.grid(row=0, column=0, columnspan=2, sticky='nswe')

        # connection to database
        self.make_connection()
        # self.make_sample_data() # add 100 sample recordas to database

        # searchfield
        df = pd.read_sql("SELECT * FROM clientes", con=self.con)
        
        table = PandasTableView(master=self, rowdata=df, paginated=True)
        table.grid(row=1, column=1, rowspan=2, sticky='nswe')

        # client form
        client_form = ClientForm(master=self, con=self.con, table_name='clientes', pandas_table=table)
        client_form.grid(row=1, column=0, sticky='nswe')

        # run
        self.mainloop()

    def make_connection(self):
        data_path = './HotelDatabase/'
        filename = 'hoteldatabase'
        os.makedirs(data_path, exist_ok=True)
        self.con = sqlite3.connect(database=data_path + filename)
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS clientes
                (nome TEXT,
                rg TEXT,
                cpf TEXT,
                endereco TEXT,
                cidade TEXT,
                estado TEXT,
                pais TEXT,
                cep TEXT,
                nasc TEXT,
                sexo TEXT,
                celular TEXT,
                email TEXT,
                empresa TEXT,
                cargo TEXT,
                escolaridade TEXT,
                profis TEXT,
                defic TEXT)
            """)

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




App()
