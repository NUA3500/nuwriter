# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ma35d1Writer.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(561, 423)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/320px-Nuvoton.png"))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("QTabWidget::pane { /* The tab widget frame */\n"
"     border-top: 1px solid #C2C7CB;\n"
"     position: absolute;\n"
"     top: -0.5em;\n"
"     background: white;\n"
" }\n"
"\n"
" QTabWidget::tab-bar {\n"
"     alignment: center;\n"
" }\n"
"\n"
" /* Style the tab using the tab sub-control. Note that\n"
"     it reads QTabBar _not_ QTabWidget */\n"
" QTabBar::tab {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"     border: 1px solid #C4C4C3;\n"
"     border-bottom-color: #C2C7CB; /* same as the pane color */\n"
"     min-width: 8ex;\n"
"     padding: 3px 15px;\n"
" }\n"
"\n"
" QTabBar::tab:selected, QTabBar::tab:hover {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #fafafa, stop: 0.4 #f4f4f4,\n"
"                                 stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);\n"
" }\n"
"\n"
" QTabBar::tab:selected {\n"
"     border-color:#C4C4C3;\n"
"\n"
" }")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.AttachTab = QtWidgets.QWidget()
        self.AttachTab.setObjectName("AttachTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.AttachTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.AttachTab)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.browseDDR_btn = QtWidgets.QPushButton(self.groupBox)
        self.browseDDR_btn.setObjectName("browseDDR_btn")
        self.gridLayout_2.addWidget(self.browseDDR_btn, 0, 3, 1, 1)
        self.ddrFileLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.ddrFileLineEdit.setFrame(True)
        self.ddrFileLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.ddrFileLineEdit.setCursorPosition(0)
        self.ddrFileLineEdit.setPlaceholderText("")
        self.ddrFileLineEdit.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.ddrFileLineEdit.setObjectName("ddrFileLineEdit")
        self.gridLayout_2.addWidget(self.ddrFileLineEdit, 0, 2, 1, 1)
        self.verticalLayout_8.addLayout(self.gridLayout_2)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem4)
        self.attach_btn = QtWidgets.QPushButton(self.AttachTab)
        self.attach_btn.setMinimumSize(QtCore.QSize(82, 28))
        self.attach_btn.setStyleSheet("")
        self.attach_btn.setDefault(True)
        self.attach_btn.setFlat(False)
        self.attach_btn.setObjectName("attach_btn")
        self.verticalLayout_4.addWidget(self.attach_btn)
        self.tabWidget.addTab(self.AttachTab, "")
        self.DownloadTab = QtWidgets.QWidget()
        self.DownloadTab.setObjectName("DownloadTab")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.DownloadTab)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tabMedia = QtWidgets.QTabWidget(self.DownloadTab)
        self.tabMedia.setObjectName("tabMedia")
        self.verticalLayout_5.addWidget(self.tabMedia)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.tabWidget.addTab(self.DownloadTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 561, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionLicense = QtWidgets.QAction(MainWindow)
        self.actionLicense.setObjectName("actionLicense")
        self.actionOptions = QtWidgets.QAction(MainWindow)
        self.actionOptions.setObjectName("actionOptions")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionLicense)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.tabMedia.setCurrentIndex(-1)
        self.ddrFileLineEdit.returnPressed.connect(self.attach_btn.click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Call setWindowTitle"))
        self.groupBox.setTitle(_translate("MainWindow", "DDR initialize code"))
        self.label_2.setText(_translate("MainWindow", "DDR File:"))
        self.browseDDR_btn.setText(_translate("MainWindow", "Browse"))
        self.attach_btn.setText(_translate("MainWindow", "Attach"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.AttachTab), _translate("MainWindow", "Attach"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DownloadTab), _translate("MainWindow", "Download"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionHelp.setText(_translate("MainWindow", "About"))
        self.actionLicense.setText(_translate("MainWindow", "License"))
        self.actionOptions.setText(_translate("MainWindow", "Options"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
import nuvoton_rc
