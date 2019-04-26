# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'labelling_view.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(761, 531)
        self.layoutWidget = QtWidgets.QWidget(Frame)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 731, 38))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.c_box_file = QtWidgets.QComboBox(self.layoutWidget)
        self.c_box_file.setObjectName("c_box_file")
        self.horizontalLayout_3.addWidget(self.c_box_file)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.c_box_a1 = QtWidgets.QComboBox(self.layoutWidget)
        self.c_box_a1.setObjectName("c_box_a1")
        self.horizontalLayout_2.addWidget(self.c_box_a1)
        self.c_box_a2 = QtWidgets.QComboBox(self.layoutWidget)
        self.c_box_a2.setObjectName("c_box_a2")
        self.horizontalLayout_2.addWidget(self.c_box_a2)
        self.c_box_pol = QtWidgets.QComboBox(self.layoutWidget)
        self.c_box_pol.setObjectName("c_box_pol")
        self.horizontalLayout_2.addWidget(self.c_box_pol)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.widget = QtWidgets.QWidget(Frame)
        self.widget.setGeometry(QtCore.QRect(20, 60, 561, 301))
        self.widget.setObjectName("widget")
        self.textEdit = QtWidgets.QTextEdit(Frame)
        self.textEdit.setGeometry(QtCore.QRect(20, 390, 561, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(Frame)
        self.textEdit_2.setGeometry(QtCore.QRect(20, 440, 561, 81))
        self.textEdit_2.setObjectName("textEdit_2")
        self.treeWidget = QtWidgets.QTreeWidget(Frame)
        self.treeWidget.setGeometry(QtCore.QRect(590, 60, 161, 461))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())

