import ttkbootstrap as ttk
import customtkinter as ctk
from ttkbootstrap.tableview import Tableview

import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *

app = ttk.Window()

coldata = [
    {"text": "LicenseNumber", "stretch": False},
    "CompanyName",
    {"text": "UserCount", "stretch": False},
]

rowdata = [
    ('A123', 'IzzyCo', 12),
    ('A136', 'Kimdee Inc.', 45),
    ('A158', 'Farmadding Co.', 36),
    ('A158', 'Farmadding Co.', 36),
    ('A158', 'Farmadding Co.', 36),
    ('A158', 'Farmadding Co.', 36),
]

dt = Tableview(
    master=app,
    coldata=coldata,
    rowdata=rowdata,
    paginated=True,
    searchable=True,
    bootstyle='dark',
    stripecolor=('#2f2f2f', '#f5f5f5')
)
dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)

app.mainloop()