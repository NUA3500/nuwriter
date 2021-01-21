
from PyQt5 import QtWidgets, QtCore

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread

from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QFormLayout, QWidget)

import os

DEV_DDR_SRAM = 0
DEV_NAND = 1
DEV_SD_EMMC = 2
DEV_SPINOR = 3
DEV_SPINAND = 4
DEV_OTP = 6
DEV_USBH = 7
DEV_UNKNOWN = 0xFF

# Command options
OPT_NONE = 0
OPT_SCRUB = 1       # For erase, use with care
OPT_WITHBAD = 1     # For read
OPT_EXECUTE = 2     # For write
OPT_VERIFY = 3      # For write
OPT_UNPACK = 4      # For pack
OPT_RAW = 5         # For write
OPT_EJECT = 6      # For msc

# class SdEmmcPage(QWidget):
#     def __init__(self, media, parent=None):
#         super(SdEmmcPage, self).__init__(parent)

#         self._media = media


#         self.mainLayout = QVBoxLayout()

#         self.addWriteArgument()
#         self.addReadArgument()
#         self.addEraseArgument()

#         self.mainLayout.addStretch()

#         self.setLayout(self.mainLayout)
#         self.addOptions()


class SpiPage(QWidget):

    signalImgProgram = pyqtSignal(int, str, str, int, bool)
    signalImgRead = pyqtSignal(int, str, str, str, int, bool)
    signalImgErase = pyqtSignal(int, str, str, int, bool)

    def __init__(self, media, parent=None):
        super(SpiPage, self).__init__(parent)

        self.parent = parent
        self._media = media


        self.mainLayout = QVBoxLayout()

        self.addWriteArgument()
        self.addReadArgument()
        self.addEraseArgument()

        self.mainLayout.addStretch()

        self.setLayout(self.mainLayout)
        self.addOptions()

        if parent != None:
            self.signalImgRead.connect(parent.doImgRead)
            self.signalImgProgram.connect(parent.doImgProgram)
            self.signalImgErase.connect(parent.doImgErase)


    def onRadioToggled(self):

        if self.radioPack.isChecked():
            self.imgAddress.setEnabled(False)
        else:
            self.imgAddress.setEnabled(True)

    def addWriteArgument(self):
        imgBrowseButton = QPushButton('Browse')
        imgBrowseButton.clicked.connect(self.pathBrowse)

        self.imgPathLine = QLineEdit('')

        imgFileLayout = QHBoxLayout()
        imgFileLayout.addWidget(self.imgPathLine)
        imgFileLayout.addWidget(imgBrowseButton)

        self.radioData = QRadioButton("Data")
        self.radioPack = QRadioButton("Pack")

        self.radioPack.toggled.connect(self.onRadioToggled)
        self.radioPack.toggled.connect(self.onRadioToggled)

        imgTypeLayout = QHBoxLayout()
        imgTypeLayout.addWidget(self.radioData)
        imgTypeLayout.addWidget(self.radioPack)
        imgTypeLayout.addStretch()

        self.imgAddress = QLineEdit('')

        spiGroup = QGroupBox("Write")
        spiLayout = QFormLayout()
        spiLayout.addRow(QLabel("Image file"), imgFileLayout)
        spiLayout.addRow(QLabel("Image type"), imgTypeLayout)
        spiLayout.addRow(QLabel("Image addr."), self.imgAddress)

        # if option == OPT_RAW and media != DEV_NAND:
        #     raise ValueError(f"Do not support raw write on {str.upper(args.write[0])}")

        if self._media == DEV_NAND:
            self.normalWrite = QRadioButton('None')
            self.rawWrite = QRadioButton('Raw Write')
            self.verifyWrite = QRadioButton('Verify')
            _optLayout = QHBoxLayout()
            _optLayout.addWidget(self.normalWrite)
            _optLayout.addWidget(self.rawWrite)
            _optLayout.addWidget(self.verifyWrite)
            _optLayout.addStretch()
            spiLayout.addRow(QLabel("Option"), _optLayout)
        else:
            self.verifyWrite = QCheckBox('Verify')
            spiLayout.addRow(QLabel("Option"), self.verifyWrite)

        spiGroup.setLayout(spiLayout)
        self.mainLayout.addWidget(spiGroup)

    def addReadArgument(self):
        group = QGroupBox("Read")
        layout = QFormLayout()

        _fileLayout = QHBoxLayout()
        self.fileSave = QLineEdit('')
        browseButton = QPushButton('Browse')
        browseButton.clicked.connect(self.saveFile)
        _fileLayout.addWidget(self.fileSave)
        _fileLayout.addWidget(browseButton)

        _rangeLayout = QHBoxLayout()
        self.readStart = QLineEdit('')
        self.readEnd = QLineEdit('')
        self.readAll = QCheckBox('ALL')
        self.readAll.setVisible(False)

        self.readAll.stateChanged.connect(lambda checked: (self.readStart.setEnabled(not checked), self.readEnd.setEnabled(not checked)))

        _rangeLayout.addWidget(self.readStart)
        _rangeLayout.addWidget(QLabel("-"))
        _rangeLayout.addWidget(self.readEnd)
        _rangeLayout.addWidget(self.readAll)

        layout.addRow(QLabel("Save file"), _fileLayout)
        layout.addRow(QLabel("Range"), _rangeLayout)

        if self._media in [DEV_NAND, DEV_SPINAND]:
            self.readWithBad = QCheckBox('With Bad')
            layout.addRow(QLabel("Option"), self.readWithBad)

        group.setLayout(layout)
        self.mainLayout.addWidget(group)

    def addEraseArgument(self):
        group = QGroupBox("Erase")
        layout = QFormLayout()

        _rangeLayout = QHBoxLayout()
        self.eraseStart = QLineEdit('')
        self.eraseEnd = QLineEdit('')
        self.eraseAll = QCheckBox('ALL')

        self.eraseAll.stateChanged.connect(lambda checked: (self.eraseStart.setEnabled(not checked), self.eraseEnd.setEnabled(not checked)))

        _rangeLayout.addWidget(self.eraseStart)
        _rangeLayout.addWidget(QLabel("-"))
        _rangeLayout.addWidget(self.eraseEnd)
        _rangeLayout.addWidget(self.eraseAll)

        layout.addRow(QLabel("Range    "), _rangeLayout)

        group.setLayout(layout)
        self.mainLayout.addWidget(group)


    def addOptions(self):
        spiButtonLayout = QHBoxLayout()

        programButton = QPushButton('Write')
        programButton.clicked.connect(self.writeMedia)

        readButton = QPushButton('Read')
        readButton.clicked.connect(self.readMedia)

        eraseButton = QPushButton('Erase')
        eraseButton.clicked.connect(self.eraseMedia)

        spiButtonLayout.addWidget(programButton)
        spiButtonLayout.addWidget(readButton)
        spiButtonLayout.addWidget(eraseButton)

        spiButtonGroup = QGroupBox()
        spiButtonGroup.setLayout(spiButtonLayout)

        self.mainLayout.addWidget(spiButtonGroup)

    def writeMedia(self):
        _file = self.imgPathLine.text()
        _address = self.imgAddress.text()
        _media = self._media
        _ispack = self.radioPack.isChecked()

        _option = OPT_NONE

        if _media == DEV_NAND:
            if self.normalWrite.isChecked():
                _option = OPT_NONE
            elif self.rawWrite.isChecked():
                _option = OPT_RAW

        if self.verifyWrite.isChecked():
            _option = OPT_VERIFY

        self.signalImgProgram.emit(_media, _address , _file, _option, _ispack)

    def readMedia(self):
        _file = self.fileSave.text()
        _start = self.readStart.text()
        _end = self.readEnd.text()
        _media = self._media
        _isall = self.readAll.isChecked()

        _option = OPT_NONE

        if _media in [DEV_NAND, DEV_SPINAND] and self.readWithBad.isChecked():
            _option = OPT_WITHBAD

        self.signalImgRead.emit(_media, _start , _file, _end, _option, _isall)

    def eraseMedia(self):
        _start = self.eraseStart.text()
        _end = self.eraseEnd.text()
        _media = self._media
        _isall = self.eraseAll.isChecked()
        self.signalImgErase.emit(_media, _start , _end, 0, _isall)


    def pathBrowse(self):
        filename = ""
        # Fix for crash in X on Ubuntu 14.04
        filename, _ = QtWidgets.QFileDialog.getOpenFileName()

        if filename != "":
            self.imgPathLine.setText(filename)

        # if filename != "" and filename[-4:] in (".bin"):
        #     self.imgPathLine.setText(filename)
        # elif filename != "":
        #     msgBox = QtWidgets.QMessageBox()
        #     msgBox.setText("Wrong file extention. Must be .bin.")
        #     msgBox.exec_()
        # pass

    def saveFile(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                    "save file",
                                    os.getcwd(),
                                    "All Files (*)")

        if fileName != "":
            self.fileSave.setText(fileName)
            return

