import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import filedialog
import webbrowser
import os
from info import check_updates
from difflib import SequenceMatcher
from backend import Backend


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

class Assignments:
    def __init__(self, parent:ttk.Frame, backend:Backend):
        self.parent = parent
        self.df = backend.df
        
        self.columns_norm = backend.cols
        
        self.var = []
        
        self.elements = []
        
        for i,c in enumerate(self.columns_norm):
            likely = sorted(self.df.columns,key=lambda x:SequenceMatcher(None,x,c).ratio(),reverse=True)[0]
            
            self.var.append(ttk.StringVar())
            self.var[-1].trace_add("write",lambda v,i,m,ind=i:self.update_df(ind))
            self.var[-1].set(likely)
            
            self.elements.append(
                [
                    ttk.Label(self.parent,text=c),
                    ttk.Combobox(self.parent,values=list(self.df.columns),textvariable=self.var[-1])
                ]
            )
            self.elements[-1][0].grid(row=0,column=i,padx=6,pady=(4,2),sticky="w")
            self.elements[-1][1].grid(row=1,column=i,padx=6,pady=(2,6),sticky="w")

    def update_df(self,i):
        cols = self.df.columns.values.tolist()
        self.df.columns.values[cols.index(self.var[i].get())]=self.columns_norm[i]


class Content:
    def __init__(self, parent:ttk.Frame, backend:Backend):
        self.nb = ttk.Notebook(parent)
        
        for i in range(len(backend.pools)):
            self.nb.add(self.Pool(self.nb,i,backend), text=f"Pool {i+1}",sticky="nw")
        
        self.nb.pack(anchor="w",fill=ttk.BOTH)
    
    class Pool(ttk.Frame):
        def __init__(self,master,idx,backend:Backend):
            super().__init__(master)
            
            self.persons = []
            self.backend = backend
            
            for n,row in backend.pools[idx].iterrows():###change to txt vars 
                self.persons.append(
                        [
                        ttk.Entry(self,validate="key",validatecommand=lambda e:self.edit_name(e,n),t),#####################################
                        ttk.Entry(self,validate="key",validatecommand=lambda e:self.edit_firstname(e,n)),
                        ttk.Entry(self,validate="key",validatecommand=lambda e:self.edit_age(e,n)),
                        ttk.Entry(self,validate="key",validatecommand=lambda e:self.edit_weight(e,n)),
                        ttk.Entry(self,validate="key",validatecommand=lambda e:self.edit_club(e,n)),
                    ]
                )
                
                for c,p in enumerate(self.persons[-1]):
                    p.grid(row=n,column=c)
        
        def edit_name(self,event,idx):####refractor
            print(event)
            #self.backend.df.loc[idx,"Name"] = 

        def edit_firstname(self,event,idx):##
            print(event)
            #self.backend.df.loc[idx,"Name"] = 

        def edit_age(self,event,idx):##
            print(event)
            #self.backend.df.loc[idx,"Name"] = 

        def edit_weight(self,event,idx):##
            print(event)
            #self.backend.df.loc[idx,"Name"] =         

        def edit_club(self,event,idx):##
            print(event)
            #self.backend.df.loc[idx,"Name"] = 

        class Person:####### rm this
            def __init__(self,master,idx,backend:Backend,p_idx):
                print(idx,backend,p_idx)
                


class GUI:
    root:ttk.Window
    backend:Backend
    m_cont:Content
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
        self.c_frame.pack(padx=2,pady=2,anchor="w")
        
        #assingment frame
        self.a_frame = ttk.Frame(self.root)
        self.a_frame.pack(padx=6,pady=6,anchor="w")
        
        self.m_frame = ttk.Frame(self.root)
        self.m_frame.pack(padx=6,pady=6,anchor="w",fill=ttk.BOTH)
        
        #-components
        self.g_file_e = ttk.Entry(self.c_frame,width=80)
        self.g_file_e.grid(row=0,column=0,padx=(4,8),pady=4,sticky="w")
         #self.g_file_e.bind("<Return>",self.load_df)
 
        self.g_file_b = ttk.Button(self.c_frame,text="Browse",command=self.get_file)
        self.g_file_b.grid(row=0,column=1,padx=(0,4),pady=4,sticky="w")
        
        self.cont_b = ttk.Button(self.a_frame,text="Continue",command=self.start)
        
        # check for updates
        self.updates()
    
    def about(self):
        webbrowser.open('file://' + os.path.join(os.path.split(__file__)[0],"assets/about.html"))
    
    def change_focus(self,event):
        if not isinstance(event.widget,str):
            event.widget.focus_set()

    def get_file(self):
        p = filedialog.askopenfilename(filetypes=[("Excel-Dateien", ".xlsx .xls"),("Alle-Dateien",".*")])
        if p != "":
            self.g_file_e.delete(0,ttk.END)
            self.g_file_e.insert(0,p)
            
            self.load_df()

    def load_df(self):
        path = self.g_file_e.get()
        if os.path.isfile(path):
            try:
                self.backend = Backend(path)
            except Exception as e:
                Error(f"an unexpexted error occured: {e}",self.root)
                return
        else:
            Error("The file doesn't exist",self.root)
            return
        
        self.cont_b.grid(row=2,column=0,sticky="w",padx=4,pady=6)
        
        self.assignments = Assignments(self.a_frame,self.backend)

    def updates(self):
        update = check_updates.check(self.app.ver)
        
        if update[0]:
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
    
    def start(self):
        self.backend.run()
        
        self.m_cont = Content(self.m_frame,self.backend)

    def run(self):
        self.root.mainloop()
