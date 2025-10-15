import ttkbootstrap as ttk
from tkinter import filedialog
import openpyxl
import pandas as pd
import webbrowser
import os
from info import check_updates

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
        
        #-menu
        self.root = ttk.Window(f"Pool generator - ver.{self.app.ver}")
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
        helpmenu.add_command(label="About & Help...", command=self.about)
        
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
        
        self.l_file_b = ttk.Button(self.c_frame,text="Browse",command=lambda: self.load_df(None))
        self.l_file_b.grid(row=1,column=0,sticky="w")
        
        self.updates()
    
    def about(self):
        webbrowser.open('file://' + os.path.join(os.path.split(__file__)[0],"assets/about.html"))
    
    def change_focus(self,event):
        event.widget.focus_set()

    def get_file(self):
        p = filedialog.askopenfilename(filetypes=[("Excel-Dateien", ".xlsx .xls"),("Alle-Dateien",".*")])
        if p != "":
            self.g_file_e.delete(0,ttk.END)
            self.g_file_e.insert(0,p)

    def load_df(self,e):
        path = self.g_file_e.get()
        if os.path.isfile(path):
            self.df = pd.read_excel(path)
            self.wb = openpyxl.open(path)
            self.ws = self.wb.active
        else:
            Error("The path doesn't exist",self.root)
            return

    def updates(self):
        update = check_updates.check(self.app.ver)
        
        if not update[0]:
            def open():
                info.destroy()
                webbrowser.open("https://github.com/JusPetBob/Judo-Pool-Generator/releases/tag/"+update[1])
            def cont():
                info.destroy()
                self.root.lift()
            
            print(update)
            info = ttk.Toplevel(title="Update available")
            info.geometry("200x100")
            info.maxsize(200,100)
            
            f = ttk.Frame(info)
            f.pack(side=ttk.BOTTOM,pady=2,anchor="center")
            
            open_b = ttk.Button(f,text="open",command=open)
            open_b.pack(side=ttk.LEFT,anchor="e",padx=10)
            continue_b = ttk.Button(f,text="continue",command=cont)
            continue_b.pack(side=ttk.RIGHT,padx=10)
            
            l = ttk.Label(info,borderwidth=1,text="A new version is available")
            l.pack(side=ttk.TOP,pady=4)
            
            info.after(100,info.lift)

    def run(self):
        self.root.mainloop()
