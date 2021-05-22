#!/usr/bin/python3
#-*- coding: utf-8 -*-
#Daniel Gonzalez
# 
# # helloworld.py
import os
import re
import pygubu
import tkmacosx
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from sys import platform

import filters
import deviceconnection

if platform == "linux" or platform == "linux2":
    PLATFORM = "gnu"
elif platform == "darwin":
    PLATFORM = "mac"
elif platform == "win32":
    PLATFORM = "win"
else:
    sys.exit(0)

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
GUI_FILE = PROJECT_PATH+"/gui/mainui.ui"

'''if PLATFORM == "mac":
    GUI_FILE = PROJECT_PATH+"/gui/mainui_mac.ui"
else:
    GUI_FILE = PROJECT_PATH+"/gui/mainui.ui"'''

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
        self.test_c_frame = self.builder.get_object('frame4')
        self.c_frame = self.builder.get_object('frame5')
        self.disc_frame = self.builder.get_object('frame_disconnect_bt')

        self.entry_h = self.builder.get_object('entry_host')
        self.entry_p = self.builder.get_object('entry_port')
        self.entry_u = self.builder.get_object('entry_user')
        self.entry_pw = self.builder.get_object('entry_pswd')

    #setup buttons method
    def setupButtons(self):
        '''if PLATFORM == "mac":
            self.bt_testc = tkmacosx.Button(self.test_c_frame, text='Provar conexió', bg='white',fg='black', borderless=1)
            self.bt_testc.pack(side="right")
            self.bt_c = tkmacosx.Button(self.c_frame, text='Conectar', bg='white',fg='black', borderless=1)
            self.bt_c.pack(side="left")
            self.bt_disc = tkmacosx.Button(self.disc_frame, text='Desconectar', bg='white',fg='black', borderless=1)
            self.bt_disc.pack(side="right", padx=30)
        else:'''
        
        self.entry_hn = self.builder.get_object('entry_hostname')
        self.entry_hn_var = tk.StringVar()
        self.entry_hn.configure(textvariable=self.entry_hn_var)
        self.text_motd = self.builder.get_object('text_motd')

        self.bt_testc = self.builder.get_object('button_testconnect')
        self.bt_c = self.builder.get_object('button_connect')
        self.bt_disc = self.builder.get_object('button_disconnect')
        self.bt_aplicar = self.builder.get_object('button_aplicar')

        self.bt_testc.bind("<Button-1>", self.test_connection_clicked)
        self.bt_c.bind("<Button-1>", self.connection_clicked)
        self.bt_disc.bind("<Button-1>", self.disconnet_from)
        self.bt_aplicar.bind("<Button-1>", self.aplicar_config)

    #disable all children from parent passed as reference
    def disableChildren(self, parent):
        for child in parent.winfo_children():
            wtype = child.winfo_class()
            if wtype not in ('Frame','Labelframe'):
                try:
                    child.configure(state='disabled')
                except:
                    pass
            else:
                self.disableChildren(child)

    #enable all children from parent passed as reference
    def enableChildren(self, parent):
        for child in parent.winfo_children():
            wtype = child.winfo_class()
            if wtype not in ('Frame','Labelframe'):
                try:
                    child.configure(state='normal')
                except:
                    pass
            else:
                self.enableChildren(child)

    def aplicar_config(self, event):
        newhostname = self.entry_hn.get()
        newmotdbanner = self.text_motd.get()

        print(newhostname, newmotdbanner)

    #test connection button clicked event
    def test_connection_clicked(self, event):
        if self.bt_testc['state'] == "disabled":
            return

        host = self.entry_h.get()
        port = self.entry_p.get()
        user = self.entry_u.get()
        pswd = self.entry_pw.get()
        
        if host != '' and port != '' and user != '' and pswd != '':
            if not deviceconnection.test_connection(host, int(port), user, pswd):
                messagebox.showinfo(message="No es pot establir una conexió amb el router.", title="Error de conexió.")
            else:
                messagebox.showinfo(message="La conexió amb el router s'ha produït correctament.", title="Conexió correcte.")
        else:
            messagebox.showinfo(message="Els camps no poden estar buits.", title="Error de format.")

    #test connection button clicked event
    def connection_clicked(self, event):
        if self.bt_c['state'] == "disabled":
            return

        host = self.entry_h.get()
        port = self.entry_p.get()
        user = self.entry_u.get()
        pswd = self.entry_pw.get()

        if host != '' and port != '' and user != '' and pswd != '':
            self.conection = deviceconnection.return_connection(host, int(port), user, pswd)
            if self.conection == False:
                messagebox.showinfo(message="No es pot establir una conexió amb el router.", title="Error de conexió.")
            else:
                print("Conexió exitosa.")
                self.disableChildren(self.conn_frame)
                self.enableChildren(self.config_frame)
                self.bt_disc.configure(state="normal")

        else:
            messagebox.showinfo(message="Els camps no poden estar buits.", title="Error de format.")

        result = str(self.conection.get_config('running', filters.hostname_filter))
        hostname = re.findall('<hostname>(.*)</hostname>', result)[0]
        self.entry_hn_var.set(hostname)

        result = str(m.get_config('running', filters.interface_filter))

    #quit connection
    def disconnet_from(self, event):
        if self.bt_disc['state'] == "disabled":
            return

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