import customtkinter as ctk
import CTkTable
import pandas as pd
import numpy as np
import sqlite3
from CTkToolTip import CTkToolTip

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


class SearchInDatabase(ctk.CTkFrame):
    """
        A Table widget with a field for searching data from a database
        parameters:
            master: parent widget
            con: sqlite3.Connertion to a database
            by: column to search by in a database table
            table_name: name of the database table
            display_table_cols: list of table columns names to display
    """
    
    def __init__(self, master, con: sqlite3.Connection, by: str, table_name: str, display_table_cols: list):
        super().__init__(master=master)
        self.by = by
        self.con = con
        self.table_name = table_name
        self.display_table_cols = display_table_cols 
        self.str_entry = ctk.StringVar()

        # layout
        self.rowconfigure(index=0, weight=1, uniform='a')
        self.rowconfigure(index=1, weight=5, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')

        # widgets
        
        # Search Field
        frame1 = ctk.CTkFrame(master=self)
        
        frame1.rowconfigure(index=0, weight=1, uniform='a')
        frame1.columnconfigure(index=0, weight=4, uniform='a')
        frame1.columnconfigure(index=1, weight=1, uniform='a')

        frame1.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)

        entry = ctk.CTkEntry(master=frame1, placeholder_text='Enter a Name', textvariable=self.str_entry)
        entry.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)

        btn = ctk.CTkButton(master=frame1, text="Search", command=lambda: self.update_query(table=table, con=con))
        btn.grid(row=0, column=1, sticky='nswe', padx=5, pady=5)

        # Table
        frame2 = ctk.CTkScrollableFrame(master=self)
        frame2.grid(row=1, column=0, sticky='nswe')
        
        query_str = self.select_all_sql_string()
        query = pd.read_sql(query_str, con=self.con)
        
        table = Table(master=frame2, values=query) 
        table.pack(fill='both', expand=True)

        # tooltips
        CTkToolTip(widget=btn, message="search by name")
        CTkToolTip(widget=entry, message="name")

    def update_query(self, table: Table, con):
        query = pd.read_sql(f"{self.select_all_sql_string()} WHERE {self.by} LIKE '%{self.str_entry.get()}%'", con=con)
        new_data = query.to_numpy().tolist()
        new_data.insert(0, query.columns.values.tolist())
        table.update_values(new_data)
    
    def select_all_sql_string(self):
        tables_str = ''
        for table in self.display_table_cols:
            tables_str += table + ','
        tables_str = tables_str[:-1]
        return f"SELECT {tables_str} FROM {self.table_name}"


# DATABASE
class Database:
    def __init__(self, con: sqlite3.Connection):
        self.con = con

    def insert_into(self, table_name: str, data):
        if isinstance(data, type(None)):
            raise ValueError("data parameter cannot be None type")
        cursor = self.con.cursor()
        if isinstance(data, (list, tuple)):
            cursor.execute(f"INSERT INTO {table_name} VALUES {tuple(data)}")
            self.con.commit()
    
    def read(self, sql_string: str, return_as='list'):
        cursor = self.con.cursor()
        if return_as == 'list': # DEBUG Do not return heaaders
            query = cursor.execute(sql_string)
            return [list(row) for row in query]
        if return_as =='dataframe':
            return pd.read_sql(sql_string, con=self.con)
        if return_as == 'dict':
            return pd.read_sql(sql_string, con=self.con).to_dict()
    
    def delete(self, table_name: str, condition: str):
        cursor = self.con.cursor()
        delete_str = f"DELETE FROM {table_name} WHERE {condition}"
        cursor.execute(delete_str)
        self.con.commit()
    
    def update(self, table_name: str, values, condition):
        update_str = f"UPDATE {table_name} SET {values} WHERE {condition}"
        cursor = self.con.cursor()
        cursor.execute(update_str)
        self.con.commit()



            


