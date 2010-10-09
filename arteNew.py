# -*- coding: utf-8 -*-

# arteNew.py
#
# Date: Mon Oct  4 2010     
# Author : Vincent Vande Vyvre <vins@swing.be>
# Version 0.1
# Revision 2
#
# Graphical user's interface for Arte7Recorder version Qt
#
# arte7recorder https://launchpad.net/~arte+7recorder
# qtarte https://code.launchpad.net/~arte+7recorder/+junk/qtarte
#
# Warning : Use this script only for testing



import os
import shutil
import pickle
import glob
import time
import urllib2
import re
from threading import Thread
import BeautifulSoup as BS

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
        self.preview = Preview(self.splitter)

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
        self.list_dwnld = ListDwnld(self.dockWidgetContents)
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
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tool_panel.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.tool_panel)
        self.action_Folder = QtGui.QAction(MainWindow)
        self.action_Index = QtGui.QAction(MainWindow)
        self.action_Connection = QtGui.QAction(MainWindow)
        self.action_About = QtGui.QAction(MainWindow)
        self.action_Download = QtGui.QAction(MainWindow)
        self.action_Cancel = QtGui.QAction(MainWindow)
        self.action_Quit = QtGui.QAction(MainWindow)
        self.menu_Options.addAction(self.action_Folder)
        self.menu_Options.addAction(self.action_Index)
        self.menu_File.addAction(self.action_Connection)
        self.menu_File.addAction(self.action_Download)
        self.menu_File.addAction(self.action_Cancel) 
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_Help.addAction(self.action_About)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Options.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()
        QtCore.QCoreApplication.processEvents()
        MainWindow.closeEvent = self.closeEvent

        self.add_btn.clicked.connect(self.add_video)
        self.remove_btn.clicked.connect(self.remove_video)
        self.up_btn.clicked.connect(self.move_up)
        self.down_btn.clicked.connect(self.move_down)
        self.download_btn.clicked.connect(self.download)
        self.cancel_btn.clicked.connect(self.cancel)
        self.save_pitch_btn.clicked.connect(self.record_pitch)

        self.set_buttons(False)
        self.add_btn.setEnabled(False)
        self.active_download = False
        self.thumb_folder = os.path.join(os.getcwd(), "thumbnails")
        self.populate()


    #---------------------------------------
    # Events
    #---------------------------------------

    def closeEvent(self,event):
        """Quiet exit. """
        if self.index:
            try:
                with open(self.thumb_folder + "/index", "w") as objfile:
                    pickle.dump(self.index, objfile)
            except IOError:
                pass
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



    def populate(self):
        """Show available movies in preview window.

        """
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
            img_ldr = ImageLoader(item[3])
            img_ldr.start()
        else:
            self.next_thumbnail(self.thumb)
        


    def next_thumbnail(self, thumb=None):
        #print "len :", len(self.liststore), self.counter, thumb
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
                #print "No thumb"
                img_ldr = ImageLoader(self.liststore[self.counter][3])
                img_ldr.start()
            else:
                self.next_thumbnail(self.thumb)



    def set_thumbnail_text(self, txt):
        """Format the movie's title.

        Keyword argument :
        txt -- title (unicode)
        """
        f = txt
        if len(txt) > 20:
            f = "".join([txt[:20], "\n", txt[20:]])
        elif len(txt) > 40:
            f = "".join([txt[:21], "\n", txt[21:41], "\n", txt[41:]])
        return f


    def str_to_unicode(self, obj, encoding='utf-8'):
        if isinstance(obj, basestring):
            if not isinstance(obj, unicode):
                obj = unicode(obj, encoding)
            return obj
        else:
            return False


    def show_pitch(self):
        #print "select:", self.preview.selectedItems()
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

            #print "data_resume :", data_resume
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
        #self.print_list()
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
        #self.print_list()

    def move_down(self):
        #print "Move down"
        sel = self.list_dwnld.selectedItems()
        if not sel:
            return
        #self.print_list()
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
        #self.print_list()


    def download(self):
        print "Download"

    def cancel(self):
        print "Cancel"

    def record_pitch(self):
        print "Save texte"


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
        self.action_Folder.setText(QtGui.QApplication.translate("MainWindow", 
                        "&Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Index.setText(QtGui.QApplication.translate("MainWindow", 
                        "&Index", None, QtGui.QApplication.UnicodeUTF8))
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
    def __init__(self, parent=None):
        super(Preview, self).__init__(parent)
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
        idx = ui.items.index(it)
        if not it:
            return

        mimeData = QtCore.QMimeData()
        mimeData.setText(str(idx))

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = QtGui.QPixmap(ui.videos[idx].pixmap)
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
            ui.add_btn.setEnabled(False)
            event.accept()
        elif event.button() == 1:
            self.itemAt(event.pos()).setSelected(True)
            ui.add_btn.setEnabled(True)
            event.accept()            
        elif event.button() == 2:
            self.itemAt(event.pos()).setSelected(True)
            ui.show_pitch()
            event.accept()
        else:
            event.ignore()

    def mouseDoubleClickEvent(self, event):
        if self.itemAt(event.pos()):
            ui.move_item(self.itemAt(event.pos()))
            event.accept()
        else:
            event.ignore()
            


    def keyPressEvent(self, event):
        print "Key :", event.key()


    def resizeEvent(self, event):
        s = self.spacing()
        self.setSpacing(s)
        self.updateGeometries() 
        event.accept()



class ListDwnld(QtGui.QListWidget):
    def __init__(self, parent=None):
        super(ListDwnld, self).__init__(parent)
        self.setBaseSize(QtCore.QSize(150, 0))
        self.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtGui.QAbstractItemView
                                    .MultiSelection)
        self.setIconSize(QtCore.QSize(100, 100))
        self.lst_movies = []

        self.currentItemChanged.connect(ui.select_video)
        self.itemClicked.connect(ui.selection_changed)


    def mousePressEvent(self, event):
        if not self.itemAt(event.pos()):
            self.clearSelection()
            ui.set_buttons(False)
            event.accept()
        else:
            self.itemAt(event.pos()).setSelected(True)
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
        img = ui.videos[idx].pixmap
        pix = img.scaled(100, 100, QtCore.Qt.KeepAspectRatio, 
                                QtCore.Qt.FastTransformation)
        item = QtGui.QListWidgetItem(self)
        item.setIcon(QtGui.QIcon(pix))
        item.setText(ui.videos[idx].title)
        item.setTextAlignment(QtCore.Qt.AlignHCenter)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.lst_movies.append(ui.videos[idx].url)
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
    def __init__(self, url):
        self.url = url
        Thread.__init__(self)

    def run(self):
        with open("image.jpg", 'wb') as objfile:
            f = urllib2.urlopen(self.url)
            objfile.write(f.read())
        ui.sgl.emit_signal()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    sys.exit(app.exec_())

