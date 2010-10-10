# -*- coding: utf-8 -*-

# arteNew.py
#
# Date: Mon Oct  4 2010     
# Author : Vincent Vande Vyvre <vins@swing.be>
# Version : 0.1
# Revision : 4
#
# Graphical user's interface for Arte7Recorder version Qt
#
# arte7recorder : https://launchpad.net/~arte+7recorder
# qtarte : https://code.launchpad.net/~arte+7recorder/+junk/qtarte
#
# Warning : Use this script only for testing



import os
import sys
import shutil
import pickle
import glob
import time
import urllib2
import re
from threading import Thread
import BeautifulSoup as BS

from setting import*

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(True)
        self.preview = Preview(self, MainWindow, self.splitter)

        self.editor = QtGui.QTextEdit(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, 
                                    QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editor.sizePolicy()
                                    .hasHeightForWidth())
        self.editor.setSizePolicy(sizePolicy)
        self.editor.setMaximumSize(QtCore.QSize(16777215, 150))
        self.editor.setAcceptDrops(False)
        self.editor.setUndoRedoEnabled(False)
        self.editor.setAcceptRichText(True) 
        self.editor.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|
                                    QtCore.Qt.TextSelectableByMouse)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 717, 25))
        self.menu_Options = QtGui.QMenu(self.menubar)
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_Help = QtGui.QMenu(self.menubar)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        # Tool panel
        self.tool_panel = QtGui.QDockWidget(MainWindow)
        self.tool_panel.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|
                                    QtCore.Qt.RightDockWidgetArea)
        self.tool_panel.setWindowTitle("None")
        self.dockWidgetContents = QtGui.QWidget()
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout = QtGui.QVBoxLayout()

        # List of selected videos for download
        self.list_dwnld = ListDwnld(self, self.dockWidgetContents)
        self.verticalLayout.addWidget(self.list_dwnld)

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.add_btn = QtGui.QToolButton(self.dockWidgetContents)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("medias/add.png"), QtGui.QIcon.Normal, 
                                    QtGui.QIcon.Off)
        self.add_btn.setIcon(icon)
        self.horizontalLayout.addWidget(self.add_btn)
        self.remove_btn = QtGui.QToolButton(self.dockWidgetContents)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("medias/remove.png"), QtGui.QIcon.Normal, 
                                    QtGui.QIcon.Off)
        self.remove_btn.setIcon(icon1)
        self.horizontalLayout.addWidget(self.remove_btn)
        self.up_btn = QtGui.QToolButton(self.dockWidgetContents)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("medias/up.svg"), QtGui.QIcon.Normal, 
                                    QtGui.QIcon.Off)
        self.up_btn.setIcon(icon2)
        self.horizontalLayout.addWidget(self.up_btn)
        self.down_btn = QtGui.QToolButton(self.dockWidgetContents)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("medias/down.svg"), QtGui.QIcon.Normal, 
                                    QtGui.QIcon.Off)
        self.down_btn.setIcon(icon3)
        self.horizontalLayout.addWidget(self.down_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.download_btn = QtGui.QToolButton(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, 
                                    QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.download_btn.sizePolicy()
                                    .hasHeightForWidth())
        self.download_btn.setSizePolicy(sizePolicy)
        self.download_btn.setText("Download")
        self.verticalLayout.addWidget(self.download_btn)
        self.prog_bar = QtGui.QProgressBar(self.dockWidgetContents)
        self.prog_bar.setProperty("value", 0)
        self.verticalLayout.addWidget(self.prog_bar)
        self.cancel_btn = QtGui.QToolButton(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, 
                                    QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_btn.sizePolicy()
                                    .hasHeightForWidth())
        self.cancel_btn.setSizePolicy(sizePolicy)
        self.cancel_btn.setText("Cancel")
        self.verticalLayout.addWidget(self.cancel_btn)
        self.save_pitch_btn = QtGui.QToolButton(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, 
                                    QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_pitch_btn.sizePolicy()
                                    .hasHeightForWidth())
        self.save_pitch_btn.setSizePolicy(sizePolicy)
        self.save_pitch_btn.setText("Save text")
        self.verticalLayout.addWidget(self.save_pitch_btn)
        self.fake_btn = QtGui.QToolButton(self.dockWidgetContents)
        self.fake_btn.hide()
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tool_panel.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.tool_panel)
        self.action_Settings = QtGui.QAction(MainWindow)
        self.action_Connection = QtGui.QAction(MainWindow)
        self.action_About = QtGui.QAction(MainWindow)
        self.action_Download = QtGui.QAction(MainWindow)
        self.action_Cancel = QtGui.QAction(MainWindow)
        self.action_Quit = QtGui.QAction(MainWindow)
        self.menu_Options.addAction(self.action_Settings)
        self.menu_File.addAction(self.action_Connection)
        self.menu_File.addAction(self.action_Download)
        self.menu_File.addAction(self.action_Cancel) 
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_Help.addAction(self.action_About)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Options.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        QtCore.QObject.connect(self.action_Settings, QtCore.SIGNAL
                                ("triggered()"), self.set_settings)
        QtCore.QObject.connect(self.action_Connection, QtCore.SIGNAL
                                ("triggered()"), self.reconnect)
        QtCore.QObject.connect(self.action_About, QtCore.SIGNAL
                                ("triggered()"), self.nihil)
        QtCore.QObject.connect(self.action_Download, QtCore.SIGNAL
                                ("triggered()"), self.download)
        QtCore.QObject.connect(self.action_Cancel, QtCore.SIGNAL
                                ("triggered()"), self.cancel)
        QtCore.QObject.connect(self.action_Quit, QtCore.SIGNAL
                                ("triggered()"), self.closeEvent)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()
        self.editor.append(u"\n\n    Connection à  http://arte7.arte.tv ...")
        QtCore.QCoreApplication.processEvents()
        MainWindow.closeEvent = self.closeEvent       

        self.add_btn.clicked.connect(self.add_video)
        self.remove_btn.clicked.connect(self.remove_video)
        self.up_btn.clicked.connect(self.move_up)
        self.down_btn.clicked.connect(self.move_down)
        self.download_btn.clicked.connect(self.download)
        self.cancel_btn.clicked.connect(self.cancel)
        self.save_pitch_btn.clicked.connect(self.record_pitch)
        self.fake_btn.clicked.connect(self.progress_notify)

        self.colors = ["Black", "Blue",   
                    "Cyan", "Dark blue", 
                    "Dark cyan", "Dark grey",
                    "Dark green", "Dark magenta",
                    "Dark red", "Dark yellow",
                    "Grey", "Green", 
                    "Light grey", "Magenta", 
                    "Red", "White",
                    "Yellow"]
        self.set_buttons(False)
        self.add_btn.setEnabled(False)
        self.active_download = False
        self.thumb_folder = os.path.join(os.getcwd(), "thumbnails")
        if not os.path.isdir(self.thumb_folder):
            os.mkdir(self.thumb_folder)
        self.config_file = os.path.join(os.getcwd(), "config.cfg")
        if not os.path.isfile(self.config_file):
            self.cfg = {"folder": "", "pitch": False, "color": 0, 
                            "thumb1": 160, "thumb2": 80, "size": (900, 700)}
            try:
                with open(self.config_file, "w") as objf:
                    pickle.dump(self.cfg, objf)
            except Exception, why:
                print "Erreur de sauvegarde du fichier config.cfg :", why
        self.update_gui()
        if self.cfg.has_key("size"):
            MainWindow.resize(self.cfg["size"][0], self.cfg["size"][1])
        self.arte = None
        self.stop = False
        #self.prog_val = 0
        #self.populate()

    def nihil(self):
        pass
    #---------------------------------------
    # Events
    #---------------------------------------

    def closeEvent(self, event=None):
        """Quiet exit. """
        if self.active_download:
            mssg = QtGui.QMessageBox()
            mssg.setIcon(QtGui.QMessageBox.Question)
            mssg.setText(u"Un téléchargement est en cours.")
            mssg.setInformativeText(u"Désirez-vous interrompre le transfert ?")
            can = QtGui.QPushButton("Annuler")
            mssg.addButton(can, QtGui.QMessageBox.ActionRole)
            qut = QtGui.QPushButton("Quitter")
            mssg.addButton(qut, QtGui.QMessageBox.ActionRole)
            mssg.setDefaultButton(can)
            reply = mssg.exec_()
            if reply == 0:
                if event:
                    event.accept()
                    return
            self.cancel()
            time.sleep(1)
            
        if self.index:
            try:
                with open(self.thumb_folder + "/index", "w") as objfile:
                    pickle.dump(self.index, objfile)
            except IOError:
                pass
        try:
            with open(self.config_file, "w") as objf:
                pickle.dump(self.cfg, objf)
        except IOError, why:
            print "Error with config.cfg :", why
        QtCore.QCoreApplication.processEvents()
        time.sleep(0.1)
        sys.exit()


    def select_video(self, new, old):
        """Select an item in selected video list.

        Keyword arguments:
        new -- new item selected
        old -- old item selected
        """
        self.set_buttons(True)

    def selection_changed(self, item):
        """Click on an item in selected video list.

        Keyword arguments:
        item -- item clicked
        """
        if not self.list_dwnld.selectedItems():
            self.set_buttons(False)

    def move_item(self, item):
        """Item in preview windows has double-clicked.

        When an item in preview is double-clicked, he's selected for
        download.

        Keyword arguments:
        item -- item double-clicked
        """
        #print "Item :", item
        idx = self.items.index(item)
        self.list_dwnld.add_object(idx)

    #---------------------------------------

    def update_gui(self):
        try:
            with open("config.cfg", "r") as objf:
                c = pickle.load(objf)
        except:
            print "Fichier 'config.cfg' introuvable"
        else:
            self.cfg = c
        style = "".join(["QWidget {color: white; background: ", 
                                    self.colors[self.cfg["color"]], "}"])
        self.preview.setStyleSheet(style)
        self.preview.setIconSize(QtCore.QSize(self.cfg["thumb1"], self.cfg["thumb1"]))
        self.list_dwnld.setIconSize(QtCore.QSize(self.cfg["thumb2"], self.cfg["thumb2"]))
        #QtCore.QSize(160, 160))

    def populate(self):
        """Show available movies in preview window.

        liststore = [[title, date, url movie, url thumbnail], [], ...]
        """
        #print "Populate ..."
        self.editor.append("    Lecture des contenus ...")
        if os.path.isfile(self.thumb_folder + "/index"):
            # Load index of pitchs
            try:
                with open(self.thumb_folder + "/index", "r") as objfile:
                    self.index = pickle.load(objfile)
            except IOError:
                self.index = {}
        else:
           self.index = {} 

        self.liststore = []
        self.sgl = Signal()
        self.sgl.bind(self)
        f = open ("database", "r")
        for line in f:
            t = line.split(";")
            t[0] = self.str_to_unicode(t[0])
            self.liststore.append([t[0], t[1], t[2], t[3]])
        self.items = []
        self.videos = []
        self.counter = 0
        item = self.liststore[0]
        self.thumb = os.path.join(self.thumb_folder, item[1] + ".jpg")
        if not os.path.isfile(self.thumb):
            #print "No thumb"
            img_ldr = ImageLoader(self, item[3])
            img_ldr.start()
        else:
            self.next_thumbnail(self.thumb)
        


    def next_thumbnail(self, thumb=None):
        video_item = VideoItem(self.liststore[self.counter])
        if thumb == None:
            shutil.copy("image.jpg", self.thumb)
 
        img = QtGui.QPixmap(self.thumb)
        pix = img.scaled(160, 160, QtCore.Qt.KeepAspectRatio, 
                                QtCore.Qt.FastTransformation)
        video_item.pixmap = pix
        
        item = QtGui.QListWidgetItem(self.preview)
        item.setIcon(QtGui.QIcon(pix))
        text = self.set_thumbnail_text(video_item.title)
        item.setText(text)
        item.setTextAlignment(QtCore.Qt.AlignHCenter)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        item.setToolTip(u"Right click for show the pitch.")
        QtCore.QCoreApplication.processEvents()
        self.items.append(item)
        self.videos.append(video_item)

        self.counter += 1
        if not len(self.liststore) == self.counter:
            self.thumb = os.path.join(self.thumb_folder, 
                                    self.liststore[self.counter][1] + ".jpg")
            if not os.path.isfile(self.thumb):
                img_ldr = ImageLoader(self, self.liststore[self.counter][3])
                img_ldr.start()
            else:
                self.next_thumbnail(self.thumb)
        else:
            self.editor.clear()
            return True



    def set_thumbnail_text(self, txt):
        """Format the movie's title.

        Keyword argument :
        txt -- title (unicode)
        """
        f = txt
        if len(txt) > 40:
            f = "".join([txt[:21], "\n", txt[21:41], "\n", txt[41:]])
        elif len(txt) > 20:
            f = "".join([txt[:20], "\n", txt[20:]])
        return f


    def str_to_unicode(self, obj, encoding='utf-8'):
        if isinstance(obj, basestring):
            if not isinstance(obj, unicode):
                obj = unicode(obj, encoding)
            return obj
        else:
            return False


    def show_pitch(self):
        dureeRE = re.compile('[^0-9]*([0-9]+)(mn|min)')
        idx = self.items.index(self.preview.selectedItems()[0])
        self.editor.clear()
        font = self.editor.font()

        if not self.videos[idx].pitch:
            try:
                datas = self.index[self.liststore[idx][1]]
            except KeyError:
                page = urllib2.urlopen(self.liststore[idx][2]).read()
                soup = BS.BeautifulSoup( page )
                base_node = soup.find('div', {"class":"recentTracksCont"})
                data_resume = u""

                for i in base_node.findAll('p'):
                    if len(data_resume) != 0:
                        data_resume += "\n"
                    try:
                        data_resume += BS.BeautifulStoneSoup(i.string, 
                                        convertEntities=BS.BeautifulStoneSoup
                                        .HTML_ENTITIES).contents[0]
                        if i["class"] == "accroche":
                            data_resume += "\n"
                    except:
                        pass

                time = dureeRE.search(page).group(1)
                datas = (data_resume, time)
                self.index[self.liststore[idx][1]] = datas

            self.videos[idx].pitch = datas[0]
            self.videos[idx].time = datas[1]

        font.setPointSize(font.pointSize()+1)
        font.setBold(True)
        self.editor.setCurrentFont(font)
        
        self.editor.append(self.videos[idx].title)

        font.setPointSize(font.pointSize()-1)
        font.setBold(False)
        self.editor.setCurrentFont(font) 
        t = "".join([self.videos[idx].date, 
                        u"   durée : ", self.videos[idx].time, " min.\n"])
        self.editor.append(t)
        self.editor.append(self.videos[idx].pitch)
        self.editor.verticalScrollBar().setValue(0)

        # Need to return False for drag and drop
        return False


    def download_notify(self, state):
        """Print, in the text editor, the download status.

        Keyword arguments:
        state -- status of downloadind : 1 : begin
                                         2 : completed
                                         3 : cancel
                                       str : error
        """
        if state == 1:
            title = self.list_dwnld.item(0).text()
            title.replace("\n", "")
            self.editor.append(u"Téléchargement de " + title + " ....")            
        elif state == 2:
            item = self.list_dwnld.item(0)
            self.list_dwnld.takeItem(0)
            self.list_dwnld.lst_movies.pop(0)
            del item
            self.editor.insertPlainText(u" terminé.")
            self.active_download = False
        elif state == 3:
            self.editor.insertPlainText(u" interrompu.")
            self.editor.append(u"Téléchargements annulés.")
            self.active_download = False
        elif isinstance(state, str):
            self.editor.insert(u" échec. Cause : " + state)
            self.active_download = False
        
    def progress_notify(self, val):
        """Update progress bar

        """
        self.prog_bar.setValue(val)


    #---------------------------------------
    # Tool buttons
    #---------------------------------------

    def add_video(self):
        #print "Add video"
        try:
            idx = self.items.index(self.preview.selectedItems()[0])
            self.list_dwnld.add_object(idx)
        except:
            pass


    def remove_video(self):
        #print "Remove"
        sel = self.list_dwnld.selectedItems()
        if self.active_download in sel:
            sel.remove(self.active_download)

        l = []
        for s in sel:
            l.append(self.list_dwnld.row(s))
        l.sort()
        l.reverse()

        for i in l:
            item = self.list_dwnld.item(i)
            self.list_dwnld.takeItem(i)
            self.list_dwnld.lst_movies.pop(i)
            del item

    def print_list(self):
        """Debug function"""
        for i in self.list_dwnld.lst_movies:
            print i
        print "\n"


    def move_up(self):
        #print "Move up"
        sel = self.list_dwnld.selectedItems()
        if not sel:
            return
        rows = []
        for s in sel:
            rows.append(self.list_dwnld.row(s))
        rows.sort()

        for r in rows:
            if r == 0:
                continue
            item = self.list_dwnld.item(r)
            self.list_dwnld.takeItem(r)
            self.list_dwnld.insertItem(r-1, item)             
            self.list_dwnld.lst_movies.insert(r-1, 
                                    self.list_dwnld.lst_movies.pop(r))
            item.setSelected(True)

    def move_down(self):
        #print "Move down"
        sel = self.list_dwnld.selectedItems()
        if not sel:
            return
        rows = []
        for s in sel:
            rows.append(self.list_dwnld.row(s))
        rows.sort()
        rows.reverse()

        for r in rows:
            if r == self.list_dwnld.count():
                continue
            item = self.list_dwnld.item(r)
            self.list_dwnld.takeItem(r)
            self.list_dwnld.insertItem(r+1, item)             
            self.list_dwnld.lst_movies.insert(r+1, self.list_dwnld.lst_movies.pop(r))
            item.setSelected(True)


    def download(self):
        print "Download"
        #liststore = [[title, date, url movie, url thumbnail], [], ...]
        self.downloads = []
        self.list_dwnld.clearSelection()
        for i in self.list_dwnld.lst_movies:
            for j in self.liststore:
                if i == j[2]:
                    self.downloads.append(j)
        movie_ldr = MovieLoader(self, self.arte, self.downloads)
        movie_ldr.start()


    def cancel(self):
        #print "Cancel"
        self.arte.abort_dwnld = True
        self.stop = True
        return


    def record_pitch(self):
        print "Save texte"

    def reconnect(self):
        self.arte.refresh()

    def set_settings(self):
        Dialog = QtGui.QDialog()
        sett = Setting()
        sett.setupUi(Dialog)
        reply = Dialog.exec_()
        if reply == 1:
            self.update_gui()



    #---------------------------------------
    # Warnings
    #---------------------------------------

    def on_error_data(self, msg):
        print "Error with database :", msg


    #---------------------------------------
    # Household tasks
    #---------------------------------------
            
    def set_buttons(self, b):
        """Set enable or desable tool buttons.

        Keyword arguments:
        b -- boolean
        """
        self.remove_btn.setEnabled(b)
        self.up_btn.setEnabled(b)
        self.down_btn.setEnabled(b)

    def cleaning(self):
        clean = Cleaner(self)
        clean.start()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", 
                        "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Options.setTitle(QtGui.QApplication.translate("MainWindow", 
                        "&Options", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", 
                        "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("MainWindow",
                        "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.add_btn.setStatusTip(QtGui.QApplication.translate("MainWindow", 
                        "Add the selected video.", None, 
                        QtGui.QApplication.UnicodeUTF8))
        self.remove_btn.setStatusTip(QtGui.QApplication.translate("MainWindow", 
                        "Remove selected video(s) from the list", None, 
                        QtGui.QApplication.UnicodeUTF8))
        self.up_btn.setStatusTip(QtGui.QApplication.translate("MainWindow", 
                        "Move up.", None, QtGui.QApplication.UnicodeUTF8))
        self.down_btn.setStatusTip(QtGui.QApplication.translate("MainWindow", 
                        "move down", None, QtGui.QApplication.UnicodeUTF8))
        self.download_btn.setStatusTip(QtGui.QApplication.translate(
                        "MainWindow", "Download now", None, 
                        QtGui.QApplication.UnicodeUTF8))
        self.cancel_btn.setStatusTip(QtGui.QApplication.translate("MainWindow", 
                        "Abort download", None, 
                        QtGui.QApplication.UnicodeUTF8))
        self.save_pitch_btn.setStatusTip(QtGui.QApplication.translate(
                        "MainWindow", "Save the pitch.", None, 
                        QtGui.QApplication.UnicodeUTF8))
        self.action_Settings.setText(QtGui.QApplication.translate("MainWindow", 
                        "&Préferences", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Connection.setText(QtGui.QApplication.translate("MainWindow", 
                        "&Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", 
                        "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Download.setText(QtGui.QApplication.translate("MainWindow", 
                        "&Download", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Cancel.setText(QtGui.QApplication.translate("MainWindow", 
                        "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", 
                        "&Quit", None, QtGui.QApplication.UnicodeUTF8))



class Preview(QtGui.QListWidget):
    def __init__(self, ui, mw, parent=None):
        super(Preview, self).__init__(parent)
        self.ui = ui
        self.mw = mw
        self.setStyleSheet("QWidget {color: white; background: black}")
        self.setDragEnabled(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setIconSize(QtCore.QSize(160, 160))
        self.setFlow(QtGui.QListView.LeftToRight)
        self.setViewMode(QtGui.QListView.IconMode)

        #self.itemDoubleClicked.connect(ui.move_item)
    

    def startDrag(self, event):
        #print "Mouse press event"
        it = self.itemAt(event.pos())
        idx = self.ui.items.index(it)
        if not it:
            return

        mimeData = QtCore.QMimeData()
        mimeData.setText(str(idx))

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = QtGui.QPixmap(self.ui.videos[idx].pixmap)
        drag.setPixmap(pixmap)
        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()))
        drag.setPixmap(pixmap)
        result = drag.start(QtCore.Qt.MoveAction)


    def mouseMoveEvent(self, event):
        self.startDrag(event)
        event.accept()

    def mousePressEvent(self, event):
        if not self.itemAt(event.pos()):
            self.clearSelection()
            self.ui.add_btn.setEnabled(False)
            event.accept()
        elif event.button() == 1:
            self.itemAt(event.pos()).setSelected(True)
            self.ui.add_btn.setEnabled(True)
            event.accept()            
        elif event.button() == 2:
            self.itemAt(event.pos()).setSelected(True)
            self.ui.show_pitch()
            event.accept()
        else:
            event.ignore()

    def mouseDoubleClickEvent(self, event):
        if self.itemAt(event.pos()):
            self.ui.move_item(self.itemAt(event.pos()))
            event.accept()
        else:
            event.ignore()
            


    def keyPressEvent(self, event):
        print "Key :", event.key()


    def resizeEvent(self, event):
        s = self.spacing()
        self.setSpacing(s)
        self.updateGeometries()
        w, h = self.mw.size().width(), self.mw.size().height()
        try:
            # At launching ui.cfg don't exist
            self.ui.cfg["size"] = (w, h)
        except:
            pass
        event.ignore()



class ListDwnld(QtGui.QListWidget):
    def __init__(self, ui, parent=None):
        super(ListDwnld, self).__init__(parent)
        self.ui = ui
        self.setBaseSize(QtCore.QSize(150, 0))
        self.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtGui.QAbstractItemView
                                    .MultiSelection)
        self.setIconSize(QtCore.QSize(80, 80))
        self.lst_movies = []

        self.currentItemChanged.connect(self.ui.select_video)
        self.itemClicked.connect(self.ui.selection_changed)


    def mousePressEvent(self, event):
        if not self.itemAt(event.pos()):
            self.clearSelection()
            self.ui.set_buttons(False)
            event.accept()
        else:
            self.itemAt(event.pos()).setSelected(True)
            self.ui.set_buttons(True)
            event.ignore()


    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()


    def dragLeaveEvent(self, event):
        #print "Leave event"
        pass


    def dropEvent(self, event):
        data = event.mimeData()
        self.add_object(data.text())
        event.accept()

    def add_object(self, item):
        #print "Item : ", item, type(item)
        idx = eval(str(item))
        img = self.ui.videos[idx].pixmap
        text = self.ui.set_thumbnail_text(self.ui.videos[idx].title)
        pix = img.scaled(100, 100, QtCore.Qt.KeepAspectRatio, 
                                QtCore.Qt.FastTransformation)
        item = QtGui.QListWidgetItem(self)
        item.setIcon(QtGui.QIcon(pix))
        item.setText(text)
        item.setTextAlignment(QtCore.Qt.AlignHCenter)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.lst_movies.append(self.ui.videos[idx].url)
        #print "File added :", ui.videos[idx].url


class VideoItem(QtCore.QObject):
    """Class of video item.

    Each video available on the site is instance of this class.
    """
    def __init__(self, item):
        self.title = item[0]
        self.date = item[1]
        self.url = item[2]
        self.thumbnail = item[3]
        self.pitch = ""


class Signal(QtCore.QObject):
    """Signal used by ImageLoader.

    This signal is used by ImageLoader when a downloading of 
    thumbnail is completed.
    """
    loadFinished = QtCore.pyqtSignal()

    def bind(self, w):
        self.w = w
        self.loadFinished.connect(self.next)

    def emit_signal(self):
        self.loadFinished.emit() 

    def next(self):
        self.w.next_thumbnail()


class ImageLoader(Thread):
    """Thumbnail loader.

    """
    def __init__(self, ui, url):
        self.url = url
        self.ui = ui
        Thread.__init__(self)

    def run(self):
        with open("image.jpg", 'wb') as objfile:
            f = urllib2.urlopen(self.url)
            objfile.write(f.read())
        self.ui.sgl.emit_signal()



class MovieLoader(Thread):
    """Movie loader.

    """
    def __init__(self, ui, arte, movies):
        self.ui = ui
        self.arte = arte
        self.movies = movies
        Thread.__init__(self)


    def run(self):
        self.arte.on_telecharge(self.movies)
        while 1:
            if self.ui.stop:
                break
            time.sleep(2)

class Cleaner(Thread):
    """Cleaner for thumbnail folder and file index.

    """
    def __init__(self, ui,):
        self.thumb = ui.thumb_folder
        self.limit = time.mktime(time.localtime()) - (7 * 24 * 60 * 60)
        self.month = ["jan.", "fev.", "mar.", "avr.", "mai", "jui.", "juil.", "aout", "sep.", "oct.", "nov.", "dec."]
        Thread.__init__(self)

    def run(self):
        x = 0
        fl = os.path.join(self.thumb, "index")
        try:
            with open(fl, "r") as objf:
                dindex = pickle.load(objf)
        except:
            dindex = {}
        dk = dindex.keys()
        for t in os.listdir(self.thumb):
            if t == "index":
                continue
            date = os.path.splitext(t)[0]
            lst = date.split(" ")
            lst[1] = self.month.index(lst[1]) + 1
            lst[2] = lst[2][:-1]
            hm = lst.pop(3)
            lhm = hm.split("h")
            lst.append(lhm[0])
            lst.append(lhm[1])
            dt = " ".join([str(i) for i in lst])
            stt =  time.strptime(dt, "%Y %m %d %H %M")
            since_epoch = time.mktime(stt)
            if since_epoch < self.limit:
                if date in dk:
                    del dindex[date]   
                os.remove(os.path.join(self.thumb, t))
                x += 1
        try:
            with open(fl, "w") as objf:
                pickle.dump(dindex, objf)
        except Exception, why:
            print "Error in cleaner :", why
        

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    sys.exit(app.exec_())

