from MyWidgets import Integrated_Register_Form, Integrated_Table_View, Validate
import os
import xlwings as xw
import ttkbootstrap as ttk
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.dialogs import Messagebox
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
        btn_repoort_button.grid(row=9, column=2, columnspan=2, sticky='nswe', padx=5, pady=5)
        
    def consumption_button(self, master):
        def add_consumption():
            row_data = self.integrated_table.get_rows(selected=True)

            if len(row_data) > 1:
                toast = ToastNotification(title="Error", message="Multiple Rows Selected", bootstyle='danger', icon='', duration=3000, position=(0,0,'nw'))
                toast.show_toast()
                return
            
            numapto = row_data[0].values
            numapto = numapto[11]
            
            Consumpiton_PopUp_Window(con=self.con, numapto=numapto, linked_tables=[self.linked_table, ])
        
        btn = ttk.Button(master=master, text='Add Consumption', command=add_consumption, bootstyle='warning')
        return btn
    
    def reservation_report_button(self, master):
        def make_report():
            # getting data
            rows = self.integrated_table.get_rows(selected=True)
            if len(rows) > 1:
                toast = ToastNotification(title="Error", message="Please select one row at a time", bootstyle='danger', duration=3000, icon='', position=(0,0,'nw'))
                toast.show_toast()
                return
            
            row_data = rows[0].values

            # load workbook make report
            with xw.App(visible=False) as app:
                wb = xw.Book(fullname=f'./ReportModels/ReservationModel.xlsx')
                ws = wb.sheets('Model')
                # cells
                cells = [
                    ws['C3'],
                    ws['C7'],
                    ws['C8'],
                    ws['C9'],
                    ws['C10'],
                    ws['C11'],
                    ws['C12'],
                    ws['F7'],
                    ws['F8'],
                    ws['F9'],
                    ws['F10'],
                    ws['F11'],
                    ws['I7'],
                    ws['K7'],
                    ws['I8'],
                    ws['K8'],
                    ws['I9'],
                    ws['K9'],
                    ws['I10'],
                    ws['K10'],
                    ws['I11'],
                    ws['K11'],
                ]

                for c, v in zip(cells,row_data):
                    c.value = v
                ws['F3'].value = row_data[1]

                # save workbook in folder
                save_folder = 'ReservationReports'
                os.makedirs(name=save_folder, exist_ok=True)
                wb.to_pdf(path=f"./{save_folder}/{row_data[1]}-{row_data[0]}.pdf")
        
        btn = ttk.Button(master=master, text='Make Report', command=make_report)
        return btn

class Consumpiton_PopUp_Window(ttk.Toplevel):
    def __init__(self, con: sqlite3.Connection, numapto, linked_tables):
        # initial setup
        super().__init__(
            title=f'Add Consumption to Room {numapto}',
            iconphoto='',
            size=(500, 500),
            resizable=(False, False),
            topmost=True,
        )
        self.con = con
        self.numapto = numapto
        self.linked_tables = linked_tables
        self.var_quantity = ttk.StringVar(value='0')
        self.form_validation = Validate()

        # layout
        self.rowconfigure(index=0, weight=2, uniform='a')
        self.rowconfigure(index=1, weight=1, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')

        # widgets
        self.table = Integrated_Table_View(master=self, con=con, table_name='produtos')
        self.table.grid(row=0, column=0, sticky='nswe')

        frame = ttk.LabelFrame(master=self, text='Add Consumption form')
        frame.grid(row=1, column=0, sticky='nswe', padx=5, pady=5)

        # frame layout
        frame.rowconfigure(index=(0,1,2), weight=1, uniform='a')
        frame.columnconfigure(index=(0,1,2,3,4), weight=1, uniform='a')

        # widgets
        label_quantity = ttk.Label(master=frame, text='QUNAT.')
        label_quantity.grid(row=0, column=0, sticky='nswe')
        
        entry_quantity = ttk.Entry(master=frame, textvariable=self.var_quantity)
        entry_quantity.grid(row=0, column=1, sticky='nswe', padx=5, pady=5)

        btn_add = ttk.Button(master=frame, text="Add", bootstyle='default', command=self.register_multiple)
        btn_add.grid(row=2, column=4, columnspan=1, sticky='nswe', padx=5, pady=5)

        btn_cancel = ttk.Button(master=frame, text="Cancel", bootstyle='danger')
        btn_cancel.grid(row=2, column=3, columnspan=1, sticky='nswe', padx=5, pady=5)

        # validation
        self.form_validation.validate_numeric(widget=entry_quantity, textvariable=self.var_quantity, required=True)

        # run
        self.mainloop()
    
    def register_multiple(self):
        """
            Add form data to the database in multiple times
        """
        # check if form is valid and display toast notification
        if not self.form_validation.check_validation():
            toast = ToastNotification(title="Invalid Form", message="Please fill all fields required.", bootstyle='danger', icon='', duration=3000, position=(0,0,'nw'))
            toast.show_toast()
            return
        
        # check produtos
        if not self.product_is_avaliable():
            toast = ToastNotification(title="Error", message="Multiple Rows Selected or Quantity Not Enought.", bootstyle='danger', icon='', duration=3000, position=(0,0,'nw'))
            toast.show_toast()
            return
        
        # user confirmation input
        ans = Messagebox().yesno(message=f"Confirm operation: \n insert data into consumos ?", title='Confirm', bootstyle='warning', parent=self)
        if not ans == 'Yes':
            toast = ToastNotification(title="Info", message="Operation Canceled.", bootstyle='info', icon='', duration=3000, position=(0,0,'nw'))
            toast.show_toast()
            return
        
        # get product id
        row_data = self.table.get_rows(selected=True)[0].values

        # insert values into database
        columns = "(numapto, produto, prod_id)"
        data = f"('{self.numapto}', '{row_data[1]}', '{row_data[0]}')"
        q = int(self.var_quantity.get())
        values = data
        if q > 0:
            for _ in range(q - 1):
                values += ', ' + data
            
            cursor = self.con.cursor()
            print(f"INSERT INTO consumos {columns} VALUES {values}")
            cursor.execute(f"INSERT INTO consumos {columns} VALUES {values}")
            self.con.commit()
        
        # update quantity data in produtos
        quantity = int(list(self.con.execute(f"SELECT quantidade FROM produtos WHERE rowid = {row_data[0]}"))[0][0])
        self.con.execute(f"UPDATE produtos SET quantidade = {quantity - q} WHERE rowid = {row_data[0]}")

        # display toast notification if success
        toast = ToastNotification(title="Success", message="Data added to database.", bootstyle='success', icon='', duration=3000, position=(0,0,'nw'))
        toast.show_toast()

        # updates table if there is table connected
        if isinstance(self.table, Integrated_Table_View):
            self.table.update_table()
        
        for table in self.linked_tables:
            table.update_table()

    def product_is_avaliable(self):
        """
            Checks if product is avalible to be consumed
        """
        row_data = self.table.get_rows(selected=True)
        if len(row_data) > 1:
                return False
            
        row_data = row_data[0].values    
        
        q = int(row_data[4])
        if int(self.var_quantity.get()) > q:
            return False
        
        return True

    
    


