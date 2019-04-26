# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
import default_view as mainview
import labelling_view as labelview

class Ui_MainWindow( QObject ):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 10, 761, 531))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.curr_ui = mainview.Ui_Frame()
        self.curr_ui.setupUi(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_UV_file = QtWidgets.QAction(MainWindow)
        self.actionOpen_UV_file.setObjectName("actionOpen_UV_file")
        self.actionOpen_fits_miriad = QtWidgets.QAction(MainWindow)
        self.actionOpen_fits_miriad.setObjectName("actionOpen_fits_miriad")
        self.actionImport_labels = QtWidgets.QAction(MainWindow)
        self.actionImport_labels.setObjectName("actionImport_labels")
        self.actionImport_Flags = QtWidgets.QAction(MainWindow)
        self.actionImport_Flags.setObjectName("actionImport_Flags")
        self.actionExport_Labels = QtWidgets.QAction(MainWindow)
        self.actionExport_Labels.setObjectName("actionExport_Labels")
        self.actionExport_Labels_2 = QtWidgets.QAction(MainWindow)
        self.actionExport_Labels_2.setObjectName("actionExport_Labels_2")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionDefault = QtWidgets.QAction(MainWindow)
        self.actionDefault.setCheckable(True)
        self.actionDefault.setChecked(True)
        self.actionDefault.setObjectName("actionDefault")
        self.actionFlagger = QtWidgets.QAction(MainWindow)
        self.actionFlagger.setCheckable(True)
        self.actionFlagger.setChecked(False)
        self.actionFlagger.setEnabled(True)
        self.actionFlagger.setObjectName("actionFlagger")
        self.actionLabeller = QtWidgets.QAction(MainWindow)
        self.actionLabeller.setCheckable(True)
        self.actionLabeller.setObjectName("actionLabeller")
        self.menuFile.addAction(self.actionOpen_UV_file)
        self.menuFile.addAction(self.actionOpen_fits_miriad)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImport_labels)
        self.menuFile.addAction(self.actionImport_Flags)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_Labels)
        self.menuFile.addAction(self.actionExport_Labels_2)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuView.addAction(self.actionDefault)
        self.menuView.addAction(self.actionFlagger)
        self.menuView.addAction(self.actionLabeller)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UVLabel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionOpen_UV_file.setText(_translate("MainWindow", "Open UV file"))
        self.actionOpen_fits_miriad.setText(_translate("MainWindow", "Open fits, miriad..."))
        self.actionImport_labels.setText(_translate("MainWindow", "Import Flags"))
        self.actionImport_Flags.setText(_translate("MainWindow", "Import Labels"))
        self.actionExport_Labels.setText(_translate("MainWindow", "Export Flags"))
        self.actionExport_Labels_2.setText(_translate("MainWindow", "Export Labels"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionDefault.setText(_translate("MainWindow", "Default"))
        self.actionFlagger.setText(_translate("MainWindow", "Flagging"))
        self.actionLabeller.setText(_translate("MainWindow", "Labelling"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

