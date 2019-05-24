import sys
import os
import traceback
from time import localtime, strftime

from tkinter import ttk
import tkinter

from status import HttpChecker, FtpChecker, RsyncChecker, WhynotChecker, HopeStatisticsChecker


tk = tkinter.Tk()
tk.attributes('-fullscreen', True)
tk.attributes('-zoomed', True)
tk.geometry("800x600")
tk.grid()

statusframe = tkinter.Frame(tk)
statusframe.place(relx=0.1, rely=0.1)

status_font = ("Arial", 24)
status_height = 1
status_width = 20
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

    time_label = tkinter.Label(statusframe,
                               bg="white",
                               borderwidth=status_borderwidth, relief=status_refief,
                               font=status_font,
                               width=status_width, height=status_height)
    time_label.grid(column=2, row=row)

    labels_checkers.append((value_label, None, checker, time_label))

    checker.start()


hope_label = tkinter.Label(statusframe,
                           text="HOPE:", bg="white",
                           borderwidth=status_borderwidth, relief=status_refief,
                           font=status_font,
                           width=status_width, height=status_height)
hope_label.grid(column=0, row=9)

hope_checker = HopeStatisticsChecker()

for row, key in [(10, "PENDING"), (11, "STARTED"), (12, "FAILURE"), (13, "SUCCESS")]:

    name_label = tkinter.Label(statusframe, text=key, bg="white",
                               borderwidth=status_borderwidth, relief=status_refief,
                               font=status_font,
                               width=status_width, height=status_height)
    name_label.grid(column=0, row=row)

    value_label = tkinter.Label(statusframe,
                                borderwidth=status_borderwidth, relief=status_refief,
                                font=status_font,
                                width=status_width, height=status_height)
    value_label.grid(column=1, row=row)

    labels_checkers.append((value_label, key, hope_checker, None))

hope_checker.start()


while True:
    for value_label, key, checker, time_label in labels_checkers:
        last_time = checker.update(key, value_label)
        if time_label is not None and last_time is not None:
            time_label.configure(text=strftime("%Y-%m-%d %T", localtime(last_time)))

    tk.update_idletasks()
    tk.update()
