# uncompyle6 version 3.9.0
# Python bytecode version base 3.6 (3379)
# Decompiled from: Python 3.6.1 (v3.6.1:69c0db5, Mar 21 2017, 18:41:36) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: readergui.py
# Compiled at: 1995-09-28 00:18:56
# Size of source mod 2**32: 272 bytes
import base64, os, tkinter as tk, tkinter.font as tkFont
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinterdnd2 as tkdnd
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from readbq import read_bq
from ecudid import ecudid
import copy
from tkinter import filedialog
from SIDIDlist import sididlist, comparesidid
from ECDlist import ecdlist, ecdcompare
from DTClist import dtclist, dtccompare
from dtcstatus import dtcstatusconfirm
from markdifferent import markdifferent
from sortexcel import sortexcel
import pyperclip, win32com.client as win32, pandas as pd
from PIL import Image, ImageTk
from ttkbootstrap import Style
from versionrecord import record2excel, updaterecord
from readswbom import readswbom, vn2featurelist, is_fit
from BOMcompare import bomcompare
import webbrowser
from githubinfo import updateornot
import threading, difflib
import subprocess


class App:

    def __init__(self, root, githubinfo):
        self.root = root
        self.curver = 200
        self.githubinfo = githubinfo
        self.root.wm_attributes('-alpha', 0.0)
        root.title('E-LAB Busquery File Reader version 2.0')
        tmpimg = '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'
        with open('tmp.ico', 'wb') as (tmp):
            tmp.write(base64.b64decode(tmpimg))
        root.wm_iconbitmap('tmp.ico')
        os.remove('tmp.ico')
        width = 800
        height = 600
        root.wm_minsize(width=800, height=400)
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        self.ft = tkFont.Font(family='Times', size=10)
        self.fts = tkFont.Font(family='Times', size=7)
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)
        root.bind('<Configure>', self.WindowResize)
        root.drop_target_register(DND_FILES)
        root.dnd_bind('<<Drop>>', self.on_drop)
        style.theme_use('minty')
        self.button_bg = '#e0e0e0'
        self.button_unselected_bg = '#606060'
        self.button_selected_bg = '#009999'
        self.switch_button1 = tk.Button(root, text='Single BusQuery File Retrieval', command=(self.show_layout1), bg=(self.button_selected_bg))
        self.switch_button2 = tk.Button(root, text='Two BusQuery Files Comparison', command=(self.show_layout2), bg=(self.button_unselected_bg))
        self.switch_button3 = tk.Button(root, text='SW BOM Checker Comparison', command=(self.show_layout3), bg=(self.button_unselected_bg))

        self.Website_Button = tk.Button(root)
        self.Website_Button['font'] = self.ft
        self.Website_Button['bg'] = self.button_bg
        self.Website_Button['justify'] = 'left'
        self.Website_Button['text'] = 'Sharepoint'
        self.Website_Button['command'] = self.website_click

        self.Update_Button = tk.Button(root)
        self.Update_Button['font'] = self.ft
        self.Update_Button['bg'] = 'orange'
        self.Update_Button['justify'] = 'left'
        self.Update_Button['text'] = 'Update to New Version'
        self.Update_Button['command'] = self.update_click

        self.Filepath_Label = tk.Label(root)
        self.Filepath_Label['font'] = self.ft
        self.Filepath_Label['fg'] = '#333333'
        self.Filepath_Label['justify'] = 'left'
        self.Filepath_Label['text'] = 'Bus Query Filepath:'
        self.DateTime = tk.StringVar()
        self.DateTime.set('')
        self.Time_Label = tk.Label(root)
        self.Time_Label['font'] = self.ft
        self.Time_Label['fg'] = '#333333'
        self.Time_Label['justify'] = 'left'
        self.Time_Label['textvariable'] = self.DateTime
        self.ECUno = tk.StringVar()
        self.ECUno.set('0 ECU')
        self.ECU_Label = tk.Label(root)
        self.ECU_Label['font'] = self.ft
        self.ECU_Label['fg'] = '#333333'
        self.ECU_Label['bg'] = '#CCFFFF'
        self.ECU_Label['justify'] = 'left'
        self.ECU_Label['textvariable'] = self.ECUno
        self.Filepath_Label2 = tk.Label(root)
        self.Filepath_Label2['font'] = self.ft
        self.Filepath_Label2['fg'] = '#333333'
        self.Filepath_Label2['justify'] = 'left'
        self.Filepath_Label2['text'] = 'Second BQ Filepath:'
        self.DateTime2 = tk.StringVar()
        self.DateTime2.set('')
        self.Time_Label2 = tk.Label(root)
        self.Time_Label2['font'] = self.ft
        self.Time_Label2['fg'] = '#333333'
        self.Time_Label2['justify'] = 'left'
        self.Time_Label2['textvariable'] = self.DateTime2
        self.ECUno2 = tk.StringVar()
        self.ECUno2.set('0 ECU')
        self.ECU_Label2 = tk.Label(root)
        self.ECU_Label2['font'] = self.ft
        self.ECU_Label2['fg'] = '#333333'
        self.ECU_Label2['bg'] = '#CCFFFF'
        self.ECU_Label2['justify'] = 'left'
        self.ECU_Label2['textvariable'] = self.ECUno2
        self.runstatus = 1
        self.ecustmp = []
        self.bqinfo1 = {}
        self.bqinfo2 = {}
        self.bqinfo = {}
        self.bominfo = {}
        self.bomver = ''
        self.filepath = tk.StringVar()
        self.Filepath_Entry = tk.Entry(root)
        self.Filepath_Entry['font'] = self.ft
        self.Filepath_Entry['fg'] = '#333333'
        self.Filepath_Entry['justify'] = 'left'
        self.Filepath_Entry['textvariable'] = self.filepath
        self.Filepath_Entry.bind('<Return>', self.filepath_entry)
        self.Filepath_Button = tk.Button(root)
        self.Filepath_Button['font'] = self.ft
        self.Filepath_Button['fg'] = '#333333'
        self.Filepath_Button['bg'] = self.button_bg
        self.Filepath_Button['justify'] = 'left'
        self.Filepath_Button['text'] = '...'
        self.Filepath_Button['command'] = self.filepath_button
        self.filestickno = 1
        self.filepath2 = tk.StringVar()
        self.Filepath_Entry2 = tk.Entry(root)
        self.Filepath_Entry2['font'] = self.ft
        self.Filepath_Entry2['fg'] = '#333333'
        self.Filepath_Entry2['justify'] = 'left'
        self.Filepath_Entry2['textvariable'] = self.filepath2
        self.Filepath_Entry2.bind('<Return>', self.filepath_entry2)
        self.Filepath_Button2 = tk.Button(root)
        self.Filepath_Button2['font'] = self.ft
        self.Filepath_Button2['fg'] = '#333333'
        self.Filepath_Button2['bg'] = self.button_bg
        self.Filepath_Button2['justify'] = 'left'
        self.Filepath_Button2['text'] = '...'
        self.Filepath_Button2['command'] = self.filepath_button2
        self.Bomcheckerpath_Label = tk.Label(root)
        self.Bomcheckerpath_Label['font'] = self.ft
        self.Bomcheckerpath_Label['fg'] = '#333333'
        self.Bomcheckerpath_Label['justify'] = 'left'
        self.Bomcheckerpath_Label['text'] = 'BOMChecker Path:'
        self.filepath3 = tk.StringVar()
        self.Filepath_Entry3 = tk.Entry(root)
        self.Filepath_Entry3['font'] = self.ft
        self.Filepath_Entry3['fg'] = '#333333'
        self.Filepath_Entry3['justify'] = 'left'
        self.Filepath_Entry3['textvariable'] = self.filepath3
        self.Filepath_Entry3.bind('<Return>', self.filepath_entry3)
        self.Filepath_Button3 = tk.Button(root)
        self.Filepath_Button3['font'] = self.ft
        self.Filepath_Button3['fg'] = '#333333'
        self.Filepath_Button3['bg'] = self.button_bg
        self.Filepath_Button3['justify'] = 'left'
        self.Filepath_Button3['text'] = '...'
        self.Filepath_Button3['command'] = self.filepath_button3
        self.Bomverinfo = tk.StringVar()
        self.Bomverinfo.set('')
        self.Bomverinfo_Label = tk.Label(root)
        self.Bomverinfo_Label['font'] = self.fts
        self.Bomverinfo_Label['fg'] = '#333333'
        self.Bomverinfo_Label['justify'] = 'left'
        self.Bomverinfo_Label['textvariable'] = self.Bomverinfo
        style.theme_use('vista')
        self.save_width = 800
        self.save_height = 600
        self.frame4 = tk.Frame(root, width=790, height=460)
        self.frame4.pack_propagate(0)
        self.frame4.place(x=5, y=140)
        self.Result_Sheet = ttk.Treeview(self.frame4)
        vsb = ttk.Scrollbar((self.frame4), orient='vertical', command=(self.Result_Sheet.yview))
        vsb.pack(side='right', fill='y')
        self.Result_Sheet.configure(yscrollcommand=(vsb.set))
        self.Result_Sheet.pack(expand=True, fill='both')
        self.Result_Sheet.bind('<Control-c>', self.copy_selection)
        self.ecunamedic = ecudid()
        tmp = tuple(['No File Imported'])
        self.ECUselect_Combobox = ttk.Combobox(root)
        self.ECUselect_Combobox['state'] = 'normal'
        self.ECUselect_Combobox['font'] = self.ft
        self.ECUselect_Combobox['justify'] = 'left'
        self.ECUselect_Combobox['value'] = tmp
        self.ECUselect_Combobox.bind('<<ComboboxSelected>>', self.ecuselct_combobox)
        self.ECUselect_Combobox.current(0)
        self.ECUselect_Label = tk.Label(root)
        self.ECUselect_Label['font'] = self.ft
        self.ECUselect_Label['fg'] = '#333333'
        self.ECUselect_Label['justify'] = 'left'
        self.ECUselect_Label['text'] = 'Module:'
        self.curecu = '000'
        self.ECUmultiselect_Label = tk.Label(root)
        self.ECUmultiselect_Label['font'] = self.ft
        self.ECUmultiselect_Label['fg'] = '#333333'
        self.ECUmultiselect_Label['justify'] = 'left'
        self.ECUmultiselect_Label['text'] = 'MultiSelect:'
        self.ECUmultiselect = tk.StringVar()
        self.ECUmultiselect_Entry = tk.Entry(root)
        self.ECUmultiselect_Entry['font'] = self.ft
        self.ECUmultiselect_Entry['fg'] = '#333333'
        self.ECUmultiselect_Entry['justify'] = 'left'
        self.ECUmultiselect_Entry['state'] = 'normal'
        self.ECUmultiselect_Entry['textvariable'] = self.ECUmultiselect
        self.ECUmultiselect_Entry.bind('<Return>', self.ecumultiselect_entry)
        self.ECUmultiselect_Entry.bind('<FocusOut>', self.ecumultiselect_entry)
        self.curecus = []
        self.curecus_backup = []
        self.ECUmultiselect_Button = tk.Button(root)
        self.ECUmultiselect_Button['font'] = self.ft
        self.ECUmultiselect_Button['fg'] = '#333333'
        self.ECUmultiselect_Button['bg'] = self.button_bg
        self.ECUmultiselect_Button['justify'] = 'left'
        self.ECUmultiselect_Button['text'] = ' + '
        self.ECUmultiselect_Button['command'] = self.ecumultiselect_button
        self.SIDID_Button = tk.Button(root)
        self.SIDID_Button['font'] = self.ft
        self.SIDID_Button['fg'] = '#333333'
        self.SIDID_Button['bg'] = self.button_bg
        self.SIDID_Button['justify'] = 'left'
        self.SIDID_Button['text'] = 'Standard Identification DIDs'
        self.SIDID_Button['command'] = self.sidid_button
        self.sididtuple = ('All')
        self.SIDID_Combobox = ttk.Combobox(root)
        self.SIDID_Combobox['state'] = 'disabled'
        self.SIDID_Combobox['font'] = self.ft
        self.SIDID_Combobox['justify'] = 'left'
        self.SIDID_Combobox['value'] = self.sididtuple
        self.SIDID_Combobox.current(0)
        self.SIDIDmultiselect = tk.StringVar()
        self.SIDIDmultiselect_Entry = tk.Entry(root)
        self.SIDIDmultiselect_Entry['font'] = self.ft
        self.SIDIDmultiselect_Entry['fg'] = '#333333'
        self.SIDIDmultiselect_Entry['justify'] = 'left'
        self.SIDIDmultiselect_Entry['state'] = 'normal'
        self.SIDIDmultiselect_Entry['textvariable'] = self.SIDIDmultiselect
        self.SIDIDmultiselect_Entry.bind('<Return>', self.sididmultiselect_entry)
        self.SIDIDmultiselect_Entry.bind('<FocusOut>', self.sididmultiselect_entry)
        self.cursidids = []
        self.cursidids_backup = []
        self.SIDIDmultiselect_Button = tk.Button(root)
        self.SIDIDmultiselect_Button['font'] = self.ft
        self.SIDIDmultiselect_Button['fg'] = '#333333'
        self.SIDIDmultiselect_Button['bg'] = self.button_bg
        self.SIDIDmultiselect_Button['justify'] = 'left'
        self.SIDIDmultiselect_Button['text'] = ' + '
        self.SIDIDmultiselect_Button['command'] = self.sididmultiselect_button
        self.DTC_Button = tk.Button(root)
        self.DTC_Button['font'] = self.ft
        self.DTC_Button['fg'] = '#333333'
        self.DTC_Button['bg'] = self.button_bg
        self.DTC_Button['justify'] = 'left'
        self.DTC_Button['text'] = 'Read DTCs'
        self.DTC_Button['command'] = self.dtc_button
        dtctuple = ('All DTCs', 'testFailed', 'testFailedThisOperationCycle', 'pendingDTC',
                    'confirmedDTC', 'testNotCompletedSinceLastClear', 'testFailedSinceLastClear',
                    'testNotCompletedThisOperationCycle', 'warningIndicatorRequested')
        self.DTC_Combobox = ttk.Combobox(root)
        self.DTC_Combobox['state'] = 'normal'
        self.DTC_Combobox['font'] = self.ft
        self.DTC_Combobox['justify'] = 'left'
        self.DTC_Combobox['value'] = dtctuple
        self.DTC_Combobox.current(0)
        self.ECD_Button = tk.Button(root)
        self.ECD_Button['font'] = self.ft
        self.ECD_Button['fg'] = '#333333'
        self.ECD_Button['bg'] = self.button_bg
        self.ECD_Button['justify'] = 'left'
        self.ECD_Button['text'] = 'ECU Configuration DIDs'
        self.ECD_Button['command'] = self.ecd_button
        ecddidtuple = 'All'
        self.ECDDID_Combobox = ttk.Combobox(root)
        self.ECDDID_Combobox['state'] = 'disabled'
        self.ECDDID_Combobox['font'] = self.ft
        self.ECDDID_Combobox['justify'] = 'left'
        self.ECDDID_Combobox['value'] = ecddidtuple
        self.ECDDID_Combobox.current(0)
        self.ECDDIDmultiselect = tk.StringVar()
        self.ECDDIDmultiselect_Entry = tk.Entry(root)
        self.ECDDIDmultiselect_Entry['font'] = self.ft
        self.ECDDIDmultiselect_Entry['fg'] = '#333333'
        self.ECDDIDmultiselect_Entry['justify'] = 'left'
        self.ECDDIDmultiselect_Entry['state'] = 'normal'
        self.ECDDIDmultiselect_Entry['textvariable'] = self.ECDDIDmultiselect
        self.ECDDIDmultiselect_Entry.bind('<Return>', self.ecddidmultiselect_entry)
        self.ECDDIDmultiselect_Entry.bind('<FocusOut>', self.ecddidmultiselect_entry)
        self.curecddids = []
        self.curecddids_backup = []
        self.ECDDIDmultiselect_Button = tk.Button(root)
        self.ECDDIDmultiselect_Button['font'] = self.ft
        self.ECDDIDmultiselect_Button['fg'] = '#333333'
        self.ECDDIDmultiselect_Button['bg'] = self.button_bg
        self.ECDDIDmultiselect_Button['justify'] = 'left'
        self.ECDDIDmultiselect_Button['text'] = ' + '
        self.ECDDIDmultiselect_Button['command'] = self.ecddidmultiselect_button
        self.VersionRecord_Button = tk.Button(root)
        self.VersionRecord_Button['font'] = self.ft
        self.VersionRecord_Button['fg'] = '#333333'
        self.VersionRecord_Button['bg'] = self.button_bg
        self.VersionRecord_Button['justify'] = 'left'
        self.VersionRecord_Button['text'] = 'SW Record'
        self.VersionRecord_Button['command'] = self.version_record
        self.VersionRecord_Button2 = tk.Button(root)
        self.VersionRecord_Button2['font'] = self.ft
        self.VersionRecord_Button2['fg'] = '#333333'
        self.VersionRecord_Button2['bg'] = self.button_bg
        self.VersionRecord_Button2['justify'] = 'left'
        self.VersionRecord_Button2['text'] = 'SW Change Record'
        self.VersionRecord_Button2['command'] = self.swchange_record
        self.Save_Button = tk.Button(root)
        self.Save_Button['font'] = self.ft
        self.Save_Button['fg'] = '#333333'
        self.Save_Button['bg'] = self.button_bg
        self.Save_Button['justify'] = 'left'
        self.Save_Button['text'] = 'Save'
        self.Save_Button['command'] = self.save_as_excel
        self.Clearresult_Button = tk.Button(root)
        self.Clearresult_Button['font'] = self.ft
        self.Clearresult_Button['fg'] = '#333333'
        self.Clearresult_Button['bg'] = self.button_bg
        self.Clearresult_Button['justify'] = 'left'
        self.Clearresult_Button['text'] = 'Clear'
        self.Clearresult_Button['command'] = self.clean_sheet
        self.Sendtome_Button = tk.Button(root)
        self.Sendtome_Button['font'] = self.ft
        self.Sendtome_Button['bg'] = self.button_bg
        self.Sendtome_Button['justify'] = 'left'
        self.Sendtome_Button['text'] = 'Report Bugs'
        self.Sendtome_Button['command'] = self.sendtome
        self.Bomchecktype = tk.StringVar()
        self.rb1 = tk.Radiobutton(root, text='No GPIRS DATA Available', variable=(self.Bomchecktype), value=0, command=(self.on_select))
        self.rb2 = tk.Radiobutton(root, text='M1/VP Sign Off with GPIRS Schedule', variable=(self.Bomchecktype), value=1, command=(self.on_select))
        self.rb1.select()
        self.VN_Label = tk.Label(root)
        self.VN_Label['font'] = self.ft
        self.VN_Label['fg'] = '#333333'
        self.VN_Label['justify'] = 'left'
        self.VN_Label['text'] = 'Vehicle Number:'
        self.Vehiclenumber = tk.StringVar()
        self.VN_Entry = tk.Entry(root)
        self.VN_Entry['font'] = self.ft
        self.VN_Entry['fg'] = '#333333'
        self.VN_Entry['justify'] = 'left'
        self.VN_Entry['state'] = 'normal'
        self.VN_Entry['textvariable'] = self.Vehiclenumber
        self.FuzzySearch_value = tk.StringVar()
        self.FuzzySearch_Entry = tk.Entry(root)
        self.FuzzySearch_Entry['font'] = self.ft
        self.FuzzySearch_Entry['fg'] = '#333333'
        self.FuzzySearch_Entry['justify'] = 'left'
        self.FuzzySearch_Entry['state'] = 'normal'
        self.FuzzySearch_Entry['textvariable'] = self.FuzzySearch_value
        self.FuzzySearch_Entry.bind('<Return>', self.fuzzysearch)
        self.FuzzySearch_Button = tk.Button(root)
        self.FuzzySearch_Button['font'] = self.ft
        self.FuzzySearch_Button['fg'] = '#333333'
        self.FuzzySearch_Button['bg'] = self.button_bg
        self.FuzzySearch_Button['justify'] = 'left'
        self.FuzzySearch_Button['text'] = 'Search'
        self.FuzzySearch_Button['command'] = self.fuzzysearch
        self.Searchtype = tk.StringVar()
        self.Searchtyperb1 = tk.Radiobutton(root, text='', variable=(self.Searchtype), value=0)
        self.Searchtyperb2 = tk.Radiobutton(root, text='', variable=(self.Searchtype), value=1)
        self.Searchtyperb3 = tk.Radiobutton(root, text='', variable=(self.Searchtype), value=2)
        self.Searchtyperb3.select()
        self.Match_Count_Label = tk.Label(root)
        self.Match_Count_Label['font'] = self.ft
        self.Match_Count_Label['fg'] = '#333333'
        self.Match_Count_Label['justify'] = 'left'
        self.Match_Count_Label['text'] = ''
        self.Previous_Button = tk.Button(root)
        self.Previous_Button['font'] = self.ft
        self.Previous_Button['fg'] = '#333333'
        self.Previous_Button['bg'] = self.button_bg
        self.Previous_Button['justify'] = 'left'
        self.Previous_Button['text'] = ' < '
        self.Previous_Button['command'] = self.select_prev
        self.Next_Button = tk.Button(root)
        self.Next_Button['font'] = self.ft
        self.Next_Button['fg'] = '#333333'
        self.Next_Button['bg'] = self.button_bg
        self.Next_Button['justify'] = 'left'
        self.Next_Button['text'] = ' > '
        self.Next_Button['command'] = self.select_next
        self.curcommand = 0
        self.match_count = 0
        self.current_match = 0
        self.show_layout1()

        if self.githubinfo['info'][0] == 2:
            messagebox.showinfo(self.githubinfo['info'][2][0], self.githubinfo['info'][2][1])
        elif self.curver < self.githubinfo['curver']:
            if self.curver in self.githubinfo['supver']:
                if self.githubinfo['info'][0] == 0 or self.githubinfo['info'][0] == 10:
                    messagebox.showinfo('New Version released', 'New Version of Bus Query File Reader is released. Please visit official Sharepoint and download the latest version!')
                else:
                    newfeature = ''
                    for i in range(len(self.githubinfo['info'][1])):
                        newfeature += str(i + 1) + '. ' + self.githubinfo['info'][1][i] + '\n'

                    popupmessage = 'New Version of Bus Query File Reader is released. Please visit official Sharepoint and download the latest version!\n Update Infos:\n' + newfeature
                    messagebox.showinfo('New Version released', popupmessage)
            else:
                if self.curver not in self.githubinfo['supver']:
                    # messagebox.showerror('Version Update needed', 'Please visit official Sharepoint and update to the latest version.')
                    # webbrowser.open('https://azureford.sharepoint.com/sites/bqreader')
                    self.select_update()
                    self.root.after(20000, self.root.destroy)
        if self.curver < self.githubinfo['curver']:
            self.Update_Button.place(relx=1,x=-280,y=10,height=20)

        root.wm_attributes('-alpha', 1.0)

    def show_layout1(self):
        self.switch_button1['bg'] = self.button_selected_bg
        self.switch_button2['bg'] = self.button_unselected_bg
        self.switch_button3['bg'] = self.button_unselected_bg
        self.switch_button1.place(x=5, y=10, height=20)
        self.switch_button2.place(x=170, y=10, height=20)
        self.switch_button3.place(x=350, y=10, height=20)
        self.Filepath_Label.place(x=5, y=35, height=20)
        self.Time_Label.place(x=270, y=35, height=20)
        self.ECU_Label.place(x=433, y=35, height=20)
        self.Filepath_Entry.place(x=120, y=35, width=130, height=20)
        self.Filepath_Button.place(x=255, y=35, width=15, height=20)
        self.ECUselect_Combobox.place(relx=1, x=(-230), y=35, width=220, height=23)
        self.ECUselect_Label.place(relx=1, x=(-300), y=35, width=60, height=20)
        self.ECUmultiselect_Label.place(relx=1, x=(-310), y=60, width=80, height=20)
        self.ECUmultiselect_Entry.place(relx=1, x=(-230), y=60, width=190, height=20)
        self.ECUmultiselect_Button.place(relx=1, x=(-30), y=60, height=20)
        self.SIDID_Button.place(x=5, y=85, width=155, height=20)
        self.SIDID_Combobox.place(x=165, y=83.5, width=55, height=23)
        self.SIDIDmultiselect_Entry.place(x=5, y=110, width=190, height=20)
        self.SIDIDmultiselect_Button.place(x=200, y=110, height=20)
        self.DTC_Button.place(x=230, y=85, width=70, height=20)
        self.DTC_Combobox.place(x=230, y=108.5, width=150, height=23)
        self.ECD_Button.place(x=390, y=85, width=135, height=20)
        self.ECDDID_Combobox.place(x=530, y=83.5, width=55, height=23)
        self.ECDDIDmultiselect_Entry.place(x=390, y=110, width=170, height=20)
        self.ECDDIDmultiselect_Button.place(x=565, y=110, height=20)
        self.VersionRecord_Button2.place(x=85, y=60, height=20)
        self.VersionRecord_Button.place(x=5, y=60, height=20)
        self.Save_Button.place(relx=1, x=(-45), y=110, height=20)
        self.Clearresult_Button.place(relx=1, x=(-45), y=85, height=20)
        self.Sendtome_Button.place(relx=1, x=(-80), y=10, height=20)
        self.Website_Button.place(relx=1, x=(-147), y=10, height=20)
        self.FuzzySearch_Entry.place(x=600, y=110, width=70, height=20)
        self.FuzzySearch_Button.place(x=675, y=110, height=20)
        self.Match_Count_Label.place(x=640, y=85, height=20)
        self.Previous_Button.place(x=610, y=85, height=20)
        self.Next_Button.place(x=680, y=85, height=20)
        self.runstatus = 1
        self.filestickno = 1
        self.Filepath_Label2.place_forget()
        self.Time_Label2.place_forget()
        self.ECU_Label2.place_forget()
        self.Filepath_Entry2.place_forget()
        self.Filepath_Button2.place_forget()
        self.Bomcheckerpath_Label.place_forget()
        self.Bomverinfo_Label.place_forget()
        self.Filepath_Entry3.place_forget()
        self.Filepath_Button3.place_forget()
        self.rb1.place_forget()
        self.rb2.place_forget()
        self.VN_Entry.place_forget()
        self.filestickstatus()

    def show_layout2(self):
        self.switch_button1['bg'] = self.button_unselected_bg
        self.switch_button2['bg'] = self.button_selected_bg
        self.switch_button3['bg'] = self.button_unselected_bg
        self.Filepath_Label.place(x=5, y=35, height=20)
        self.Time_Label.place(x=270, y=35, height=20)
        self.ECU_Label.place(x=433, y=35, height=20)
        self.Filepath_Entry.place(x=120, y=35, width=130, height=20)
        self.Filepath_Button.place(x=255, y=35, width=15, height=20)
        self.Filepath_Label2.place(x=5, y=60, height=20)
        self.Time_Label2.place(x=270, y=60, height=20)
        self.ECU_Label2.place(x=433, y=60, height=20)
        self.Filepath_Entry2.place(x=120, y=60, width=130, height=20)
        self.Filepath_Button2.place(x=255, y=60, width=15, height=20)
        self.DTC_Button.place(x=230, y=85, width=70, height=20)
        self.DTC_Combobox.place(x=230, y=108.5, width=150, height=23)
        self.ECD_Button.place(x=390, y=85, width=135, height=20)
        self.ECDDID_Combobox.place(x=530, y=83.5, width=55, height=23)
        self.ECDDIDmultiselect_Entry.place(x=390, y=110, width=170, height=20)
        self.ECDDIDmultiselect_Button.place(x=565, y=110, height=20)
        self.FuzzySearch_Entry.place(x=600, y=110, width=70, height=20)
        self.FuzzySearch_Button.place(x=675, y=110, height=20)
        self.Match_Count_Label.place(x=640, y=85, height=20)
        self.Previous_Button.place(x=610, y=85, height=20)
        self.Next_Button.place(x=680, y=85, height=20)
        self.Bomcheckerpath_Label.place_forget()
        self.Bomverinfo_Label.place_forget()
        self.Filepath_Entry3.place_forget()
        self.Filepath_Button3.place_forget()
        self.VersionRecord_Button.place_forget()
        self.VersionRecord_Button2.place_forget()
        self.rb1.place_forget()
        self.rb2.place_forget()
        self.VN_Entry.place_forget()
        self.filestickno = 3
        self.runstatus = 3
        self.filestickstatus()

    def show_layout3(self):
        self.switch_button1['bg'] = self.button_unselected_bg
        self.switch_button2['bg'] = self.button_unselected_bg
        self.switch_button3['bg'] = self.button_selected_bg
        self.Filepath_Label.place(x=5, y=35, height=20)
        self.Time_Label.place(x=270, y=35, height=20)
        self.ECU_Label.place(x=433, y=35, height=20)
        self.Filepath_Entry.place(x=120, y=35, width=130, height=20)
        self.Filepath_Button.place(x=255, y=35, width=15, height=20)
        self.Bomcheckerpath_Label.place(x=5, y=60, height=20)
        self.Bomverinfo_Label.place(x=270, y=60, height=20)
        self.Filepath_Entry3.place(x=120, y=60, width=130, height=20)
        self.Filepath_Button3.place(x=255, y=60, width=15, height=20)
        self.rb1.place(x=240, y=85)
        self.rb2.place(x=240, y=110)
        self.VN_Entry.place(x=460, y=110, width=120)
        self.Filepath_Label2.place_forget()
        self.Time_Label2.place_forget()
        self.ECU_Label2.place_forget()
        self.Filepath_Entry2.place_forget()
        self.Filepath_Button2.place_forget()
        self.DTC_Button.place_forget()
        self.DTC_Combobox.place_forget()
        self.ECD_Button.place_forget()
        self.ECDDID_Combobox.place_forget()
        self.ECDDIDmultiselect_Entry.place_forget()
        self.ECDDIDmultiselect_Button.place_forget()
        self.VersionRecord_Button.place_forget()
        self.VersionRecord_Button2.place_forget()
        self.FuzzySearch_Button.place_forget()
        self.FuzzySearch_Entry.place_forget()
        self.Match_Count_Label.place_forget()
        self.Previous_Button.place_forget()
        self.Next_Button.place_forget()
        self.filestickno = 4
        self.runstatus = 4
        self.filestickstatus()

    def version_record(self):
        verinfo = {}
        if 'ecus' in self.bqinfo:
            for ecu in self.bqinfo['ecus'].keys():
                verinfo[ecu] = []
                if 'sidid' in self.bqinfo['ecus'][ecu]:
                    if 'F188' in self.bqinfo['ecus'][ecu]['sidid']:
                        verinfo[ecu].append(self.bqinfo['ecus'][ecu]['sidid']['F188'][1][1])
                    else:
                        verinfo[ecu].append('-')
                    if 'F10A' in self.bqinfo['ecus'][ecu]['sidid']:
                        verinfo[ecu].append(self.bqinfo['ecus'][ecu]['sidid']['F10A'][1][1])
                    else:
                        verinfo[ecu].append('-')
                else:
                    verinfo[ecu] = ['-','-']
        save_path = filedialog.asksaveasfilename(title='save to', defaultextension='.xlsx', filetypes=[('Excel Workbook', '*.xlsx')])
        try:
            record2excel(verinfo, self.bqinfo['date'] + ' ' + self.bqinfo['time'], save_path)
            messagebox.showinfo('Record SW info Successfully', 'The SW Record File is generated successfully!')
        except:
            messagebox.showerror('Error', "Failure when trying to generate the record. Please close the record file if it's running and try again.")

    def swchange_record(self):
        verinfo = {}
        if 'ecus' in self.bqinfo:
            for ecu in self.bqinfo['ecus'].keys():
                verinfo[ecu] = []
                if 'sidid' in self.bqinfo['ecus'][ecu]:
                    if 'F188' in self.bqinfo['ecus'][ecu]['sidid']:
                        verinfo[ecu].append(self.bqinfo['ecus'][ecu]['sidid']['F188'][1][1])
                    else:
                        verinfo[ecu].append('-')
                    if 'F10A' in self.bqinfo['ecus'][ecu]['sidid']:
                        verinfo[ecu].append(self.bqinfo['ecus'][ecu]['sidid']['F10A'][1][1])
                    else:
                        verinfo[ecu].append('-')
                else:
                    verinfo[ecu] = ['-','-']
        path_ = askopenfilename()
        try:
            updaterecord(verinfo, self.bqinfo['date'] + ' ' + self.bqinfo['time'], path_)
            messagebox.showinfo('Updated Successfully', 'The SW Change Record File is updated successfully!')
        except:
            messagebox.showerror('Error', "Failure when trying to update the record. Please close the record file if it's running and try again.")

        return 0

    def filepath_entry(self, event=None):
        self.bqinfo1 = {}
        self.bqinfo1 = read_bq(self.filepath.get())
        self.DateTime.set(self.bqinfo1['date'] + ' ' + self.bqinfo1['time'])
        self.ECUno.set(str(len(self.bqinfo1['ecus'])) + ' ECU(s)')
        self.filestickstatus()
        return 'break'

    def filepath_button(self):
        path_ = askopenfilename()
        self.filepath.set(path_)
        self.filepath_entry()
        return 0

    def filepath_entry2(self, event=None):
        self.bqinfo2 = {}
        self.bqinfo2 = read_bq(self.filepath2.get())
        self.DateTime2.set(self.bqinfo2['date'] + ' ' + self.bqinfo2['time'])
        self.ECUno2.set(str(len(self.bqinfo2['ecus'])) + ' ECU(s)')
        self.filestickstatus()
        return 'break'

    def filepath_button2(self):
        path_ = askopenfilename()
        self.filepath2.set(path_)
        self.filepath_entry2()
        return 0

    def filepath_entry3(self, event=None):
        self.bominfo = {}
        self.bomver = ''
        self.bominfo, self.bomver = readswbom(self.filepath3.get())
        self.Bomverinfo.set(self.bomver)
        self.filestickstatus()
        return 'break'

    def filepath_button3(self):
        path_ = askopenfilename()
        self.filepath3.set(path_)
        self.filepath_entry3()
        return 0

    def WindowResize(self, event=None):
        new_width = self.root.winfo_width()
        new_height = self.root.winfo_height()
        if new_width == 1:
            if new_height == 1:
                return
        if self.save_width != new_width or self.save_height != new_height:
            self.frame4.config(width=(new_width - 10), height=(new_height - 140))
        self.save_width = new_width
        self.save_height = new_height

    def filestickstatus(self):
        if self.filestickno == 1:
            self.bqinfo = copy.deepcopy(self.bqinfo1)
            self.curecus = []
            self.cursidids = []
            self.curecddids = []
            self.updateinfo()
            self.runstatus = 1
            return 1
        else:
            if self.filestickno == 3:
                self.bqinfo = copy.deepcopy(self.bqinfo1)
                self.dicMeg(self.bqinfo, self.bqinfo2)
                self.curecus = []
                self.cursidids = []
                self.curecddids = []
                self.updateinfo()
                self.runstatus = 3
                return 3
            if self.filestickno == 4:
                self.bqinfo = copy.deepcopy(self.bqinfo1)
                self.curecus = []
                self.cursidids = []
                self.curecddids = []
                self.updateinfo()
                self.runstatus = 4
                return 4
            return 0

    def on_drop(self, event):
        curpath = event.data
        if curpath[0] == '{':
            curpath = curpath[1:-1]
        if self.filestickno == 1:
            self.filepath.set(curpath)
            self.filepath_entry()
        else:
            if self.filestickno == 3:
                self.select_filepath(curpath)
            elif self.filestickno == 4:
                if 'rtf' in curpath:
                    self.filepath.set(curpath)
                    self.filepath_entry()
                elif 'xlsm' in curpath:
                    self.filepath3.set(curpath)
                    self.filepath_entry3()

    def select_filepath(self, curpath):

        def select_para_1():
            self.filepath.set(curpath)
            popup_window.destroy()
            self.filepath_entry()

        def select_para_2():
            self.filepath2.set(curpath)
            popup_window.destroy()
            self.filepath_entry2()

        popup_window = tk.Toplevel(root)
        popup_window.title('Please Select')
        tmpimg = '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'
        with open('tmp.ico', 'wb') as (tmp):
            tmp.write(base64.b64decode(tmpimg))
        popup_window.wm_iconbitmap('tmp.ico')
        os.remove('tmp.ico')
        popup_window.wm_attributes('-alpha', 0.0)
        popup_window.geometry('300x50')
        popup_window.wm_attributes('-alpha', 1.0)
        popup_window.resizable(width=False, height=False)
        popup_label = tk.Label(popup_window, text='Which BusQuery you want to select this one as?')
        popup_button1 = tk.Button(popup_window, text='1st BusQuery File', command=select_para_1)
        popup_button2 = tk.Button(popup_window, text='2nd BusQuery File', command=select_para_2)
        popup_label.pack()
        popup_button1.pack(side='left')
        popup_button2.pack(side='right')
        x = root.winfo_rootx() + root.winfo_width() // 2 - 150
        y = root.winfo_rooty() + root.winfo_height() // 2 - 25
        popup_window.geometry('+{}+{}'.format(x, y))

    def updateinfo(self):
        if self.runstatus != 4:
            self.ecustmp = []
            tmp = [
             'All Modules']
            if 'ecus' in self.bqinfo:
                for ecu in self.bqinfo['ecus'].keys():
                    self.ecustmp.append(ecu)
                    tmp.append('0x' + ecu + ' ' + self.ecunamedic[ecu])

            self.ECUselect_Combobox['value'] = tuple(tmp)
            self.ECUselect_Combobox.current(0)
            self.curecu = '000'
            self.curecus = []
            self.updateselection()
            self.SIDID_Combobox.current(0)
            self.ECUmultiselect.set('')
            self.SIDIDmultiselect.set('')
        else:
            tmp = [
             'All Modules']
            self.ecustmp = []
            for ecu in self.bominfo.keys():
                self.ecustmp.append(ecu)
                tmp.append('0x' + ecu + ' ' + self.ecunamedic[ecu])

            self.ECUselect_Combobox['value'] = tuple(tmp)
            self.ECUselect_Combobox.current(0)
            self.curecu = '000'
            self.curecus = []
            self.updateselection()
            self.SIDID_Combobox.current(0)
            self.ECUmultiselect.set('')
            self.SIDIDmultiselect.set('')
        return 0

    def ecuselct_combobox(self, event=None):
        if self.ECUselect_Combobox.current() != 0:
            self.curecu = self.ECUselect_Combobox.get()[2:5]
            if self.ECUmultiselect_Entry.get() == '':
                self.curecus = []
        if self.ECUselect_Combobox.current() == 0:
            if self.ECUmultiselect_Entry.get() == '':
                self.curecus = []
                for ecuid in list(self.ECUselect_Combobox['value'])[1:]:
                    self.curecus.append(ecuid[2:5])

        self.updateselection()
        return 0

    def ecumultiselect_entry(self, event=None):
        self.curecus = self.ECUmultiselect.get().split(',')
        if '' in self.curecus:
            self.curecus.remove('')
        for ecu in self.curecus:
            if ecu not in self.ecustmp:
                self.ECUmultiselect.set(self.curecus2str(ecus=(self.curecus_backup)))
                self.curecus = self.curecus_backup.copy()
                messagebox.showinfo('ERROR', 'Inputted format error or inputted module not in file')
                return 0

        self.curecus_backup = self.curecus.copy()
        self.updateselection()
        return 1

    def ecumultiselect_button(self):
        self.ecumultiselect_entry(self)
        if self.ECUselect_Combobox.current() != 0:
            if self.ECUselect_Combobox.get()[2:5] not in self.curecus:
                self.curecus.append(self.ECUselect_Combobox.get()[2:5])
            self.ECUmultiselect.set(self.curecus2str(ecus=(self.curecus)))
            self.curecus_backup = self.curecus.copy()
        else:
            self.curecus = []
            for ecuid in list(self.ECUselect_Combobox['value'])[1:]:
                self.curecus.append(ecuid[2:5])

            self.ECUmultiselect.set(self.curecus2str(ecus=(self.curecus)))
            self.curecus_backup = self.curecus.copy()

    def sididmultiselect_entry(self, event=None):
        self.cursidids = self.SIDIDmultiselect.get().split(',')
        if '' in self.cursidids:
            self.cursidids.remove('')
        for did in self.cursidids:
            if did not in self.SIDID_Combobox['value']:
                self.SIDIDmultiselect.set(self.curecus2str(ecus=(self.cursidids_backup)))
                self.cursidids = self.cursidids_backup.copy()
                messagebox.showinfo('ERROR', 'Inputted format error or inputted dids not in file')
                return 0

        self.cursidids_backup = self.cursidids.copy()
        return 1

    def sididmultiselect_button(self):
        self.ecddidmultiselect_entry()
        if self.SIDID_Combobox.get() == 'All':
            self.cursidids = list(self.SIDID_Combobox['value'])[1:]
        else:
            if self.SIDID_Combobox.get() not in self.cursidids:
                self.cursidids.append(self.SIDID_Combobox.get())
        self.SIDIDmultiselect.set(self.curecus2str(ecus=(self.cursidids)))
        self.cursidids_backup = self.cursidids.copy()

    def ecddidmultiselect_entry(self, event=None):
        self.curecddids = self.ECDDIDmultiselect.get().split(',')
        if '' in self.curecddids:
            self.curecddids.remove('')
        for did in self.curecddids:
            if did not in self.ECDDID_Combobox['value']:
                self.ECDDIDmultiselect.set(self.curecus2str(ecus=(self.curecddids_backup)))
                self.curecddids = self.curecddids_backup.copy()
                messagebox.showinfo('ERROR', 'Inputted format error or inputted dids not in file')
                return 0

        self.cursidids_backup = self.cursidids.copy()
        return 0

    def ecddidmultiselect_button(self):
        self.ecddidmultiselect_entry()
        if self.ECDDID_Combobox.get() == 'All':
            self.curecddids = list(self.ECDDID_Combobox['value'])[1:]
        else:
            if self.ECDDID_Combobox.get() not in self.curecddids:
                self.curecddids.append(self.ECDDID_Combobox.get())
        self.ECDDIDmultiselect.set(self.curecus2str(ecus=(self.curecddids)))
        self.curecddids_backup = self.curecddids.copy()
        return 0

    def sendtome(self):
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = 'nliu47@ford.com'
        mail.Cc = 'DWANG90@ford.com;JLI220@ford.com'
        mail.Subject = 'Issues about BusQuery reader'
        mail.Body = 'My Bus Query File Reader version is: ' + str(self.curver) + '. I find problems or have some suggestions about Bus Query File Reader:'
        if self.filepath.get() != '':
            mail.Attachments.Add(self.filepath.get())
        if self.filepath2.get() != '':
            mail.Attachments.Add(self.filepath2.get())
        if self.filepath3.get() != '':
            mail.Attachments.Add(self.filepath3.get())
        mail.Display(True)

    def updateselection(self):
        if self.runstatus != 4:
            tmplist = [
             'All']
            tmpecdlist = ['All']
            if self.curecus == []:
                if self.ECUselect_Combobox.current() != 0:
                    if self.bqinfo['ecus'][self.curecu]['status'] == 'Success':
                        if 'sidid' in self.bqinfo['ecus'][self.curecu]:
                            for key in self.bqinfo['ecus'][self.curecu]['sidid']:
                                if key not in tmplist:
                                    tmplist.append(key)

                        if 'ecds' in self.bqinfo['ecus'][self.curecu]:
                            for key in self.bqinfo['ecus'][self.curecu]['ecds']:
                                if key not in tmpecdlist and key != 'numbers':
                                    tmpecdlist.append(key)

                else:
                    for ecuid in list(self.ECUselect_Combobox['value'])[1:]:
                        self.curecus.append(ecuid[2:5])

                    for ecuid in self.curecus:
                        if self.bqinfo['ecus'][ecuid]['status'] == 'Success':
                            if 'sidid' in self.bqinfo['ecus'][ecuid]:
                                for key in self.bqinfo['ecus'][ecuid]['sidid']:
                                    if key not in tmplist:
                                        tmplist.append(key)

                            if 'ecds' in self.bqinfo['ecus'][ecuid]:
                                for key in self.bqinfo['ecus'][ecuid]['ecds']:
                                    if key not in tmpecdlist and key != 'numbers':
                                        tmpecdlist.append(key)
            else:
                for ecuid in self.curecus:
                    if self.bqinfo['ecus'][ecuid]['status'] == 'Success':
                        if 'sidid' in self.bqinfo['ecus'][ecuid]:
                            for key in self.bqinfo['ecus'][ecuid]['sidid']:
                                if key not in tmplist:
                                    tmplist.append(key)

                        if 'ecds' in self.bqinfo['ecus'][ecuid]:
                            for key in self.bqinfo['ecus'][ecuid]['ecds']:
                                if key not in tmpecdlist and key != 'numbers':
                                    tmpecdlist.append(key)
            self.SIDID_Combobox['value'] = tuple(tmplist)
            self.SIDID_Combobox['state'] = 'normal'
            self.ECDDID_Combobox['value'] = tuple(tmpecdlist)
            self.ECDDID_Combobox['state'] = 'normal'
        else:
            tmplist = [
             'All']
            if self.curecus == []:
                if self.ECUselect_Combobox.current() != 0:
                    for key in self.bominfo[self.curecu].keys():
                        if key not in tmplist:
                            tmplist.append(key)

                else:
                    if self.ECUselect_Combobox.current() == 0:
                        if self.curecus == []:
                            for ecuid in list(self.ECUselect_Combobox['value'])[1:]:
                                self.curecus.append(ecuid[2:5])

                        for ecuid in self.curecus:
                            for key in self.bominfo[ecuid].keys():
                                if key not in tmplist:
                                    tmplist.append(key)

                self.SIDID_Combobox['value'] = tuple(tmplist)
                self.SIDID_Combobox['state'] = 'normal'
        return 0

    def curecus2str(self, ecus):
        return ','.join(str(ecu) for ecu in ecus)

    def dicMeg(self, dic1, dic2):
        for i in dic2:
            if i in dic1:
                if type(dic1[i]) is dict:
                    if type(dic2[i]) is dict:
                        self.dicMeg(dic1[i], dic2[i])
            else:
                if isinstance(dic2[i], str):
                    dic1[i] = dic2[i]
                else:
                    dic1[i] = copy.deepcopy(dic2[i])

        return 0

    def sidid_button(self):
        if self.runstatus != 4:
            self.curcommand = 1
            self.clean_sheet()
            self.ecumultiselect_entry()
            self.sididmultiselect_entry()
            if self.cursidids == []:
                if self.SIDID_Combobox.get() == 'All':
                    tmpsidids = list(self.SIDID_Combobox['value'])[1:]
                else:
                    tmpsidids = [
                     self.SIDID_Combobox.get()]
            else:
                tmpsidids = self.cursidids.copy()
            if self.curecus == []:
                if self.ECUselect_Combobox.current() != 0:
                    tmpecus = [self.ECUselect_Combobox.get()[2:5]]
                else:
                    tmpecus = []
                    for ecuid in list(self.ECUselect_Combobox['value'])[1:]:
                        tmpecus.append(ecuid[2:5])
            else:
                tmpecus = self.curecus.copy()
        if self.runstatus == 1 or self.runstatus == 2:
            tmpinfo = sididlist(self.bqinfo, tmpecus, tmpsidids)
            self.Result_Sheet['columns'] = ('DID', 'Description', 'Value')
            self.Result_Sheet.column('#0', width=150, stretch=False)
            self.Result_Sheet.column('DID', width=80, anchor='w')
            self.Result_Sheet.column('Description', width=250, anchor='w')
            self.Result_Sheet.column('Value', width=350, anchor='w')
            self.Result_Sheet.heading('DID', text='DID', anchor='w')
            self.Result_Sheet.heading('Description', text='Description', anchor='w')
            self.Result_Sheet.heading('Value', text='Value', anchor='w')
            for ecu, ecuinfos in tmpinfo.items():
                st = self.ecunamedic[ecu].index('[')
                en = self.ecunamedic[ecu].index(']')
                ecu_item = self.Result_Sheet.insert('', (tk.END), text=('0x' + ecu + ' ' + self.ecunamedic[ecu][st + 1:en]), open=True, values=())
                self.Result_Sheet.item(ecu_item, tags=('newecu', ))
                for did, description, value, status in ecuinfos:
                    item = self.Result_Sheet.insert(ecu_item, (tk.END), values=(did, description, value))
                    if status == 1:
                        self.Result_Sheet.item(item, tags=('invalid', ))
                    else:
                        if status == 2:
                            self.Result_Sheet.item(item, tags=('error', ))
                        else:
                            if status == 3:
                                self.Result_Sheet.item(item, tags=('invalid', ))
                            else:
                                if status == 4:
                                    self.Result_Sheet.item(item, tags=('unexpected', ))
                                elif status == 0:
                                    self.Result_Sheet.item(item, tags=('normal', ))

            self.Result_Sheet.tag_configure('invalid', background='orange')
            self.Result_Sheet.tag_configure('error', background='salmon')
            self.Result_Sheet.tag_configure('unexpected', background='gray')
            self.Result_Sheet.tag_configure('newecu', background='lightblue')
            self.Result_Sheet.tag_configure('normal', background='yellowgreen')
        else:
            if self.runstatus == 3:
                tmpinfo = comparesidid(self.bqinfo1, self.bqinfo2, tmpecus, tmpsidids)
                self.Result_Sheet['columns'] = ('DID', 'Description', '1st BusQuery',
                                                '2nd BusQuery')
                self.Result_Sheet.column('#0', width=100, stretch=False)
                self.Result_Sheet.column('DID', width=50, anchor='w')
                self.Result_Sheet.column('Description', width=180, anchor='w')
                self.Result_Sheet.column('1st BusQuery', width=250, anchor='w')
                self.Result_Sheet.column('2nd BusQuery', width=250, anchor='w')
                self.Result_Sheet.heading('DID', text='DID', anchor='w')
                self.Result_Sheet.heading('Description', text='Description', anchor='w')
                self.Result_Sheet.heading('1st BusQuery', text='1st BusQuery', anchor='w')
                self.Result_Sheet.heading('2nd BusQuery', text='2nd BusQuery', anchor='w')
                for ecu, ecuinfos in tmpinfo.items():
                    st = self.ecunamedic[ecu].index('[')
                    en = self.ecunamedic[ecu].index(']')
                    ecu_item = self.Result_Sheet.insert('', (tk.END), text=('0x' + ecu + ' ' + self.ecunamedic[ecu][st + 1:en]), open=True, values=())
                    self.Result_Sheet.item(ecu_item, tags=('newecu', ))
                    for did, description, value1, value2, status1, status2, compareres in ecuinfos:
                        item = self.Result_Sheet.insert(ecu_item, (tk.END), values=(did, description, value1, value2))
                        if compareres == 0:
                            self.Result_Sheet.item(item, tags=('different', ))
                        elif status1 == 0 and status2 == 0:
                            self.Result_Sheet.item(item, tags=('normal', ))
                        else:
                            self.Result_Sheet.item(item, tags=('warning', ))

                self.Result_Sheet.tag_configure('warning', background='gray')
                self.Result_Sheet.tag_configure('different', background='red')
                self.Result_Sheet.tag_configure('normal', background='yellowgreen')
                self.Result_Sheet.tag_configure('newecu', background='lightblue')

            else:
                if self.Bomchecktype.get() == '0':
                    self.curcommand = 1
                    self.clean_sheet()
                    self.ecumultiselect_entry()
                    self.sididmultiselect_entry()
                    if self.cursidids == []:
                        if self.SIDID_Combobox.get() == 'All':
                            tmpsidids = list(self.SIDID_Combobox['value'])[1:]
                        else:
                            tmpsidids = [
                             self.SIDID_Combobox.get()]
                    else:
                        tmpsidids = self.cursidids.copy()
                    if self.curecus == []:
                        if self.ECUselect_Combobox.current() != 0:
                            tmpecus = [
                             self.ECUselect_Combobox.get()[2:5]]
                        else:
                            tmpecus = []
                            for ecuid in list(self.ECUselect_Combobox['value'])[1:]:
                                tmpecus.append(ecuid[2:5])

                    else:
                        tmpecus = self.curecus.copy()
                    tmpinfo = bomcompare(self.bqinfo, self.bominfo, tmpecus, tmpsidids)
                    self.Result_Sheet['columns'] = ('DID', 'Description', 'SW BomChecker',
                                                    'Bus Query File')
                    self.Result_Sheet.column('#0', width=100, stretch=False)
                    self.Result_Sheet.column('DID', width=50, anchor='w')
                    self.Result_Sheet.column('Description', width=180, anchor='w')
                    self.Result_Sheet.column('SW BomChecker', width=250, anchor='w')
                    self.Result_Sheet.column('Bus Query File', width=250, anchor='w')
                    self.Result_Sheet.heading('DID', text='DID', anchor='w')
                    self.Result_Sheet.heading('Description', text='Description', anchor='w')
                    self.Result_Sheet.heading('SW BomChecker', text='SW BomChecker', anchor='w')
                    self.Result_Sheet.heading('Bus Query File', text='Bus Query File', anchor='w')
                    for ecu, ecuinfos in tmpinfo.items():
                        st = self.ecunamedic[ecu].index('[')
                        en = self.ecunamedic[ecu].index(']')
                        ecu_item = self.Result_Sheet.insert('', (tk.END), text=('0x' + ecu + ' ' + self.ecunamedic[ecu][st + 1:en]), open=True, values=())
                        self.Result_Sheet.item(ecu_item, tags=('newecu', ))
                        for did, description, value1, value2, compareres, fcode in ecuinfos:
                            item = self.Result_Sheet.insert(ecu_item, (tk.END), values=(did, description, value1, value2))
                            if compareres == 0:
                                self.Result_Sheet.item(item, tags=('different', ))
                            else:
                                self.Result_Sheet.item(item, tags=('same', ))

                    self.Result_Sheet.tag_configure('different', background='red')
                    self.Result_Sheet.tag_configure('newecu', background='lightblue')
                    self.Result_Sheet.tag_configure('same', background='yellowgreen')
                elif self.Bomchecktype.get() == '1':
                    vnnumber = self.VN_Entry.get()
                    if vnnumber == '':
                        messagebox.showinfo('ERROR', 'Please input Vehicle Number.')
                    else:
                        featurelist = vn2featurelist(vnnumber, self.filepath3.get())
                        if featurelist == []:
                            messagebox.showinfo('ERROR', 'unknown Vehicle Number.')
                        else:
                            self.curcommand = 1
                            self.clean_sheet()
                            self.ecumultiselect_entry()
                            self.sididmultiselect_entry()
                            if self.cursidids == []:
                                if self.SIDID_Combobox.get() == 'All':
                                    tmpsidids = list(self.SIDID_Combobox['value'])[1:]
                                else:
                                    tmpsidids = [
                                     self.SIDID_Combobox.get()]
                            else:
                                tmpsidids = self.cursidids.copy()
                            if self.curecus == []:
                                if self.ECUselect_Combobox.current() != 0:
                                    tmpecus = [
                                     self.ECUselect_Combobox.get()[2:5]]
                                else:
                                    tmpecus = []
                                    for ecuid in list(self.ECUselect_Combobox['value'])[1:]:
                                        tmpecus.append(ecuid[2:5])

                            else:
                                tmpecus = self.curecus.copy()
                            tmpinfo = bomcompare(self.bqinfo, self.bominfo, tmpecus, tmpsidids)
                            self.Result_Sheet['columns'] = ('DID', 'Description', 'SW BomChecker',
                                                            'Bus Query File')
                            self.Result_Sheet.column('#0', width=100, stretch=False)
                            self.Result_Sheet.column('DID', width=50, anchor='w')
                            self.Result_Sheet.column('Description', width=180, anchor='w')
                            self.Result_Sheet.column('SW BomChecker', width=250, anchor='w')
                            self.Result_Sheet.column('Bus Query File', width=250, anchor='w')
                            self.Result_Sheet.heading('DID', text='DID', anchor='w')
                            self.Result_Sheet.heading('Description', text='Description', anchor='w')
                            self.Result_Sheet.heading('SW BomChecker', text='SW BomChecker', anchor='w')
                            self.Result_Sheet.heading('Bus Query File', text='Bus Query File', anchor='w')
                            for ecu, ecuinfos in tmpinfo.items():
                                st = self.ecunamedic[ecu].index('[')
                                en = self.ecunamedic[ecu].index(']')
                                ecu_item = self.Result_Sheet.insert('', (tk.END), text=('0x' + ecu + ' ' + self.ecunamedic[ecu][st + 1:en]), open=True, values=())
                                self.Result_Sheet.item(ecu_item, tags=('newecu', ))
                                for did, description, value1, value2, compareres, fcode in ecuinfos:
                                    if is_fit(fcode, featurelist):
                                        item = self.Result_Sheet.insert(ecu_item, (tk.END), values=(did, description, value1, value2))
                                        if compareres == 0:
                                            self.Result_Sheet.item(item, tags=('different', ))
                                        else:
                                            self.Result_Sheet.item(item, tags=('same', ))

                            self.Result_Sheet.tag_configure('different', background='red')
                            self.Result_Sheet.tag_configure('newecu', background='lightblue')
                            self.Result_Sheet.tag_configure('same', background='yellowgreen')

    def ecd_button(self):
        self.curcommand = 3
        self.clean_sheet()
        self.ecumultiselect_entry()
        self.ecddidmultiselect_entry()
        if self.curecddids == []:
            if self.ECDDID_Combobox.get() == 'All':
                tmpecdids = list(self.ECDDID_Combobox['value'])[1:]
            else:
                tmpecdids = [
                 self.ECDDID_Combobox.get()]
        else:
            tmpecdids = self.curecddids.copy()
        if self.curecus == []:
            if self.ECUselect_Combobox.current() != 0:
                tmpecus = [
                 self.ECUselect_Combobox.get()[2:5]]
            else:
                tmpecus = []
                for ecuid in list(self.ECUselect_Combobox['value'])[1:]:
                    tmpecus.append(ecuid[2:5])

        else:
            tmpecus = self.curecus.copy()
        if self.runstatus == 1 or self.runstatus == 2:
            tmpinfo = ecdlist(self.bqinfo, tmpecus, tmpecdids)
            self.Result_Sheet['columns'] = ('Description', 'Value')
            self.Result_Sheet.column('#0', width=100, stretch=False)
            self.Result_Sheet.column('Description', width=300, anchor='w')
            self.Result_Sheet.column('Value', width=400, anchor='w')
            self.Result_Sheet.heading('Description', text='Description', anchor='w')
            self.Result_Sheet.heading('Value', text='Value', anchor='w')
            for ecu, ecuinfos in tmpinfo.items():
                st = self.ecunamedic[ecu].index('[')
                en = self.ecunamedic[ecu].index(']')
                ecu_item = self.Result_Sheet.insert('', (tk.END), text=('0x' + ecu + ' ' + self.ecunamedic[ecu][st + 1:en]),
                  open=True,
                  values=())
                self.Result_Sheet.item(ecu_item, tags=('newecu', ))
                for ecd, ecdinfos in ecuinfos.items():
                    ecd_item = self.Result_Sheet.insert(ecu_item, (tk.END), text=('0x' + ecd), open=True, values=())
                    self.Result_Sheet.item(ecd_item, tags=('newecd', ))
                    for description, value in ecdinfos:
                        item = self.Result_Sheet.insert(ecd_item, (tk.END), values=(description, value))
                        if description == 'no mdx imported. Origin Data displayed.':
                            self.Result_Sheet.item(item, tags=('mdxneeded', ))
                        else:
                            self.Result_Sheet.item(item, tags=('normal', ))

            self.Result_Sheet.tag_configure('newecu', background='lightblue')
            self.Result_Sheet.tag_configure('newecd', background='lightcyan')
            self.Result_Sheet.tag_configure('normal', background='lightgreen')
            self.Result_Sheet.tag_configure('mdxneeded', background='darkseagreen')
        elif self.runstatus == 3:
            tmpinfo = ecdcompare(self.bqinfo1, self.bqinfo2, self.bqinfo, tmpecus, tmpecdids)
            self.Result_Sheet['columns'] = ('Description', '1st BusQuery', '2nd BusQuery')
            self.Result_Sheet.column('#0', width=100, stretch=False)
            self.Result_Sheet.column('Description', width=220, anchor='w')
            self.Result_Sheet.column('1st BusQuery', width=250, anchor='w')
            self.Result_Sheet.column('2nd BusQuery', width=250, anchor='w')
            self.Result_Sheet.heading('Description', text='Description', anchor='w')
            self.Result_Sheet.heading('1st BusQuery', text='1st BusQuery', anchor='w')
            self.Result_Sheet.heading('2nd BusQuery', text='2nd BusQuery', anchor='w')
            for ecu, ecuinfos in tmpinfo.items():
                st = self.ecunamedic[ecu].index('[')
                en = self.ecunamedic[ecu].index(']')
                ecu_item = self.Result_Sheet.insert('', (tk.END), text=('0x' + ecu + ' ' + self.ecunamedic[ecu][st + 1:en]),
                  open=True,
                  values=())
                self.Result_Sheet.item(ecu_item, tags=('newecu', ))
                for ecd, ecdinfos in ecuinfos.items():
                    ecd_item = self.Result_Sheet.insert(ecu_item, (tk.END), text=('0x' + ecd), open=True, values=())
                    self.Result_Sheet.item(ecd_item, tags=('newecd', ))
                    for description, value1, value2 in ecdinfos:
                        item = self.Result_Sheet.insert(ecd_item, (tk.END), values=(description, value1, value2))
                        if value1 != value2:
                            self.Result_Sheet.item(item, tags=('different', ))
                        else:
                            if description == 'no mdx imported. Origin Data displayed.':
                                self.Result_Sheet.item(item, tags=('mdxneeded', ))
                            else:
                                self.Result_Sheet.item(item, tags=('normal', ))

            self.Result_Sheet.tag_configure('different', background='red')
            self.Result_Sheet.tag_configure('newecu', background='lightblue')
            self.Result_Sheet.tag_configure('newecd', background='lightcyan')
            self.Result_Sheet.tag_configure('normal', background='lightgreen')
            self.Result_Sheet.tag_configure('mdxneeded', background='darkseagreen')

    def dtc_button(self):
        self.curcommand = 2
        self.clean_sheet()
        self.ecumultiselect_entry()
        self.ecddidmultiselect_entry()
        if self.curecus == []:
            if self.ECUselect_Combobox.current() != 0:
                tmpecus = [
                 self.ECUselect_Combobox.get()[2:5]]
            else:
                tmpecus = []
                for ecuid in list(self.ECUselect_Combobox['value'])[1:]:
                    tmpecus.append(ecuid[2:5])

        else:
            tmpecus = self.curecus.copy()
        if self.runstatus == 1 or self.runstatus == 2:
            dtctype = self.DTC_Combobox.current()
            tmpinfo, restype, errorflag = dtclist(self.bqinfo, tmpecus, dtctype)
            self.Result_Sheet['columns'] = ('DID', 'Description', 'Status')
            self.Result_Sheet.column('#0', width=100, stretch=False)
            self.Result_Sheet.column('DID', width=80, anchor='w')
            self.Result_Sheet.column('Description', width=530, anchor='w')
            self.Result_Sheet.column('Status', width=80, anchor='w')
            self.Result_Sheet.heading('DID', text='DID', anchor='w')
            self.Result_Sheet.heading('Description', text=restype, anchor='w')
            self.Result_Sheet.heading('Status', text='Status', anchor='w')
            for ecu, ecuinfos in tmpinfo.items():
                st = self.ecunamedic[ecu].index('[')
                en = self.ecunamedic[ecu].index(']')
                if ecu not in errorflag:
                    ecu_item = self.Result_Sheet.insert('', (tk.END), text=('0x' + ecu + ' ' + self.ecunamedic[ecu][st + 1:en]),
                      open=True,
                      values=('', 'Numbers: ' + str(len(ecuinfos))))
                else:
                    ecu_item = self.Result_Sheet.insert('', (tk.END), text=('0x' + ecu + ' ' + self.ecunamedic[ecu][st + 1:en]),
                      open=True,
                      values=('', 'no 0x' + ecu + ' dtc info in this BusQuery File'))
                self.Result_Sheet.item(ecu_item, tags=('newecu', ))
                for did, dtcinfos, dtcstatus in ecuinfos:
                    item = self.Result_Sheet.insert(ecu_item, (tk.END), values=('0x' + did, dtcinfos, '0x' + dtcstatus))
                    if dtcstatusconfirm(2, dtcstatus) == 1:
                        self.Result_Sheet.item(item, tags=('failedthiscycle', ))
                    else:
                        self.Result_Sheet.item(item, tags=('normal', ))

            self.Result_Sheet.tag_configure('newecu', background='lightblue')
            self.Result_Sheet.tag_configure('normal', background='lightgreen')
            self.Result_Sheet.tag_configure('failedthiscycle', background='darkorange')
        elif self.runstatus == 3:
            tmpinfo, restype, res_num = dtccompare(self.bqinfo1, self.bqinfo2, self.bqinfo, tmpecus, self.DTC_Combobox.current())
            self.Result_Sheet['columns'] = ('DID', 'Description', 'Status(1st)', 'Status(2nd)')
            self.Result_Sheet.column('#0', width=100, stretch=False)
            self.Result_Sheet.column('DID', width=80, anchor='w')
            self.Result_Sheet.column('Description', width=430, anchor='w')
            self.Result_Sheet.column('Status(1st)', width=85, anchor='w')
            self.Result_Sheet.column('Status(2nd)', width=85, anchor='w')
            self.Result_Sheet.heading('DID', text='DID', anchor='w')
            self.Result_Sheet.heading('Description', text=('Description(' + restype + ')'), anchor='w')
            self.Result_Sheet.heading('Status(1st)', text='Status(1st)', anchor='w')
            self.Result_Sheet.heading('Status(2nd)', text='Status(2nd)', anchor='w')
            for ecu, ecuinfos in tmpinfo.items():
                st = self.ecunamedic[ecu].index('[')
                en = self.ecunamedic[ecu].index(']')
                ecu_item = self.Result_Sheet.insert('', (tk.END), text=('0x' + ecu + ' ' + self.ecunamedic[ecu][st + 1:en]),
                  open=True,
                  values=('', str(res_num[ecu][0]) + '  ;  ' + str(res_num[ecu][1])))
                self.Result_Sheet.item(ecu_item, tags=('newecu', ))
                for did, description, dtcinfo1, dtcinfo2 in ecuinfos:
                    item = self.Result_Sheet.insert(ecu_item, (tk.END), values=('0x' + did, description, '0x' + dtcinfo1, '0x' + dtcinfo2))
                    if dtcinfo1 == '-':
                        self.Result_Sheet.item(item, tags=('newlyadded', ))
                    else:
                        if dtcinfo2 == '-':
                            self.Result_Sheet.item(item, tags=('decreased', ))
                        else:
                            if dtcinfo1 != dtcinfo2:
                                self.Result_Sheet.item(item, tags=('different', ))
                            else:
                                self.Result_Sheet.item(item, tags=('normal', ))

            self.Result_Sheet.tag_configure('newecu', background='lightblue')
            self.Result_Sheet.tag_configure('newlyadded', background='red')
            self.Result_Sheet.tag_configure('decreased', background='tomato')
            self.Result_Sheet.tag_configure('different', background='limegreen')
            self.Result_Sheet.tag_configure('normal', background='lightgreen')

    def copy_selection(self, event):
        selected_items = self.Result_Sheet.selection()
        if selected_items:
            values = []
            for item in selected_items:
                if self.Result_Sheet.item(item)['values'] == '':
                    values.append([self.Result_Sheet.item(item)['text']])
                else:
                    values.append(self.Result_Sheet.item(item)['values'])

            formatted_data = ''
            for row in values:
                formatted_data += '\t'.join(map(str, row)) + '\n'

            pyperclip.copy(formatted_data)

    def clean_sheet(self):
        for item in self.Result_Sheet.get_children():
            self.Result_Sheet.delete(item)

        for col in self.Result_Sheet['columns']:
            self.Result_Sheet.heading(col, text='', anchor='w')

    def save_as_excel(self):
        file_path = filedialog.asksaveasfilename(title='save to', defaultextension='.xlsx', filetypes=[('Excel Workbook', '*.xlsx')])
        if file_path:
            data = []
            if self.curcommand == 1 or self.curcommand == 2:
                columnlen = len(self.Result_Sheet['columns'])
                for item in self.Result_Sheet.get_children():
                    ecu = self.Result_Sheet.item(item)['text']
                    for child in self.Result_Sheet.get_children(item):
                        value = []
                        value.append(ecu)
                        for i in range(0, columnlen):
                            value.append(self.Result_Sheet.item(child)['values'][i])

                        data.append(value)

                tmpcolumns = list(self.Result_Sheet['columns'])
                tmpcolumns.insert(0, 'ECU')
                df = pd.DataFrame(data, columns=tmpcolumns)
                writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
                df.to_excel(writer, sheet_name='Sheet1', index=False)
                worksheet = writer.sheets['Sheet1']
                workbook = writer.book
                text_format = workbook.add_format({'num_format':'@',  'align':'left'})
                worksheet.set_column(0, 0, 15)
                worksheet.set_column(2, columnlen + 1, 50, text_format)
                writer.save()
                sortexcel(file_path, 1)
                if self.runstatus == 3 or self.runstatus == 4:
                    markdifferent(file_path)
            elif self.curcommand == 3:
                columnlen = len(self.Result_Sheet['columns'])
                for item in self.Result_Sheet.get_children():
                    ecu = self.Result_Sheet.item(item)['text']
                    for child in self.Result_Sheet.get_children(item):
                        did = self.Result_Sheet.item(child)['text']
                        for secondchild in self.Result_Sheet.get_children(child):
                            value = [
                             ecu, did]
                            for i in range(0, columnlen):
                                value.append(self.Result_Sheet.item(secondchild)['values'][i])

                            data.append(value)

                tmpcolumns = list(self.Result_Sheet['columns'])
                tmpcolumns.insert(0, 'DID')
                tmpcolumns.insert(0, 'ECU')
                df = pd.DataFrame(data, columns=tmpcolumns)
                writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
                df.to_excel(writer, sheet_name='Sheet1', index=False)
                worksheet = writer.sheets['Sheet1']
                workbook = writer.book
                text_format = workbook.add_format({'num_format':'@',  'align':'left'})
                worksheet.set_column(0, 0, 15)
                worksheet.set_column(2, columnlen + 1, 50, text_format)
                writer.save()
                sortexcel(file_path, 2)
                if self.runstatus == 3:
                    markdifferent(file_path)

    def on_select(self):
        if self.Bomchecktype.get() == '0':
            self.VN_Entry.configure(state='disabled')
        else:
            self.VN_Entry.configure(state='normal')

    def website_click(self):
        webbrowser.open('https://azureford.sharepoint.com/sites/bqreader')

    def fuzzysearch(self, event=None):
        keyword = self.FuzzySearch_Entry.get()
        if not keyword:
            return 0
        self.ecd_button()
        if self.Searchtype.get() == '0':
            for ecu in self.Result_Sheet.get_children():
                for ecd in self.Result_Sheet.get_children(ecu):
                    for child in self.Result_Sheet.get_children(ecd):
                        if self.str_similar(str(self.Result_Sheet.item(child)['values'][0]), keyword) >= 0.7:
                            self.Result_Sheet.item(child, tags=('match', ))

        else:
            if self.Searchtype.get() == '1':
                for ecu in self.Result_Sheet.get_children():
                    for ecd in self.Result_Sheet.get_children(ecu):
                        for child in self.Result_Sheet.get_children(ecd):
                            if self.str_similar(str(self.Result_Sheet.item(child)['values'][0]), keyword) >= 0.9:
                                self.Result_Sheet.item(child, tags=('match', ))

            else:
                if self.Searchtype.get() == '2':
                    for ecu in self.Result_Sheet.get_children():
                        for ecd in self.Result_Sheet.get_children(ecu):
                            for child in self.Result_Sheet.get_children(ecd):
                                if keyword.lower() in str(self.Result_Sheet.item(child)['values'][0]).lower():
                                    self.Result_Sheet.item(child, tags=('match', ))

        self.match_count = 0
        self.current_match = 0
        match_index = 0
        for ecu in self.Result_Sheet.get_children():
            for ecd in self.Result_Sheet.get_children(ecu):
                for child in self.Result_Sheet.get_children(ecd):
                    if 'match' in self.Result_Sheet.item(child)['tags']:
                        self.match_count += 1
                        if self.current_match == 0:
                            self.current_match = self.match_count
                            self.Result_Sheet.selection_set(child)
                            self.Result_Sheet.focus(child)
                            self.Result_Sheet.see(child)
                            match_index += 1

        self.Match_Count_Label.config(text=f"{self.current_match}/{self.match_count}")
        if not self.Result_Sheet.tag_has('match'):
            messagebox.showinfo('Failure', 'No matches found.')
        self.Result_Sheet.tag_configure('match', background='blue')

    def select_next(self, event=None):
        selection = self.Result_Sheet.selection()
        next_did = self.Result_Sheet.parent(selection)
        next_ecu = self.Result_Sheet.parent(next_did)
        if selection:
            next_item = self.Result_Sheet.next(selection)
            while next_ecu:
                while next_did:
                    while next_item:
                        if 'match' in self.Result_Sheet.item(next_item)['tags']:
                            self.Result_Sheet.selection_set(next_item)
                            self.Result_Sheet.focus(next_item)
                            self.Result_Sheet.see(next_item)
                            self.current_match += 1
                            self.Match_Count_Label.config(text=f"{self.current_match}/{self.match_count}")
                            return
                        next_item = self.Result_Sheet.next(next_item)
                    else:
                        next_did = self.Result_Sheet.next(next_did)
                        if next_did:
                            while bool(self.Result_Sheet.get_children(next_did)) == False:
                                next_did = self.Result_Sheet.next(next_did)
                            else:
                                next_item = self.Result_Sheet.get_children(next_did)[0]

                else:
                    next_ecu = self.Result_Sheet.next(next_ecu)
                    if next_ecu:
                        while bool(self.Result_Sheet.get_children(next_ecu)) == False:
                            next_ecu = self.Result_Sheet.next(next_ecu)
                        else:
                            next_did = self.Result_Sheet.get_children(next_ecu)[0]
                            if next_did:
                                while bool(self.Result_Sheet.get_children(next_did)) == False:
                                    next_did = self.Result_Sheet.next(next_did)
                                else:
                                    next_item = self.Result_Sheet.get_children(next_did)[0]

    def select_prev(self, event=None):
        selection = self.Result_Sheet.selection()
        prev_did = self.Result_Sheet.parent(selection)
        prev_ecu = self.Result_Sheet.parent(prev_did)
        if selection:
            prev_item = self.Result_Sheet.prev(selection)
            while prev_ecu:
                while prev_did:
                    while prev_item:
                        if 'match' in self.Result_Sheet.item(prev_item)['tags']:
                            self.Result_Sheet.selection_set(prev_item)
                            self.Result_Sheet.focus(prev_item)
                            self.Result_Sheet.see(prev_item)
                            self.current_match -= 1
                            self.Match_Count_Label.config(text=f"{self.current_match}/{self.match_count}")
                            return
                        prev_item = self.Result_Sheet.prev(prev_item)
                    else:
                        prev_did = self.Result_Sheet.prev(prev_did)
                        if prev_did:
                            while bool(self.Result_Sheet.get_children(prev_did)) == False:
                                prev_did = self.Result_Sheet.prev(prev_did)
                            else:
                                prev_item = self.Result_Sheet.get_children(prev_did)[-1]

                else:
                    prev_ecu = self.Result_Sheet.prev(prev_ecu)
                    if prev_ecu:
                        while bool(self.Result_Sheet.get_children(prev_ecu)) == False:
                            prev_ecu = self.Result_Sheet.prev(prev_ecu)
                        else:
                            prev_did = self.Result_Sheet.get_children(prev_ecu)[-1]
                            if prev_did:
                                while bool(self.Result_Sheet.get_children(prev_did)) == False:
                                    prev_did = self.Result_Sheet.prev(prev_did)
                                else:
                                    prev_item = self.Result_Sheet.get_children(prev_did)[-1]

    def str_similar(self, s1, s2):
        s1 = s1.lower()
        s2 = s2.lower()
        max_ratio = 0
        for i in range(len(s1) - len(s2) + 1):
            substr = s1[i:i + len(s2)]
            ratio = difflib.SequenceMatcher(None, substr, s2).quick_ratio()
            max_ratio = max(max_ratio, ratio)

        return max_ratio

    def update_click(self):
        cur_path = os.getcwd()
        updater_path = cur_path.replace('BQreader\\bq_reader','OTAinstaller\\OTAinstaller.exe')
        subprocess.Popen([updater_path])
        root.destroy()

    def select_update(self):
        # def command1():
        #     self.update_click()
        #     self.root.after(0, self.root.destroy)
        # def command2():
        #     self.website_click()
        #     self.root.after(0, self.root.destroy)
        popup_window = tk.Toplevel(root)
        popup_window.wm_attributes('-alpha', 0.0)
        popup_window.title('Version Update Needed')
        tmpimg = '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'
        with open('tmp.ico', 'wb') as (tmp):
            tmp.write(base64.b64decode(tmpimg))
        popup_window.wm_iconbitmap('tmp.ico')
        os.remove('tmp.ico')
        popup_window.geometry('300x80')
        popup_window.resizable(width=False, height=False)
        popup_label = tk.Label(popup_window, text='This Version is not supported any more.\nThe tool will be closed in 20s.\n Please update to new version for better performance.')
        popup_button1 = tk.Button(popup_window, text='Update Online', command=self.update_click)
        popup_button2 = tk.Button(popup_window, text='Download from Sharepoint', command=self.website_click)
        popup_label.pack()
        popup_button1.pack(side='left')
        popup_button2.pack(side='right')
        x = root.winfo_rootx() + root.winfo_width() // 2 - 100
        y = root.winfo_rooty() + root.winfo_height() // 2 - 40
        popup_window.geometry('+{}+{}'.format(x, y))
        popup_window.wm_attributes('-alpha', 1.0)




