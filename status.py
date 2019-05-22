import os
import requests
from ftplib import FTP
import tempfile
from threading import Thread, Lock
from time import time


class StatusChecker(Thread):
    def __init__(self):
        Thread.__init__(self)

        self._lock = Lock()
        self._label_text = None
        self._label_color = None
        self._time = None

    def run(self):
        while True:
            try:
                label_text, label_color = self.get_text_and_color()
                t = time()
            except Exception as e:
                label_text = str(e)
                label_color = "red"

            with self._lock:
                self._label_text = label_text
                self._label_color = label_color
                self._time = t

    def update(self, label):
        with self._lock:
            label.configure(text=self._label_text, bg=self._label_color)
            return self._time

    def get_text_and_color(self):
        raise RuntimeError("Not implemented")


class HttpChecker(StatusChecker):
    def __init__(self, url):
        StatusChecker.__init__(self)

        self.url = url

    def get_text_and_color(self):
        r = requests.get(self.url)

        if r.status_code == 200:
            color = "green"
        else:
            color= "red"

        text = requests.status_codes._codes[r.status_code][0]

        return (text, color)


def do_nothing(x):
    pass


class FtpChecker(StatusChecker):
    def __init__(self, host, dir_path):
        StatusChecker.__init__(self)

        self.host = host
        self.dir_path = dir_path

    def get_text_and_color(self):
        try:
            ftp = FTP(self.host)
            ftp.login()
            ftp.cwd(self.dir_path)
            ftp.dir(do_nothing)
            ftp.quit()

            return ("success", "green")
        except Exception as e:
            return (str(e), "red")


class RsyncChecker(StatusChecker):
    def __init__(self, source):
        StatusChecker.__init__(self)

        self.source = source

    def get_text_and_color(self):
        dest = tempfile.mktemp()

        try:
            r = os.system("/usr/bin/rsync -a %s %s" % (self.source, dest))
        finally:
            if os.path.isfile(dest):
                os.remove(dest)

        text = "exit {}".format(r)
        if r == 0:
            return (text, "green")
        else:
            return (text, "red")


class WhynotChecker(StatusChecker):
    def __init__(self, db):
        StatusChecker.__init__(self)

        self.db = db

    def get_text_and_color(self):
        r = requests.get("https://www3.cmbi.umcn.nl/WHY_NOT2/entries_file/?databank=%s&collection=unannotated&listing=PDBIDs" % self.db)

        if r.status_code != 200:
            color = "red"
            text = requests.status_codes._codes[r.status_code][0]

        count = len(r.text.split())

        if count <= 0:
            color = "green"

        elif count < 1000:
            color = "yellow"
        else:
            color = "red"

        text = "%i unannotated" % count

        return (text, color)
