#!/usr/bin/python3
#-*- coding: utf-8 -*-
#Daniel Gonzalez
# 
# # helloworld.py
import os
import re
import sys
import pygubu
import tkmacosx
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from sys import platform

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
GUI_FILE = PROJECT_PATH+"/gui/mainui.ui"
sys.path.insert(1, PROJECT_PATH+"/templates")

import filters
import deviceconnection

#import PROJECT_PATH/filters

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
        self.frame_interface = self.builder.get_object('frame_interface_selected')
        
        self.entry_hn = self.builder.get_object('entry_hostname')
        self.entry_hn_var = tk.StringVar()
        self.entry_hn.configure(textvariable=self.entry_hn_var)
        self.text_motd = self.builder.get_object('text_motd')
        self.combobox_interfaces = self.builder.get_object('combobox_interfaces')

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

    #apply router configuration (motds and hostname)
    def aplicar_config(self, event):
        newhostname = self.entry_hn.get()
        newmotdbanner = self.text_motd.get()

        print(newhostname, newmotdbanner)

    #create frame
    def create_interface_frame(self):
        print("create frame with interface options (ip, mask, gateway...)")

        frame_ip = tk.Frame(self.frame_interface, padx=30, pady=30)
        frame_ip.pack(side="top", expand=False, fill="x")
        frame_ip_lbl = tk.Frame(frame_ip)
        frame_ip_lbl.pack(side="left", expand=True, fill="x")
        frame_ip_entry = tk.Frame(frame_ip)
        frame_ip_entry.pack(side="right", expand=True, fill="x")

        ip_lbl = tk.Label(frame_ip_lbl, text="hola")
        ip_lbl.pack(side="right")
        ip_entry = tk.Entry(frame_ip_entry)
        ip_entry.pack(side="left")

    #combobox interface selected
    def interface_selected(self, event):
        option = self.combobox_interfaces.get()

        if option == "Interfície...":
            return

        last_i = int(option[-1])
        #print(last_i)

        #get interface data
        interfaces_res = str(self.conection.get_config('running', filters.interface_filter))
        request = '<GigabitEthernet><name>'+str(last_i)+'</name>(.*)</GigabitEthernet>'
        singleinter = re.findall(request, interfaces_res)[0]
        #final interface data filtered by option selected
        interface_info = singleinter.split('</GigabitEthernet>')[0]

        self.create_interface_frame()

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

        #get values from entry text
        host = self.entry_h.get()
        port = self.entry_p.get()
        user = self.entry_u.get()
        pswd = self.entry_pw.get()

        #make conection
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

        #get hostname name and set it to entrytext
        result = str(self.conection.get_config('running', filters.hostname_filter))
        hostname = re.findall('<hostname>(.*)</hostname>', result)[0]
        self.entry_hn_var.set(hostname)

        #get actual motd and set it to the text
        result = str(self.conection.get_config('running', filters.motd_filter))
        #double filter because of <banner><motd><banner>text</banner></motd></banner>
        a = re.findall('<banner>(.*)</banner>', result)[0]
        motd = re.findall('<banner>(.*)</banner>', a)[0]
        self.text_motd.insert(END, motd)

        #get quantity of Gigabitehternet interfaces there are in the router
        result = str(self.conection.get_config('running', filters.interface_filter))
        num_interf = re.findall('<name>(.*)</name>', result)[0]
        last_i = int(num_interf[-1])

        interfaces = []
        for i in range (1,last_i+1):
            interfaces.append("GigabitEthernet "+str(i))
        #print(interfaces)
        self.combobox_interfaces.configure(values=interfaces, state="readonly")
        self.combobox_interfaces.set('Interfície...')
        self.combobox_interfaces.bind('<<ComboboxSelected>>', self.interface_selected)

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