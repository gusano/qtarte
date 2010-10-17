#!/usr/bin/env python 
# -*- coding: utf-8 -*-


import sys
import os, subprocess, shutil, select
import signal
import re
import urllib2, xml.dom.minidom
import pynotify 
import locale
import gettext
import BeautifulSoup as BS

from Catalog import Catalog, unescape_html, get_lang
from arte7_ui import*

from PyQt4 import QtCore, QtGui

subprocess_pid = None

def unescape_xml(text):
    text = text.replace( "%3A", ":").replace( "%2F", "/").replace( "%2C", ",")
    return BS.BeautifulStoneSoup(text, convertEntities=BS.BeautifulStoneSoup.XML_ENTITIES).contents[0]

def get_rtmp_url( url_page, quality ):
    page_soup = BS.BeautifulSoup(urllib2.urlopen(url_page).read())

    movie_object = page_soup.find("object", classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000")
    movie = movie_object.find("param", {"name":"movie"})
    movie_url = "http" + unescape_xml(movie['value'].split("http")[-1])

    xml_soup = BS.BeautifulStoneSoup(urllib2.urlopen(movie_url).read())
    movie_url = xml_soup.find("video", {'lang': get_lang()})['ref']

    xml_soup = BS.BeautifulStoneSoup(urllib2.urlopen(movie_url).read())
    base_soup = xml_soup.find("urls")
    movie_url = base_soup.find("url", {"quality": quality}).string
    return movie_url

def rtmp_download( link, destination = "/dev/null", try_resume = True, resuming =False ):
    global subprocess_pid
    some_dl_done = False
    need_more_dl = True
    if try_resume and os.path.isfile( destination ):
        for percent in rtmp_download(link, destination, False, True ):
            if percent != -1:
                some_dl_done = True
                need_more_dl = percent != 100.0
                yield percent
            else:
                break

    cmd_dl = 'flvstreamer -r "%s" --flv "%s"' % (link, destination)
    cmd_resume = 'flvstreamer -r "%s" --resume --flv "%s"' % (link, destination)
    cmd_resume_skip = 'flvstreamer -r "%s" --resume --skip 1 --flv "%s"' % (link, destination)
    SECONDS_TO_WAIT = 3
    max_skip_cnt = 10
    percent_re = re.compile("\((.+)%\)$")

    ret_code = None
    if some_dl_done or resuming:
        cmd = cmd_resume
    else:
        cmd = cmd_dl
    while need_more_dl:
        stderr_buff = ""
        whole_stderr_buff = ""
        p = subprocess.Popen( cmd, shell=True, stderr=subprocess.PIPE, close_fds=True)
        subprocess_pid = p.pid + 1
        while ret_code is None:
            fds_read, fds_write, fds_exception = select.select([p.stderr],[], [], SECONDS_TO_WAIT)
            if len(fds_read) == 1:
                c = p.stderr.read(1)
                whole_stderr_buff += c
                if c in ("\n","\r"):
                    match = percent_re.search( stderr_buff )
                    if match is not None:
                        # If anyframe was retreived, then reset available skip count
                        max_skip_cnt = 10
                        yield float(match.group(1))
                    stderr_buff = ""
                else:
                    stderr_buff += c
            ret_code = p.poll()
        whole_stderr_buff += p.stderr.read()
        subprocess_pid = None
        if ret_code == 0:
            yield 100.0
            break
        elif ret_code == 2:
            cmd = cmd_resume
        else:
            must_resume = False
            for line in whole_stderr_buff.split("\n"):
                if line.find("Couldn't resume FLV file, try --skip 1") != -1:
                    must_resume = True
                    break
            if must_resume and max_skip_cnt >= 0:
                max_skip_cnt -= 1
                cmd = cmd_resume_skip
            else:
                print ret_code
                print whole_stderr_buff
                print
                yield -1.0
        ret_code = None


class Arte7(object):
    """Main class.

    """
    wmvRE = re.compile('availableFormats.*=.*"(.*HQ.*wmv.*)"')
    mmsRE = re.compile('"(mms.*)"')
    resumeRE = re.compile('<p class="text">([^<]*)<')
    dureeRE = re.compile('[^0-9]*([0-9]+)(mn|min)')
    def __init__(self):
        # Wake up GUI
        ui.arte = self
        reply = ui.populate()
        ui.cleaning()
        self.abort_dwnld = False
        self.p_signal = ProgressSignal()
        self.p_signal.bind(ui)


        self.c_dir = os.getcwd()
        self.dirconf = self.c_dir 

        while 1:
            if not ui.cfg["folder"]:
                ui.set_settings()
            else:
                break
        self.directory = ui.cfg["folder"]
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

    def notify(self, n_signal):
        img_uri = os.path.join(os.getcwd(), "medias/icon.png")
        pynotify.init("Arte+7 Recorder")
        notification = pynotify.Notification(self.nom_emi, "Download complete", img_uri)
        notification.show()
        n_signal.value = 2
        n_signal.emit_signal()
        return


    def set_options(self, f):
        return True


    #Download
    def on_telecharge(self, movies):
        n_signal = NotifySignal()
        n_signal.bind(ui)
        for n in movies:
            url_page = n[2]
            self.nom_emi = n[0]
            self.nom_fichier = self.nom_emi + "-" + n[1] + '.flv'
            self.nom_fichier = self.nom_fichier.replace("/", "-")
            n_signal.value = 1
            n_signal.emit_signal()
            ui.active_download = True
            try:
                rtmp_url = get_rtmp_url(url_page, quality = "hd")
                signal_fin = False
                for percent in rtmp_download(rtmp_url, self.directory + "/" + self.nom_fichier.replace("'", "_")):
                    if percent == -1.0:
                        raise IOError()
                    signal_fin = percent == 100.0
                    self.p_signal.value = int(percent)
                    self.p_signal.emit_signal()
                    if self.abort_dwnld:
                        if subprocess_pid is not None:
                            os.kill( subprocess_pid, signal.SIGINT )
                            n_signal.value = 3
                            n_signal.emit_signal() 
                            break

            except IOError, why:
                print "Download error :", why
                n_signal.value = why
                n_signal.emit_signal()
                                           
            else:
                if signal_fin :
                    self.notify(n_signal)
        # Kill the gui thread
        ui.stop = True

class NotifySignal(QtCore.QObject):
    """Signal used by on_telecharge function.

    This signal is used by telecharge when a downloading of 
    movie is completed.
    """
    loadFinished = QtCore.pyqtSignal()

    def bind(self, ui):
        self.ui = ui
        self.value = None
        self.loadFinished.connect(self.next)

    def emit_signal(self):
        self.loadFinished.emit() 

    def next(self):
        self.ui.download_notify(self.value)

class ProgressSignal(QtCore.QObject):
    """Signal used by on_telecharge function.

    This signal is used by telechage when a downloading of 
    movie is completed.
    """
    loadProgress = QtCore.pyqtSignal()
             
    def bind(self, ui):
        self.ui = ui
        self.value = None
        self.loadProgress.connect(self.next)

    def emit_signal(self):
        self.loadProgress.emit() 

    def next(self):
        self.ui.progress_notify(self.value)

def make_connection():
    catalog = Catalog()
    f = os.path.join(ui.user_folder, 'database')
    if catalog.error:
        ui.on_error_data(catalog.error)
    else:
        try:
            with open(f, 'w') as datalist:
                datalist.write('\n'.join(['%s;%s;%s;%s' % (video[Catalog.TITLE_TAG], 
                                    video[Catalog.DATE_TAG], video[Catalog.URL_TAG], 
                                    video[Catalog.IMAGE_TAG]) 
                                    for video in catalog.videos]))
        except IOError, why:
            ui.on_error_data(why)



if __name__ == "__main__":
    cwd = os.path.split(sys.argv[0])[0]
    app = QtGui.QApplication(sys.argv)
    ## Translation process
    loc = QtCore.QLocale.system().name()
    qtTranslator = QtCore.QTranslator()
    if qtTranslator.load("qt_" + loc):
        app.installTranslator(qtTranslator)
    appTranslator = QtCore.QTranslator()
    if appTranslator.load("arte7recorder_" + loc):
        app.installTranslator(appTranslator)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, cwd)
    make_connection()
    
    arte = Arte7()
    
    sys.exit(app.exec_())












