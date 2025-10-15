import gui

class App:
    def __init__(self,ver:str):
        self.ver = ver
        
        self.gui = gui.GUI(self)
        
        #self.gui.updates()
    
    def run(self):
        self.gui.run()

if __name__ == "__main__":
    app = App("0.1")
    app.run()