import sys
import os
import traceback

from tkinter import ttk
import tkinter

from status import HttpChecker, FtpChecker, RsyncChecker, WhynotChecker


tk = tkinter.Tk()
tk.attributes('-fullscreen', True)
tk.attributes('-zoomed', True)
tk.geometry("800x600")
tk.grid()

statusframe = tkinter.Frame(tk)
statusframe.place(relx=0.1, rely=0.1)

status_font = ("Arial", 24)
status_height = 1
status_width = 25
status_borderwidth = 1
status_refief = "solid"


labels_checkers = []

for row, name, checker in [(0, "HOPE", HttpChecker("https://www3.cmbi.umcn.nl/hope/")),
                           (1, "MRS", HttpChecker("https://mrs.cmbi.umcn.nl/")),
                           (2, "FTP", FtpChecker("ftp.cmbi.umcn.nl", "/pub/molbio/data/")),
                           (3, "RSYNC", RsyncChecker("rsync://rsync.cmbi.ru.nl/dssp/1crn.dssp")),
                           (4, "DSSP", WhynotChecker("DSSP")),
                           (5, "HSSP", WhynotChecker("HSSP")),
                           (6, "BDB", WhynotChecker("BDB")),
                           (7, "PDBFINDER", WhynotChecker("PDBFINDER")),
                           (8, "PDBFINDER2", WhynotChecker("PDBFINDER2"))]:

    name_label = tkinter.Label(statusframe,
                               text=name,
                               bg="white",
                               borderwidth=status_borderwidth, relief=status_refief,
                               font=status_font,
                               width=status_width, height=status_height)
    name_label.grid(column=0, row=row)

    value_label = tkinter.Label(statusframe,
                                borderwidth=status_borderwidth, relief=status_refief,
                                font=status_font,
                                width=status_width, height=status_height)
    value_label.grid(column=1, row=row)

    labels_checkers.append((value_label, checker))

    checker.start()


while True:
    for label, checker in labels_checkers:
        checker.update(label)

    tk.update_idletasks()
    tk.update()
