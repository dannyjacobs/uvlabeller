# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flagging_view.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(761, 531)
        self.widget = QtWidgets.QWidget(Frame)
        self.widget.setGeometry(QtCore.QRect(10, 50, 731, 461))
        self.widget.setObjectName("widget")
        self.layoutWidget = QtWidgets.QWidget(Frame)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 731, 38))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.c_box_file_3 = QtWidgets.QComboBox(self.layoutWidget)
        self.c_box_file_3.setObjectName("c_box_file_3")
        self.horizontalLayout_6.addWidget(self.c_box_file_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.c_box_a1_3 = QtWidgets.QComboBox(self.layoutWidget)
        self.c_box_a1_3.setObjectName("c_box_a1_3")
        self.horizontalLayout_7.addWidget(self.c_box_a1_3)
        self.c_box_a2_3 = QtWidgets.QComboBox(self.layoutWidget)
        self.c_box_a2_3.setObjectName("c_box_a2_3")
        self.horizontalLayout_7.addWidget(self.c_box_a2_3)
        self.c_box_pol_3 = QtWidgets.QComboBox(self.layoutWidget)
        self.c_box_pol_3.setObjectName("c_box_pol_3")
        self.horizontalLayout_7.addWidget(self.c_box_pol_3)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_7)

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

