import ttkbootstrap as ttk
from tkinter import filedialog
import openpyxl
import pandas as pd
import webbrowser
from os import path

class Error:
    def __init__(self,message,parent:ttk.Window):
        self.parent = parent
        
        self.root = ttk.Toplevel(title="Error")
        self.root.geometry("200x100")
        
        self.t = ttk.Label(self.root,text=message,style="danger")
        self.t.pack(anchor="w",side="top",pady=2,padx=2)
        
        self.ok = ttk.Button(self.root,text="Ok",command=self.close)
        self.ok.pack(anchor="ne",side="bottom",pady=4,padx=4)
        
        self.root.lift()
        self.root.focus_force()
        self.root.grab_set()

    def close(self):
        self.root.grab_release()
        self.root.destroy()
        self.parent.focus_get()
        self.parent.deiconify()

class GUI:
    root:ttk.Window
    df:pd.DataFrame
    wb:openpyxl.Workbook
    columns:list = []
    def __init__(self,app):
        self.app = app
        
        self.root = ttk.Window(f"Pool generator-{self.app.ver}")
        self.root.geometry("700x300")
        self.root.bind_all('<Button>', self.change_focus)
        
        menu = ttk.Menu(self.root)
        self.root.config(menu=menu)
        filemenu = ttk.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open...", command=self.get_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)

        helpmenu = ttk.Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.about)
        
        #-frames
        self.c_frame = ttk.Frame(self.root)
        self.c_frame.grid(row=0,column=0,padx=2,pady=2)
        
        self.m_frame = ttk.Frame(self.root)
        self.m_frame.grid(row=2,column=0)
        
        #-components
        self.g_file_e = ttk.Entry(self.c_frame,width=80)
        self.g_file_e.grid(row=0,column=0)
        self.g_file_e.bind("<Return>",self.load_df)

        self.g_file_b = ttk.Button(self.c_frame,text="Browse",command=self.get_file)
        self.g_file_b.grid(row=0,column=1)
    
    def about(self):
        webbrowser.open('file://' + path.join(path.split(__file__)[0],"help/about.html"))
    
    def change_focus(self,event):
        event.widget.focus_set()

    def get_file(self):
        p = filedialog.askopenfilename(filetypes=[("Excel-Dateien", ".xlsx .xls"),("Alle-Dateien",".*")])
        if p != "":
            self.g_file_e.delete(0,ttk.END)
            self.g_file_e.insert(0,p)

    def load_df(self,e):
        path = self.g_file_e.get()
        try:
            self.df = pd.read_excel(path)
            self.wb = openpyxl.open(path)
            self.ws = self.wb.active
        except:
            Error("Der Pfad wurde nicht gefunden",self.root)
            return

    def run(self):
        self.root.mainloop()