class DdrSramPage(QWidget):

    signalImgProgram = pyqtSignal(int, str, str, int, bool)

    def __init__(self, parent=None):
        super(DdrSramPage, self).__init__(parent)

        self.imgPathLine = QLineEdit('')
        self.imgAddress = QLineEdit('1000')
        self.optExecute = QCheckBox('Execute after download')

        imgFileLayout = QHBoxLayout()
        imgFileLayout.addWidget(self.imgPathLine)
        # imgFileLayout.addWidget(QPushButton('Browse'))
        imgBrowseButton = QPushButton('Browse')
        imgBrowseButton.clicked.connect(self.pathBrowse)
        imgFileLayout.addWidget(imgBrowseButton)

        optionLayout = QHBoxLayout()
        optionLayout.addWidget(self.optExecute)
        optionLayout.addStretch()

        progGroup = QGroupBox("Parameters")
        progLayout = QFormLayout()
        progLayout.addRow(QLabel("Image file"), imgFileLayout)
        progLayout.addRow(QLabel("Image addr."), self.imgAddress)

        progLayout.addRow(QLabel("Option"), optionLayout)

        progGroup.setLayout(progLayout)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(progGroup)
        self.mainLayout.addStretch()

        self.setLayout(self.mainLayout)
        self.addOptions()

    def pathBrowse(self):
        filename = ""
        # Fix for crash in X on Ubuntu 14.04
        filename, _ = QtWidgets.QFileDialog.getOpenFileName()
        if filename != "":
            self.imgPathLine.setText(filename)
        pass

    def addOptions(self):
        optionLayout = QHBoxLayout()

        programButton = QPushButton('Write')
        programButton.clicked.connect(self.writeDDR)

        # optionLayout.addStretch()
        optionLayout.addWidget(programButton)
        # optionLayout.addStretch()

        optionGroup = QGroupBox()
        optionGroup.setLayout(optionLayout)

        self.mainLayout.addWidget(optionGroup)

    def writeDDR(self):
        imgFile = self.imgPathLine.text()
        # With the 0x prefix, Python can distinguish hex and decimal automatically.
        # imgAddr = int(self.imgAddress.text(),0)
        imgAddr = self.imgAddress.text()

        # Command options
        # OPT_NONE = 0
        # OPT_EXECUTE = 2     # For write
        if self.optExecute.isChecked():
            option = 2
        else:
            option = 0

        # DEV_DDR_SRAM = 0
        media = 0
        self.signalImgProgram.emit(media, imgAddr , imgFile, option, False)

