#!/usr/bin/python3
#-*- coding: utf-8 -*-
#Daniel Gonzalez
# 
# # helloworld.py
import os
import re
import sys
import lxml
import pygubu
import tkmacosx
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from jinja2 import Template
from tkinter import messagebox
from sys import platform

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
GUI_FILE = PROJECT_PATH+"/gui/mainui.ui"
sys.path.insert(1, PROJECT_PATH+"/templates")

print(PROJECT_PATH)

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
        self.bt_copyconfig = self.builder.get_object('button_copyrs')

        self.bt_testc.bind("<Button-1>", self.test_connection_clicked)
        self.bt_c.bind("<Button-1>", self.connection_clicked)
        self.bt_disc.bind("<Button-1>", self.disconnet_from)
        self.bt_aplicar.bind("<Button-1>", self.aplicar_config)
        self.bt_copyconfig.bind("<Button-1>", self.copy_config)

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

    #copy config
    def copy_config(self, event):
        if self.bt_copyconfig['state'] == "disabled":
            return

        filename = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=(("Extensible Markup Language file", "*.xml"),("All Files", "*.*")))
        
        if filename == None or filename == "":
            return

        result = self.conection.get_config('running', filters.full_filter)
        with open(filename, "w") as outfile:
            outfile.write(str(result))

        tree = lxml.etree.parse(filename)
        pretty = lxml.etree.tostring(tree, encoding="unicode", pretty_print=True)

        with open(filename, "w") as outfile:
            outfile.write(pretty)

    #apply interface configuration
    def aplicar_int_config(self, event):
        ip = self.ip_var.get()
        mascara = self.mask_var.get()
        
        try:
            interface_template = Template(open(PROJECT_PATH+'/templates/interface.xml').read())
            interface_rendered = interface_template.render(
                INTERFACE_INDEX=self.curr_interface,
                IP_ADDRESS=ip,
                SUBNET_MASK=mascara
            )
            result = self.conection.edit_config(target='running', config=interface_rendered)
            messagebox.showinfo(message="Configuració actualitzada correctament.", title="Actualització.")
        except:
            messagebox.showinfo(message="No ha sigut posible actualitzar els valors del router.\n Revisa que la ip i la mascara tinguin el format correcte.", title="Error d'update.")

    #apply router configuration (motds and hostname)
    def aplicar_config(self, event):
        newhostname = self.entry_hn.get()
        newmotdbanner = self.text_motd.get("1.0",END)

        try:
            hostname_template = Template(open(PROJECT_PATH+'/templates/hostname.xml').read())
            hostname_rendered = hostname_template.render(
                HOSTNAME=newhostname, 
                BANNER_MOTD=newmotdbanner
            )
            result = self.conection.edit_config(target='running', config=hostname_rendered)
            messagebox.showinfo(message="Configuració actualitzada correctament.", title="Actualització.")
        except:
            messagebox.showinfo(message="No ha sigut posible actualitzar els valors del router.", title="Error d'update.")

    #destroy all childs from self.frame_interface
    def destroy_int_frame(self):
        for child in self.frame_interface.winfo_children():
            child.destroy()

    #create frame
    def create_interface_frame(self, interface_num):
        #print("create frame with interface options (ip, mask, gateway...)")
        self.curr_interface = interface_num

        frame_data = tk.Frame(self.frame_interface, pady=30)
        frame_data.pack(side="top", fill="both")

        #ip frame
        frame_ip = tk.Frame(frame_data, height=10)
        frame_ip.pack(side="top", fill="x", pady=5)
        
        frame_ip_lbl = tk.Frame(frame_ip, height=20)
        frame_ip_lbl.pack(side="left", expand=True, fill="x")
        frame_ip_lbl.pack_propagate(0)
        frame_ip_entry = tk.Frame(frame_ip, height=30, width=20)
        frame_ip_entry.pack(side="right", expand=True, fill="x")
        frame_ip_entry.pack_propagate(0)

        ip_lbl = tk.Label(frame_ip_lbl, text="IP: ")
        ip_lbl.pack(side="right", expand=False)
        self.ip_entry = tk.Entry(frame_ip_entry)
        self.ip_entry.pack(side="left")

        #mask frame
        frame_mask = tk.Frame(frame_data, height=10)
        frame_mask.pack(side="top", fill="x", pady=5)

        frame_mask_lbl = tk.Frame(frame_mask, height=20)
        frame_mask_lbl.pack(side="left", expand=True, fill="x")
        frame_mask_lbl.pack_propagate(0)
        frame_mask_entry = tk.Frame(frame_mask, height=30, width=20)
        frame_mask_entry.pack(side="right", expand=True, fill="x")
        frame_mask_entry.pack_propagate(0)

        mask_lbl = tk.Label(frame_mask_lbl, text="Mascara: ")
        mask_lbl.pack(side="right", expand=False)
        self.mask_entry = tk.Entry(frame_mask_entry)
        self.mask_entry.pack(side="left")

        '''#gateway frame
        frame_gw = tk.Frame(frame_data, height=10)
        frame_gw.pack(side="top", fill="x", pady=5)
        
        frame_gw_lbl = tk.Frame(frame_gw, height=20)
        frame_gw_lbl.pack(side="left", expand=True, fill="x")
        frame_gw_lbl.pack_propagate(0)
        frame_gw_entry = tk.Frame(frame_gw, height=30, width=20)
        frame_gw_entry.pack(side="right", expand=True, fill="x")
        frame_gw_entry.pack_propagate(0)

        gw_lbl = tk.Label(frame_gw_lbl, text="Porta d'enllaç: ")
        gw_lbl.pack(side="right", expand=False)
        gw_entry = tk.Entry(frame_gw_entry)
        gw_entry.pack(side="left")'''

        #apply changes frame
        frame_apply = tk.Frame(self.frame_interface, height=35)
        frame_apply.pack(side="bottom", fill="x", expand=False)
        frame_apply.pack_propagate(0)
        
        self.bt_int_aplicar = tk.Button(frame_apply, text="Aplicar")
        self.bt_int_aplicar.pack(side="top", expand=False)
        self.bt_int_aplicar.bind("<Button-1>", self.aplicar_int_config)

        '''lambda event, a=10, b=20, c=30:
                            self.rand_func(a, b, c))'''

        #define StringVar to textvariable
        self.ip_var = tk.StringVar()
        self.mask_var = tk.StringVar()
        #self.gw_var = tk.StringVar()

        self.ip_entry.configure(textvariable=self.ip_var)
        self.mask_entry.configure(textvariable=self.mask_var)
        #gw_entry.configure(textvariable=self.mask_var)

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

        #get ip address
        try:
            ip_address_1 = re.findall('<address>(.*)</address>', interface_info)[0]
            ip_address = re.findall('<address>(.*)</address>', ip_address_1)[0]
            if len(ip_address) > 15:
                tmp = ip_address.split(">")
                ip_address = tmp[-1]
        except:
            ip_address = ""

        #get mask
        try:
            mascara = re.findall('<mask>(.*)</mask>', interface_info)[0]
            if len(mascara) > 15:
                tmp = mascara.split(">")
                mascara = tmp[-1]
        except:
            mascara = ""

        self.destroy_int_frame()
        self.create_interface_frame(last_i)

        self.frame_interface.after(100, self.set_values, ip_address, mascara)

        #self.ip_var.set(ip_address)
        #self.ip_var.set(mascara)
        #print(ip_address, mascara)
        #print(type(ip_address), mascara)
        #self.frame_interface.update()

    def set_values(self, ip_address, mascara):
        #print(ip_address, mascara)
        self.ip_var.set(ip_address)
        self.mask_var.set(mascara)

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

        try:
            #get actual motd and set it to the text
            result = str(self.conection.get_config('running', filters.motd_filter))
            #double filter because of <banner><motd><banner>text</banner></motd></banner>
            a = re.findall('<banner>(.*)</banner>', result)[0]
            motd = re.findall('<banner>(.*)</banner>', a)[0]
        except:
            motd = ""
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
        self.destroy_int_frame()
        self.enableChildren(self.conn_frame)

    #run application
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Devnet Configuration")
    app = MainApp(root)
    app.run()