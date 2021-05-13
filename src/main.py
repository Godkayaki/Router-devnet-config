#!/usr/bin/python3
#-*- coding: utf-8 -*-
#Daniel Gonzalez
# 
# # helloworld.py
import tkinter as tk
import os
import pygubu
from tkinter import *
from tkinter import messagebox

import deviceconnection as dv

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
        self.disableChildren(self.config_frame)

    #define pygubu widgets
    def defineWidgets(self):
        self.config_frame = self.builder.get_object('frame_configuration')
        self.conn_frame = self.builder.get_object('frame_connection')
        self.entry_h = self.builder.get_object('entry_host')
        self.entry_p = self.builder.get_object('entry_port')
        self.entry_u = self.builder.get_object('entry_user')
        self.entry_pw = self.builder.get_object('entry_pswd')

    #setup buttons method
    def setupButtons(self):
        self.bt_testc = self.builder.get_object('button_testconnect')
        self.bt_c = self.builder.get_object('button_connect')
        self.bt_disc = self.builder.get_object('button_disconnect')

        self.bt_testc.bind("<Button-1>", self.test_connection_clicked)
        self.bt_c.bind("<Button-1>", self.connection_clicked)
        self.bt_disc.bind("<Button-1>", self.disconnet_from)

    #disable all children from parent passed as reference
    def disableChildren(self, parent):
        for child in parent.winfo_children():
            wtype = child.winfo_class()
            if wtype not in ('Frame','Labelframe'):
                child.configure(state='disable')
            else:
                self.disableChildren(child)

    #enable all children from parent passed as reference
    def enableChildren(self, parent):
        for child in parent.winfo_children():
            wtype = child.winfo_class()
            if wtype not in ('Frame','Labelframe'):
                child.configure(state='normal')
            else:
                self.enableChildren(child)

    #test connection button clicked event
    def test_connection_clicked(self, event):
        host = self.entry_h.get()
        port = self.entry_p.get()
        user = self.entry_u.get()
        pswd = self.entry_pw.get()
        
        if host != '' and port != '' and user != '' and pswd != '':
            if not deviceconnection.test_connection(host, int(port), user, pswd):
                messagebox.showinfo(message="No es pot establir una conexió amb el router.", title="Error de conexió.")
            else:
                messagebox.showinfo(message="La conexió amb el router s'ha prduït correctament.", title="Conexió correcte.")
        else:
            messagebox.showinfo(message="Els camps no poden estar buits.", title="Error de format.")

    #test connection button clicked event
    def connection_clicked(self, event):
        host = self.entry_h.get()
        port = self.entry_p.get()
        user = self.entry_u.get()
        pswd = self.entry_pw.get()

        if host != '' and port != '' and user != '' and pswd != '':
            c = deviceconnection.return_connection(host, int(port), user, pswd)
            if c == False:
                messagebox.showinfo(message="No es pot establir una conexió amb el router.", title="Error de conexió.")
            else:
                print("conexio exitosa.")
                self.disableChildren(self.conn_frame)
                self.enableChildren(self.config_frame)

        else:
            messagebox.showinfo(message="Els camps no poden estar buits.", title="Error de format.")

    #quit connection
    def disconnet_from(self, event):
        self.disableChildren(self.config_frame)
        self.enableChildren(self.conn_frame)

    #run application
    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Devnet Configuration")
    app = MainApp(root)
    app.run()