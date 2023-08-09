import pandas as pd
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.dialogs.dialogs import Messagebox
import sqlite3
import re

# WIDGETS

class Integrated_Table_View(Tableview):

    def __init__(self,
            master,
            con: sqlite3.Connection,
            table_name: str,
            paginated=False,
            searchable=True,
            headers:list=[],
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
            pagesize=100,
            stripecolor=(None, None)
        )
        self.autofit_columns()
    
    def update_table(self):
        rowdata = pd.read_sql(f"SELECT * FROM {self.table_name}", con=self.con)
        rowdata = rowdata[self.headers].to_numpy().tolist()
        self.build_table_data(coldata=self.headers, rowdata=rowdata)
        self.autofit_columns()


class Integrated_Form(ttk.Labelframe):

    def __init__(self, master, con: sqlite3.Connection, table_name: str, integrated_table: Integrated_Table_View=None, text='Table'):
        # initial setup
        self.con = con
        self.table_name = table_name
        self.integrated_table = integrated_table
        self.form_validation = Validate()
        self.id = ttk.StringVar(value='')
        self.vars = []
        self.linked_form = []
        super().__init__(master=master, text=text)
  
    def add_to_database(self):
        """
            Add form data to the database
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

        # insert values into database
        columns, data, _ = self.get_form_data()
        cursor = self.con.cursor()
        cursor.execute(f"INSERT INTO {self.table_name} {columns} VALUES {data}")
        self.con.commit()

        # display toast notification if success
        toast = ToastNotification(title="Success", message="Client added to database.", bootstyle='success', icon='', duration=3000, position=(0,0,'nw'))
        toast.show_toast()

        # updates pandas table if there is pandas table connected
        if isinstance(self.integrated_table, Integrated_Table_View):
            self.integrated_table.update_table()
        
        # clear form
        self.clear_form()

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
        for i in range(len(table_columns)):
            # Try access data
            try:
                data += f"'{self.vars[i].get()}',"
                col_data += f"{table_columns[i]}='{self.vars[i].get()}', "
            except:
                data += "' ',"
            
            columns += f"{table_columns[i]},"
        data = data[:-1] + ')'
        columns = columns[:-1] + ')'
        col_data = col_data[:-2]
        
        return columns, data, col_data
        
    def clear_form(self):
        # enable disable
        self.btn_save_edit.configure(state='disabled')
        self.btn_delete.configure(state='enabled')
        
        self.id.set('')
        for var in self.vars:
            var.set(value='')
       
    def fill_form(self):
        """
            Fills all form data with selected row of pandas table view
        """
        
        # checks if user didn't select more than one row
        rows = self.integrated_table.get_rows(selected=True)
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
        
    def edit_data(self):
        # checks if pandas table is connected
        if not isinstance(self.integrated_table, Integrated_Table_View):
            toast = ToastNotification(title="Warning", message="Please connect to a Pandas Table", bootstyle='warning', duration=3000, icon='', position=(0,0,'nw'))
            toast.show_toast()
            return

        self.fill_form()

        # anable disable
        self.btn_save_edit.configure(state='enabled')
        self.btn_delete.configure(state='disabled')

    def save_edit(self):
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
        self.con.execute(f"UPDATE {self.table_name} SET {col_data} WHERE rowid = {self.id.get()}")
        self.con.commit()

        # diplay toast notification
        toast = ToastNotification(title="Success", message="Data updated with success.", bootstyle='success', icon='', duration=3000, position=(0,0,'nw'))
        toast.show_toast()

        # update display
        self.integrated_table.update_table()

        # clear form data
        self.clear_form()

    def delete_from_database(self):
        # checks if pandas table is connected
        if not isinstance(self.integrated_table, Integrated_Table_View):
            toast = ToastNotification(title="Warning", message="Please connect to a Pandas Table", bootstyle='warning', position=(0,0,'nw'), duration=3000, icon='')
            toast.show_toast()
            return
        
        # checks if user didn't select more than one row
        rows = self.integrated_table.get_rows(selected=True)
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
        self.con.execute(f"DELETE FROM {self.table_name} WHERE rowid = {selected_id}")
        self.con.commit()

        # diplay toast notification
        toast = ToastNotification(title="Success", message="Operation done with success.", bootstyle='success', icon='', duration=3000, position=(0,0,'nw'))
        toast.show_toast()

        # update display
        self.integrated_table.update_table()
        
    def register_button(self, master):
        btn_register = ttk.Button(master=master, text='Register', command=self.add_to_database)
        ToolTip(widget=btn_register, text='Add data to database.', bootstyle=('dark', 'inverse'))

        return btn_register
    
    def delete_button(self, master):
        self.btn_delete = ttk.Button(master=master, text='Delete', command=self.delete_from_database, bootstyle='danger')
        ToolTip(widget=self.btn_delete, text='Delete selected form database.', bootstyle=('danger', 'inverse'))

        return self.btn_delete
    
    def save_edit_button(self, master):
        self.btn_save_edit = ttk.Button(master=master, text='Save Edit', command=self.save_edit, bootstyle='success', state='disabled')
        ToolTip(widget=self.btn_save_edit, text='Saves edit to database.', bootstyle=('success', 'inverse'))

        return self.btn_save_edit
    
    def edit_button(self, master):
        btn_edit = ttk.Button(master=master, text='Edit', command=self.edit_data, bootstyle="primary-outline")
        ToolTip(widget=btn_edit, text='Fills form with selected data.', bootstyle=('dark', 'inverse'))

        return btn_edit
    
    def clear_form_button(self, master):
        btn_clear_form = ttk.Button(master=master, text='Clear', command=self.clear_form, bootstyle='warning')
        ToolTip(widget=btn_clear_form, text='Reset form of cancel edit.', bootstyle=('warning', 'inverse'))

        return btn_clear_form

    def link(self, integrated_form):
        self.linked_form = integrated_form.vars



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
        