if __name__ == "__main__":
    class MainDialog(QDialog):
        def __init__(self, parent=None):
            super(MainDialog, self).__init__(parent)
            self.tabMedia = QTabWidget()

            # DDR/SRAM
            self.ddrPage = DdrSramPage()
            self.ddrPage.signalImgProgram.connect(self.doImgProgram)
            self.tabMedia.addTab(self.ddrPage, "DDR/SRAM")

            # NAND
            self.nandPage = SpiPage(DEV_NAND)
            self.tabMedia.addTab(self.nandPage, "NAND")
            self.nandPage.signalImgProgram.connect(self.doImgProgram)
            self.tabMedia.setCurrentIndex(1)


            mainLayout = QVBoxLayout()
            mainLayout.setContentsMargins(5, 5, 5, 5)
            # addWidget
            mainLayout.addWidget(self.tabMedia)
            self.setLayout(mainLayout)
            self.setWindowTitle("MA35D1 NuWriter")

        @QtCore.pyqtSlot(int, str, str, int, bool)
        def doImgProgram(self, media, start, image_file_name, option, ispack):
            print(f"slot doImgProgram {media}, {start}, {image_file_name}, {option}, {ispack}")

    import sys

    app = QtWidgets.QApplication(sys.argv)
    myapp = MainDialog()
    myapp.show()
    sys.exit(app.exec_())
