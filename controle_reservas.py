from MyWidgets import Integrated_Register_Form, Integrated_Table_View
import pandas as pd
from win32com import client
import ttkbootstrap as ttk
from ttkbootstrap.toast import ToastNotification
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
        self.reservation_form = Reservation_Form(master=self, con=self.con, table_name='reservas', integrated_table=table, text='Reservation Form')
        self.reservation_form.grid(row=0, column=1, rowspan=2, sticky='nswe')


class Reservation_Form(Integrated_Register_Form):
    def __init__(self, master, con: sqlite3.Connection, table_name: str, integrated_table: str, text='Table'):
        super().__init__(
            master=master,
            con=con,
            table_name=table_name,
            integrated_table=integrated_table,
            text=text
        )

        # layout
        self.rowconfigure(index=0, weight=2, uniform='a')
        self.rowconfigure(index=1, weight=5, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')

        top_frame = ttk.Labelframe(master=self, text='Dados Reserva')
        down_frame = ttk.LabelFrame(master=self, text='Dados Acompanhantes')

        top_frame.rowconfigure(index=(0,1,2,3), weight=1, uniform='a')
        top_frame.columnconfigure(index=(0,1,2,3,4,5,6,7,8,9), weight=1, uniform='a')

        down_frame.rowconfigure(index=(0,1,2,3,4,5,6,7,8,9), weight=1, uniform='a')
        down_frame.columnconfigure(index=(0,1,2,3,4,5,6,7,8,9), weight=1, uniform='a')

        top_frame.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)
        down_frame.grid(row=1, column=0, sticky='nswe', padx=5, pady=5)

        # VARIABLES
        var_nome = ttk.StringVar(value='')
        var_cpf = ttk.StringVar(value='')
        var_nasc = ttk.StringVar(value='')
        var_celular = ttk.StringVar(value='')
        var_email = ttk.StringVar(value='')
        var_empresa = ttk.StringVar(value='')
        var_dtinicio = ttk.StringVar(value='')
        var_dtfinal = ttk.StringVar(value='')
        var_diareserva = ttk.StringVar(value='')
        var_qthospede = ttk.StringVar(value='')
        var_numapto = ttk.StringVar(value='')
        var_nomeacp1 = ttk.StringVar(value='')
        var_rgacp1 = ttk.StringVar(value='')
        var_nomeacp2 = ttk.StringVar(value='')
        var_rgacp2 = ttk.StringVar(value='')
        var_nomeacp3 = ttk.StringVar(value='')
        var_rgacp3 = ttk.StringVar(value='')
        var_nomeacp4 = ttk.StringVar(value='')
        var_rgacp4 = ttk.StringVar(value='')

        self.declare_variables([
            var_nome,
            var_cpf,
            var_nasc,
            var_celular,
            var_email,
            var_empresa,
            var_dtinicio,
            var_dtfinal,
            var_diareserva,
            var_qthospede,
            var_numapto,
            var_nomeacp1,
            var_rgacp1,
            var_nomeacp2,
            var_rgacp2,
            var_nomeacp3,
            var_rgacp3,
            var_nomeacp4,
            var_rgacp4,
        ])

        # WIDGETS
        
        # create widgets

        label_nome = ttk.Label(master=top_frame, text='NOME')
        entry_nome = ttk.Entry(master=top_frame, textvariable=var_nome)

        label_cpf = ttk.Label(master=top_frame, text='CPF')
        entry_cpf = ttk.Entry(master=top_frame, textvariable=var_cpf)

        label_nasc = ttk.Label(master=top_frame, text='NASC')
        entry_nasc = ttk.Entry(master=top_frame, textvariable=var_nasc)

        label_celular = ttk.Label(master=top_frame, text='CELULAR')
        entry_celular = ttk.Entry(master=top_frame, textvariable=var_celular)

        label_email = ttk.Label(master=top_frame, text='E-MAIL')
        entry_email = ttk.Entry(master=top_frame, textvariable=var_email)

        label_empresa = ttk.Label(master=top_frame, text='EMPRESA')
        entry_empresa = ttk.Entry(master=top_frame, textvariable=var_empresa)

        label_dtinicio = ttk.Label(master=top_frame, text="DtINÍCIO")
        entry_dtinicio = ttk.Entry(master=top_frame, textvariable=var_dtinicio)

        label_dtfinal = ttk.Label(master=top_frame, text='DtFINAL')
        entry_dtfinal = ttk.Entry(master=top_frame, textvariable=var_dtfinal)

        label_diareserva = ttk.Label(master=top_frame, text='DIA RESERVA')
        entry_diareserva = ttk.Entry(master=top_frame, textvariable=var_diareserva)

        label_qthospede = ttk.Label(master=top_frame, text='Qtd. Hospedes')
        entry_qthospede = ttk.Entry(master=top_frame, textvariable=var_qthospede)

        label_numapto = ttk.Label(master=top_frame, text='NUM. APTO')
        entry_numapto = ttk.Entry(master=top_frame, textvariable=var_numapto)

        label_nomeacp1 = ttk.Label(master=down_frame, text='NOME ACP-1')
        entry_nomeacp1 = ttk.Entry(master=down_frame, textvariable=var_nomeacp1)

        label_rgacp1 = ttk.Label(master=down_frame, text='RG')
        entry_rgacp1 = ttk.Entry(master=down_frame, textvariable=var_rgacp1)

        label_nomeacp2 = ttk.Label(master=down_frame, text='NOME ACP-2')
        entry_nomeacp2 = ttk.Entry(master=down_frame, textvariable=var_nomeacp2)

        label_rgacp2 = ttk.Label(master=down_frame, text='RG')
        entry_rgacp2 = ttk.Entry(master=down_frame, textvariable=var_rgacp2)

        label_nomeacp3 = ttk.Label(master=down_frame, text='NOME ACP-3')
        entry_nomeacp3 = ttk.Entry(master=down_frame, textvariable=var_nomeacp3)

        label_rgacp3 = ttk.Label(master=down_frame, text='RG')
        entry_rgacp3 = ttk.Entry(master=down_frame, textvariable=var_rgacp3)

        label_nomeacp4 = ttk.Label(master=down_frame, text='NOME ACP-4')
        entry_nomeacp4 = ttk.Entry(master=down_frame, textvariable=var_nomeacp4)

        label_rgacp4 = ttk.Label(master=down_frame, text='RG')
        entry_rgacp4 = ttk.Entry(master=down_frame, textvariable=var_rgacp4)


        btn_register = self.register_button(master=down_frame)
        btn_edit = self.edit_button(master=down_frame)
        btn_save_edit = self.save_edit_button(master=down_frame)
        btn_clear_form = self.clear_form_button(master=down_frame)
        btn_delete = self.delete_button(master=down_frame)
        btn_add_consumption = self.consumption_button(master=down_frame)
        btn_repoort_button = self.reservation_report_button(master=down_frame)

        # validation
        self.form_validation.validate_text(widget=entry_nome, textvariable=var_nome, required=True)
        self.form_validation.validate_cpf(widget=entry_cpf, textvariable=var_cpf)
        self.form_validation.validate_date(widget=entry_nasc, textvariable=var_nasc)
        self.form_validation.validate_phone_number(widget=entry_celular, textvariable=var_celular, required=True)
        self.form_validation.validate_contains(widget=entry_email, textvariable=var_email, text='@')
        self.form_validation.validate_date(widget=entry_dtinicio, textvariable=var_dtinicio, required=True)
        self.form_validation.validate_date(widget=entry_dtfinal, textvariable=var_dtfinal, required=True)
        self.form_validation.validate_date(widget=entry_diareserva, textvariable=var_diareserva, required=True)
        self.form_validation.validate_numeric(widget=entry_qthospede, textvariable=var_qthospede, required=True)
        self.form_validation.validate_numeric(widget=entry_numapto, textvariable=var_numapto, required=True)
        self.form_validation.validate_numeric(widget=entry_rgacp1, textvariable=var_rgacp1)
        self.form_validation.validate_numeric(widget=entry_rgacp2, textvariable=var_rgacp2)
        self.form_validation.validate_numeric(widget=entry_rgacp3, textvariable=var_rgacp3)
        self.form_validation.validate_text(widget=entry_nomeacp1, textvariable=var_nomeacp1)
        self.form_validation.validate_text(widget=entry_nomeacp2, textvariable=var_nomeacp2)
        self.form_validation.validate_text(widget=entry_nomeacp3, textvariable=var_nomeacp3)

        # place
        label_nome.grid(row=0, column=0, sticky='nswe')
        entry_nome.grid(row=0, column=1, columnspan=6, sticky='nswe', padx=5, pady=5)

        label_cpf.grid(row=0, column=7, sticky='nswe')
        entry_cpf.grid(row=0, column=8, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_nasc.grid(row=1, column=0, sticky='nswe')
        entry_nasc.grid(row=1, column=1, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_celular.grid(row=1, column=3, sticky='nswe')
        entry_celular.grid(row=1, column=4, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_email.grid(row=1, column=6, sticky='nswe')
        entry_email.grid(row=1, column=7, columnspan=3, sticky='nswe', padx=5, pady=5)

        label_empresa.grid(row=2, column=0, sticky='nswe')
        entry_empresa.grid(row=2, column=1, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_dtinicio.grid(row=2, column=3, sticky='nswe')
        entry_dtinicio.grid(row=2, column=4, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_dtfinal.grid(row=2, column=6, sticky='nswe')
        entry_dtfinal.grid(row=2, column=7, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_diareserva.grid(row=3, column=0, sticky='nswe')
        entry_diareserva.grid(row=3, column=1, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_qthospede.grid(row=3, column=3, sticky='nswe')
        entry_qthospede.grid(row=3, column=4, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_numapto.grid(row=3, column=6, sticky='nswe')
        entry_numapto.grid(row=3, column=7, columnspan=2, sticky='nswe', padx=5, pady=5)

        label_nomeacp1.grid(row=0, column=0, columnspan=2, sticky='nswe')
        entry_nomeacp1.grid(row=0, column=2, columnspan=4, sticky='nswe', padx=5, pady=5)

        label_rgacp1.grid(row=0, column=6, columnspan=2, sticky='nswe')
        entry_rgacp1.grid(row=0, column=7, columnspan=3, sticky='nswe', padx=5, pady=5)

        label_nomeacp2.grid(row=1, column=0, columnspan=2, sticky='nswe')
        entry_nomeacp2.grid(row=1, column=2, columnspan=4, sticky='nswe', padx=5, pady=5)

        label_rgacp2.grid(row=1, column=6, columnspan=2, sticky='nswe')
        entry_rgacp2.grid(row=1, column=7, columnspan=3, sticky='nswe', padx=5, pady=5)

        label_nomeacp3.grid(row=2, column=0, columnspan=2, sticky='nswe')
        entry_nomeacp3.grid(row=2, column=2, columnspan=4, sticky='nswe', padx=5, pady=5)

        label_rgacp3.grid(row=2, column=6, columnspan=2, sticky='nswe')
        entry_rgacp3.grid(row=2, column=7, columnspan=3, sticky='nswe', padx=5, pady=5)

        label_nomeacp4.grid(row=3, column=0, columnspan=2, sticky='nswe')
        entry_nomeacp4.grid(row=3, column=2, columnspan=4, sticky='nswe', padx=5, pady=5)

        label_rgacp4.grid(row=3, column=6, columnspan=2, sticky='nswe')
        entry_rgacp4.grid(row=3, column=7, columnspan=3, sticky='nswe', padx=5, pady=5)


        btn_register.grid(row=9, column=8, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_edit.grid(row=9, column=6, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_add_consumption.grid(row=9, column=4, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_save_edit.grid(row=8, column=6, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_clear_form.grid(row=9, column=0, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_delete.grid(row=8, column=0, columnspan=2, sticky='nswe', padx=5, pady=5)
        btn_repoort_button.grid(row=8, column=2, columnspan=2, sticky='nswe', padx=5, pady=5)
        
    def consumption_button(self, master):
        def add_consumption():
            Consumpiton_PopUp_Window(con=self.con)
        
        btn = ttk.Button(master=master, text='Add Consumption', command=add_consumption, bootstyle='warning')
        return btn
    
    def reservation_report_button(self, master, con: sqlite3.Connection=None):
        def make_report():
            # getting data
            rows = self.integrated_table.get_rows(selected=True)
            if len(rows) > 1:
                toast = ToastNotification(title="Error", message="Please select one row at a time", bootstyle='danger', duration=3000, icon='', position=(0,0,'nw'))
                toast.show_toast()
                return
            
            row_data = rows[0].values

            # load workbook
            excel = client.Dispatch("Excel.Application")
            book = excel.Workbooks.Open('./Reports/ReservationModel.xlsx')
            sheet = book.Worksheets[0]
            

            # cells
            cells = [
                sheet.Range('D4'),
                sheet.Range('D7'),
                sheet.Range('D8'),
                sheet.Range('D9'),
                sheet.Range('D10'),
                sheet.Range('D11'),
                sheet.Range('D12'),
                sheet.Range('K7'),
                sheet.Range('K8'),
                sheet.Range('K9'),
                sheet.Range('K10'),
                sheet.Range('K11'),
                sheet.Range('D14'),
                sheet.Range('K14'),
                sheet.Range('D15'),
                sheet.Range('K15'),
                sheet.Range('D16'),
                sheet.Range('K16'),
                sheet.Range('D17'),
                sheet.Range('K17'),
                sheet.Range('D18'),
                sheet.Range('K18'),
            ]

            for c, v in zip(cells,row_data):
                c.Value = v

            # save workbook
            book

            df = pd.read_excel(io='./Reports/ReservationModel.xlsx', sheet_name='Model')
        
        btn = ttk.Button(master=master, text='Make Report', command=make_report)
        return btn

class Consumpiton_PopUp_Window(ttk.Toplevel):
    def __init__(self, con: sqlite3.Connection):
        # initial setup
        super().__init__(
            title='Add Consumption',
            iconphoto='',
            size=(500, 500),
            resizable=(False, False),
            topmost=True,
        )
        self.con = con

        # layout
        self.rowconfigure(index=0, weight=2, uniform='a')
        self.rowconfigure(index=1, weight=1, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')

        # widgets
        table = Integrated_Table_View(master=self, con=con, table_name='produtos')
        table.grid(row=0, column=0, sticky='nswe')

        frame = ttk.LabelFrame(master=self, text='Add Consumption form')
        frame.grid(row=1, column=0, sticky='nswe', padx=5, pady=5)

        # frame layout
        frame.rowconfigure(index=(0,1,2), weight=1, uniform='a')
        frame.columnconfigure(index=(0,1,2,3,4), weight=1, uniform='a')

        # widgets
        btn_add = ttk.Button(master=frame, text="Add", bootstyle='default')
        btn_add.grid(row=2, column=4, columnspan=1, sticky='nswe', padx=5, pady=5)

        btn_remove = ttk.Button(master=frame, text="Remove", bootstyle='danger')
        btn_remove.grid(row=2, column=3, columnspan=1, sticky='nswe', padx=5, pady=5)

        # run
        self.mainloop()

    
    


