# -*- coding: utf-8 -*-

# setting.py
#
# Date: Mon Oct  10 2010     
# Author : Vincent Vande Vyvre <vins@swing.be>
#
# Option dialog box for Arte7Recorder version Qt
#
# arte7recorder : https://launchpad.net/~arte+7recorder
# qtarte : https://code.launchpad.net/~arte+7recorder/+junk/qtarte
#

import os
import sys
import pickle

from PyQt4 import QtCore, QtGui

class Setting(object):
    def setupUi(self, Dialog):
        Dialog.resize(464, 288)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.logo_lbl = QtGui.QLabel(Dialog)
        self.logo_lbl.setText("None")
        self.logo_lbl.setPixmap(QtGui.QPixmap("medias/icon.png"))
        self.horizontalLayout.addWidget(self.logo_lbl)
        self.title_fr = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans Mono")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.title_fr.setFont(font)
        self.horizontalLayout.addWidget(self.title_fr)
        spacerItem = QtGui.QSpacerItem(178, 20, QtGui.QSizePolicy.Expanding, 
                                QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.folder_lbl = QtGui.QLabel(Dialog)
        self.horizontalLayout_2.addWidget(self.folder_lbl)
        self.folder_edit = QtGui.QLineEdit(Dialog)
        self.folder_edit.setMinimumSize(QtCore.QSize(200, 0))
        self.horizontalLayout_2.addWidget(self.folder_edit)
        self.browse_btn = QtGui.QToolButton(Dialog)
        self.browse_btn.clicked.connect(self.get_folder)
        self.horizontalLayout_2.addWidget(self.browse_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.pitch_chb = QtGui.QCheckBox(Dialog)
        self.horizontalLayout_3.addWidget(self.pitch_chb)
        spacerItem1 = QtGui.QSpacerItem(118, 20, QtGui.QSizePolicy.Expanding, 
                                QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.bckgrnd_lbl = QtGui.QLabel(Dialog)
        self.horizontalLayout_4.addWidget(self.bckgrnd_lbl)
        self.bckgrnd_cmb = QtGui.QComboBox(Dialog)
        self.bckgrnd_cmb.setMinimumSize(QtCore.QSize(160, 0))
        self.horizontalLayout_4.addWidget(self.bckgrnd_cmb)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, 
                                QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.gridLayout = QtGui.QGridLayout()
        self.thumb1_lbl = QtGui.QLabel(Dialog)
        self.gridLayout.addWidget(self.thumb1_lbl, 0, 0, 1, 1)
        self.thumb1_spb = QtGui.QSpinBox(Dialog)
        self.thumb1_spb.setSuffix(" pxl")
        self.thumb1_spb.setMinimum(60)
        self.thumb1_spb.setMaximum(200)
        self.thumb1_spb.setProperty("value", 160)
        self.gridLayout.addWidget(self.thumb1_spb, 0, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, 
                                QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 2, 1, 1)
        self.thumb2_lbl = QtGui.QLabel(Dialog)
        self.gridLayout.addWidget(self.thumb2_lbl, 1, 0, 1, 1)
        self.thumb2_spb = QtGui.QSpinBox(Dialog)
        self.thumb2_spb.setSuffix(" pxl")
        self.thumb2_spb.setMinimum(60)
        self.thumb2_spb.setMaximum(200)
        self.thumb2_spb.setProperty("value", 80)
        self.gridLayout.addWidget(self.thumb2_spb, 1, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, 
                                QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel
                                |QtGui.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.dialog = Dialog

        self.retranslateUi(Dialog)
        self.set_color()
        self.get_config()
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), 
                                self.set_config)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), 
                                Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def get_config(self):
        try:
            with open("config.cfg", "r") as objf:
                self.cfg = pickle.load(objf)
        except:
            print "Fichier 'config.cfg' introuvable"
            self.cfg = {}
        else:
            self.folder_edit.setText(self.cfg["folder"])
            self.pitch_chb.setChecked(self.cfg["pitch"])
            self.bckgrnd_cmb.setCurrentIndex(self.cfg["color"])
            self.thumb1_spb.setValue(self.cfg["thumb1"])
            self.thumb2_spb.setValue(self.cfg["thumb2"])

    def set_config(self):
        self.cfg["folder"] = unicode(self.folder_edit.text())
        self.cfg["pitch"] = self.pitch_chb.isChecked()
        self.cfg["color"] = self.bckgrnd_cmb.currentIndex()
        self.cfg["thumb1"] = self.thumb1_spb.value()
        self.cfg["thumb2"] = self.thumb2_spb.value()
        try:
            with open("config.cfg", "w") as objf:
                pickle.dump(self.cfg, objf)
        except Exception, why:
            print "Erreur de sauvegarde du fichier config.cfg :", why
        self.dialog.accept()

    def get_folder(self):
        f = os.path.expanduser('~')
        d = unicode(QtGui.QFileDialog.getExistingDirectory(None, 
                            u"Choose destination folder", f, 
                            QtGui.QFileDialog.DontResolveSymlinks
                            | QtGui.QFileDialog.ShowDirsOnly))

        if os.path.isdir(d):
            self.folder_edit.setText(d)



    def set_color(self):
        colors = ["Black", "Blue",   
                    "Cyan", "Dark blue", 
                    "Dark cyan", "Dark grey",
                    "Dark green", "Dark magenta",
                    "Dark red", "Dark yellow",
                    "Grey", "Green", 
                    "Light grey", "Magenta", 
                    "Red", "White",
                    "Yellow"]

        ico_paths = ['medias/Qcolor_black.png', 'medias/Qcolor_blue.png',
                     'medias/Qcolor_cyan.png', 'medias/Qcolor_darkBlue.png',
                     'medias/Qcolor_darkCyan.png', 'medias/Qcolor_darkgrey.png',
                     'medias/Qcolor_darkGreen.png', 'medias/Qcolor_darkMagenta.png',
                     'medias/Qcolor_darkRed.png', 'medias/Qcolor_darkYellow.png',
                     'medias/Qcolor_grey.png', 'medias/Qcolor_green.png',
                     'medias/Qcolor_lightGrey.png', 'medias/Qcolor_magenta.png',
                     'medias/Qcolor_red.png', 'medias/Qcolor_white.png',
                     'medias/Qcolor_yellow.png']

        for i in range(0, 17):
            try:
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(ico_paths[i]), 
                            QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.bckgrnd_cmb.addItem(icon, colors[i])
            except Exception, why:
                print "No icon", why

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 
                                "arte7recorder", None, 
                                QtGui.QApplication.UnicodeUTF8))
        self.title_fr.setText(QtGui.QApplication.translate("Dialog", 
                                "Settings", None, 
                                QtGui.QApplication.UnicodeUTF8))
        self.folder_lbl.setText(QtGui.QApplication.translate("Dialog", 
                                "Videos folder :", None, 
                                QtGui.QApplication.UnicodeUTF8))
        self.browse_btn.setText(QtGui.QApplication.translate("Dialog", 
                                "Browser", None, 
                                QtGui.QApplication.UnicodeUTF8))
        self.pitch_chb.setText(QtGui.QApplication.translate("Dialog",   
                                "To record the summaries automatically.", 
                                None, QtGui.QApplication.UnicodeUTF8))
        self.bckgrnd_lbl.setText(QtGui.QApplication.translate("Dialog", 
                                "Background color :", None, 
                                QtGui.QApplication.UnicodeUTF8))
        self.thumb1_lbl.setText(QtGui.QApplication.translate("Dialog", 
                                "Size of preview's thumbnails :", None, 
                                QtGui.QApplication.UnicodeUTF8))
        self.thumb2_lbl.setText(QtGui.QApplication.translate("Dialog", 
                                "Size of basket's thumbnails :", None, 
                                QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Setting()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

