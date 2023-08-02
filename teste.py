import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
from math import floor
import pandas as pd
import numpy as np

class App(ctk.CTk):
    def __init__(self):
        # initial setup
        super().__init__()
        self.title("My Window")
        self.geometry('700x500')

        # layout
        self.rowconfigure(index=(0,1), weight=1, uniform='a')
        self.columnconfigure(index=(0,1), weight=1, uniform='a')


        tree_view = MyTreeView(master=self, displaycols=['mamamia', 'peperoni', 'modafoca', 'shazan!'],
            on_right_click=lambda event: print('right-click'),
            on_delete=lambda event: print('delete'),
            on_click=lambda event: print('click'),
            on_double_click=lambda event: print('double-click')    
        )
        tree_view.grid(row=0, column=0, sticky='nswe', rowspan=1, columnspan=1)
        self.mainloop()


class MyTreeView(ttk.Treeview):
    def __init__(self,
            master, 
            displaycols: list,
            on_click=lambda event: event,
            on_double_click=lambda event: event,
            on_right_click=lambda event: event,
            on_delete=lambda event: event,
        ):
        
        # STYLE
        # style = ttk.Style()
        # style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        # style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        # style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        # INITIAL SETUP
        self.displaycols = displaycols
        super().__init__(
            master=master, 
            columns=tuple(displaycols),
            show='headings',
        )
        self.width = self.winfo_screenmmwidth()

        # AUTORESIZE COLUMNS
        for heading in displaycols:
            col_width = floor(self.width / (len(displaycols)))
            self.column(heading, width=col_width, stretch=False)
            self.heading(heading, text=heading)
        
        # DEBUG
        for _ in range(15):
            self.insert(parent='', index=tk.END, values=tuple('teste' for _ in range(len(displaycols))))
        
        # BINDING
        self.bind('<Delete>', lambda event: on_delete(event))
        self.bind('<<TreeviewSelect>>', lambda event: on_click(event))
        self.bind('<Double-1>', lambda event: on_double_click(event))
        self.bind('<Button-3>', lambda event: on_right_click(event))

    # METHODS
    def add_row(self, row: list):
        self.insert(parent='', index=tk.END, values=row)
    
    def add_rows(self, rows: list):
        for row in rows:
            self.insert(parent='', index=tk.END, values=row)
    
    def delete_all(self):
        for item in self.get_children():
            self.delete(item)
           

App()
