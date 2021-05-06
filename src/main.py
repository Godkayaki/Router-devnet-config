# helloworld.py
import tkinter as tk
import os
import pygubu
from tkinter import *

import deviceconnection

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
GUI_FILE = PROJECT_PATH+"/gui/mainui.ui"

class MainApp(Frame):
    
    #init method
    def __init__(self, parent=None):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(GUI_FILE)
        self.mainwindow = builder.get_object('mainwindow')
        
        self.defineWidgets()
        self.setupButtons()

    #define pygubu widgets
    def defineWidgets(self):
        self.entry_h = self.builder.get_object('entry_host')
        self.entry_p = self.builder.get_object('entry_port')
        self.entry_u = self.builder.get_object('entry_user')
        self.entry_pw = self.builder.get_object('entry_pswd')

    #setup buttons method
    def setupButtons(self):
        self.bt_testc = self.builder.get_object('button_testconnect')
        self.bt_c = self.builder.get_object('button_connect')

        self.bt_testc.bind("<Button-1>", self.test_connection_clicked)
        self.bt_c.bind("<Button-1>", self.connection_clicked)

    #test connection button clicked event
    def test_connection_clicked(self, event):
        host = self.entry_h.get()
        port = int(self.entry_p.get())
        user = self.entry_u.get()
        pswd = self.entry_pw.get()
        
        if deviceconnection.test_connection(host, port, user, pswd):
            messagebox.showinfo(message="Mensaje", title="Título")

    #test connection button clicked event
    def connection_clicked(self, event):
        pass

    #run application
    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Devnet Configuration")
    app = MainApp(root)
    app.run()