if __name__ == '__main__':
    tmppreload = '/9j/4AAQSkZJRgABAQEAYABgAAD/4QAiRXhpZgAATU0AKgAAAAgAAQESAAMAAAABAAEAAAAAAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAD6AZADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD856KKK/aD5cKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAC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iZWdlIUMVBUZwfmNfOdFaLB0vY/V7e76tafmT7SXNz9T7w/aj/4KyfB/9qv4n2vjrxB+zG1342t9T0u6Oo6j8R77UbZ7S0vIZpbEWUlv9mWGeFJoSoj2qbh5NrNndc+DX/BcDT/2c/2r/EfjbwD8EPDPhTwB4v0K20jWPAtjfxQ2t1PbvI0d4s8dooWQCaVCvlFWWRs5O0r8B0Vj/ZeG5PZtNq1rOUnpp3flp26FfWJ3v19EfeXxE/4LO+HdI/Y88afB/wCC/wADNM+Dem+PpJv7XvYfEkmsSSRzhUuUVZbdCPMiBi5YhEYhFU7SPg2iiujD4WlQTVNbu71bbfq7sidSU/iCiiiuggKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiq+laiNWsVnWG4gDMy7J4zHINrFeQexxkHuCD3qxSjJNXQBRRRTAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAor2L/AId4/H//AKIX8Yf/AAjNS/8AjNH/AA7x+P8A/wBEL+MP/hGal/8AGa5fruH/AJ196NPZz7HjtFexf8O8fj//ANEL+MP/AIRmpf8Axmj/AId4/H//AKIX8Yf/AAjNS/8AjNH13D/zr70Hs59jx2ivYv8Ah3j8f/8Aohfxh/8ACM1L/wCM0f8ADvH4/wD/AEQv4w/+EZqX/wAZo+u4f+dfeg9nPseO0V7F/wAO8fj/AP8ARC/jD/4Rmpf/ABmj/h3j8f8A/ohfxh/8IzUv/jNH13D/AM6+9B7OfY8dor2L/h3j8f8A/ohfxh/8IzUv/jNH/DvH4/8A/RC/jD/4Rmpf/GaPruH/AJ196D2c+x47RXsX/DvH4/8A/RC/jD/4Rmpf/GaP+HePx/8A+iF/GH/w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'
    with open('tmppreload200.jpg', 'wb') as (tmp):
        tmp.write(base64.b64decode(tmppreload))
    image = Image.open('tmppreload200.jpg')
    window = tk.Tk()
    window.overrideredirect(1)
    window_width = image.width
    window_height = image.height
    x = window.winfo_screenwidth() // 2 - window_width // 2
    y = window.winfo_screenheight() // 2 - window_height // 2
    window.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))
    tk_image = ImageTk.PhotoImage(image)
    window.geometry('%dx%d' % (image.width, image.height))
    image_label = tk.Label(window, image=tk_image)
    image_label.place(x=((window_width - image.width) // 2), y=((window_height - image.height) // 2))
    os.remove('tmppreload200.jpg')
    githubinfo = {'curver':200,  'supver':[200],  'info':[10]}

    def loading_finish():
        global githubinfo
        try:
            githubinfo = updateornot()
        except:
            githubinfo = {'curver':200,
             'supver':[200],  'info':[10]}
        window.after(0, window.destroy)


    def start_thread():
        thread = threading.Thread(target=loading_finish)
        thread.start()


    start_thread()
    window.mainloop()
    root = TkinterDnD.Tk()
    style = Style()
    app = App(root, githubinfo)
    root.mainloop()
