
#!/usr/bin/python3
import sys, os

from PyQt5 import QtWidgets, QtCore, QtGui

# FIXME: without dispose_resources, the ui tool raises an exception.
# SystemExit: [Errno 13] Access denied (insufficient permissions)
# but, with dispose_resources, the command tool raises timeout error.

# from nuwriter import *
from nuwriterTEMP import (DEV_DDR_SRAM, DEV_NAND, DEV_OTP, DEV_SD_EMMC,
        DEV_SPINAND, DEV_SPINOR, DEV_USBH,
        OPT_NONE, OPT_SCRUB, OPT_WITHBAD, OPT_EXECUTE, OPT_VERIFY,
        OPT_UNPACK, OPT_RAW, OPT_EJECT,
        do_attach, do_img_erase, do_img_program, do_img_read, do_otp_program,
        do_pack_program)

class EmittingStream(QtCore.QObject):

    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

from mainwindow import Ui_MainWindow
from gui.mediaPages import DdrSramPage, SpiPage

try:
    # Include in try/except block if you're also targeting Mac/Linux
    from PyQt5.QtWinExtras import QtWin
    myappid = 'Nuvoton.nuwriter.UiPyqt5.0120'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

import configparser

class Ui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self) # Call the inherited classes __init__ method
        # uic.loadUi('gui/ui/NUA3500-Writer.ui', self) # Load the .ui file

        self.setupUi(self)


        self.setWindowTitle("MA35D1 NuWriter")

        self.addMedia()

        self.text_browser = QtWidgets.QTextBrowser(self)
        self.verticalLayout.addWidget(self.text_browser)

        # Install the custom output stream
        # sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        self.outputStream = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stdout = self.outputStream
        sys.stderr = self.outputStream

        self.initToolSetting()

        # Attach
        self.browseDDR_btn.clicked.connect(self.iniBrowse)
        self.attach_btn.clicked.connect(self.doAttach)

    def addMedia(self):

        # DEV_DDR_SRAM = 0
        self.ddrPage = DdrSramPage()
        self.tabMedia.addTab(self.ddrPage, "DDR/SRAM")
        self.ddrPage.signalImgProgram.connect(self.doImgProgram)

        # DEV_NAND = 1
        self.nandPage = SpiPage(DEV_NAND, self)
        self.tabMedia.addTab(self.nandPage, "NAND")

        # DEV_SD_EMMC = 2
        self.sdEmmcPage = SpiPage(DEV_SD_EMMC, self)
        self.tabMedia.addTab(self.sdEmmcPage, "SD/EMMC")

        # DEV_SPINOR = 3
        self.spiNorPage = SpiPage(DEV_SPINOR, self)
        self.tabMedia.addTab(self.spiNorPage, "SPI NOR")

        # DEV_SPINAND = 4
        self.spiNandPage = SpiPage(DEV_SPINAND, self)
        self.tabMedia.addTab(self.spiNandPage, "SPI NAND")

        # DEV_OTP = 6


    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    ################################################################################################
    # 'MA35D1.ini'
    ################################################################################################

    def initToolSetting(self):

        self.iniFileName = 'MA35D1.ini'

        iniFileName = self.iniFileName

        # https://pyinstaller.readthedocs.io/en/stable/runtime-information.html
        if getattr(sys, 'frozen', False):
            # we are running in a bundle
            app_dir = os.path.dirname(os.path.abspath(sys.executable))
        else:
            # we are running in a normal Python environment
            app_dir = os.path.dirname(os.path.abspath(__file__))

        iniFilePath = os.path.join(app_dir, iniFileName)

        if not os.path.exists(iniFilePath):
            open(iniFileName, 'w', encoding='utf-8')

        self.conf = configparser.ConfigParser()
        self.conf.read(iniFilePath, encoding='utf-8')

        section = 'Attach'

        if not self.conf.has_section(section):
            self.conf.add_section(section)
            self.conf.set(section, 'Ini File', '')
        else:
            self.ddrFileLineEdit.setText(self.conf.get(section, 'Ini File', fallback=''))

        section = 'DDR'

        if not self.conf.has_section(section):
            self.conf.add_section(section)
            self.conf.set(section, 'write file', '')
            self.conf.set(section, 'write addr', '')
            self.conf.set(section, 'write execute', 'false')
        else:
            self.ddrPage.imgPathLine.setText(self.conf.get(section, 'write file', fallback=''))
            self.ddrPage.imgAddress.setText(self.conf.get(section, 'write addr', fallback=''))
            self.ddrPage.optExecute.setChecked(self.conf.getboolean(section, 'write execute', fallback=False))


        sections = ['NAND', 'SPINOR', 'SPINAND', 'SD']

        for sec in sections:
            if sec == 'NAND':
                page = self.nandPage
            elif sec == 'SPINOR':
                page = self.spiNorPage
            elif sec == 'SPINAND':
                page = self.spiNandPage
            elif sec == 'SD':
                page = self.sdEmmcPage

            if not self.conf.has_section(sec):
                self.conf.add_section(sec)
                self.conf.set(sec, 'write file', '')
                self.conf.set(sec, 'write addr', '')
                self.conf.set(sec, 'write pack', 'false')
                self.conf.set(sec, 'write option', '')
                self.conf.set(sec, 'read file', '')
                self.conf.set(sec, 'read start', '')
                self.conf.set(sec, 'read length', '')
                self.conf.set(sec, 'read all', 'false')
                self.conf.set(sec, 'read option', '')
                self.conf.set(sec, 'erase start', '')
                self.conf.set(sec, 'erase length', '')
                self.conf.set(sec, 'erase all', 'false')
            else:
                page.imgPathLine.setText(self.conf.get(sec, 'write file', fallback=''))
                page.imgAddress.setText(self.conf.get(sec, 'write addr', fallback=''))
                page.radioPack.setChecked(self.conf.getboolean(sec, 'write pack', fallback=False))

                _wopt = self.conf.get(sec, 'write option', fallback='')

                try:
                    if _wopt == "Verify":
                        page.verifyWrite.setChecked(True)
                    elif _wopt == "Raw":
                        page.rawWrite.setChecked(True)
                except:
                    pass

                page.fileSave.setText(self.conf.get(sec, 'read file', fallback=''))
                page.readStart.setText(self.conf.get(sec, 'read start', fallback=''))
                page.readEnd.setText(self.conf.get(sec, 'read length', fallback=''))
                page.readAll.setChecked(self.conf.getboolean(sec, 'read all', fallback=False))

                _ropt = self.conf.get(sec, 'read option', fallback='')

                try:
                    if _ropt == "WithBad":
                        page.readWithBad.setChecked(True)
                except:
                    pass

                page.eraseStart.setText(self.conf.get(sec, 'erase start', fallback=''))
                page.eraseEnd.setText(self.conf.get(sec, 'erase length', fallback=''))
                page.eraseAll.setChecked(self.conf.getboolean(sec, 'erase all', fallback=False))

    def closeEvent(self, evt):
        # self.conf.write(open(self.iniFileName, 'w', encoding='utf-8'))
        pass

    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        self.text_browser.insertPlainText(text)

    def iniBrowse(self):
        filename = ""
        # Fix for crash in X on Ubuntu 14.04
        filename, _ = QtWidgets.QFileDialog.getOpenFileName()
        if filename != "":
            self.ddrFileLineEdit.setText(filename)

    ################################################################################################
    # command line
    ################################################################################################

    @QtCore.pyqtSlot()
    def doAttach(self):
        iniFile = self.ddrFileLineEdit.text()
        self.conf.set('Attach', 'Ini File', iniFile)
        self.conf.write(open(self.iniFileName, 'w', encoding='utf-8'))

        self.text_browser.clear()
        print(f'do_attach({iniFile})')

        try:
            do_attach(iniFile)
        except SystemExit as e:
            print(f'SystemExit: {e}')
            pass
        except Exception as e:
            print(f'An Error occurred: {e}')
            pass
        except:
            print('except')
            pass

    # def do_img_read(media, start, out_file_name, length=0x1, option=OPT_NONE) -> None:
    @QtCore.pyqtSlot(int, str, str, str, int, bool)
    def doImgRead(self, media, startStr, fileStr, lengthStr, option, isall=False):

        if isall:
            start = 0
            length = 0
        else:
            try:
                start = int(startStr, 0) & 0xffffffff
            except:
                start = 0

            try:
                length = int(lengthStr, 0) & 0xffffffff
            except:
                length = 0x1


        self.text_browser.clear()

        if media in [DEV_NAND, DEV_SPINOR, DEV_SPINAND, DEV_SD_EMMC]:

            if media == DEV_NAND:
                section = 'NAND'
            elif media == DEV_SPINOR:
                section = 'SPINOR'
            elif media == DEV_SPINAND:
                section = 'SPINAND'
            else:
                section = 'SD'

            self.conf.set(section, 'read file', fileStr)
            self.conf.set(section, 'read start', startStr)
            self.conf.set(section, 'read length', lengthStr)

            if option == OPT_NONE:
                self.conf.set(section, 'read option', "None")
            elif option == OPT_WITHBAD:
                self.conf.set(section, 'read option', "WithBad")

            if isall:
                self.conf.set(section, 'read all', 'true')
            else:
                self.conf.set(section, 'read all', 'false')

        self.conf.write(open(self.iniFileName, 'w', encoding='utf-8'))

        try:
            print(f'do_img_read({media}, {start}, {fileStr}, {length}, {option})')
            do_img_read(media, start, fileStr, length, option)
        except SystemExit as e:
            print(f'SystemExit: {e}')
            pass
        except Exception as e:
            print(f'An Error occurred: {e}')
            pass
        except:
            print('except')
            pass


        pass

    # def do_img_program(media, start, image_file_name, option=OPT_NONE) -> None:
    @QtCore.pyqtSlot(int, str, str, int, bool)
    def doImgProgram(self, media, startStr, image_file_name, option, ispack=False):

        try:
            start = int(startStr, 0) & 0xffffffff
        except:
            start = 0

        self.text_browser.clear()

        if media == DEV_DDR_SRAM:
            section = 'DDR'
            self.conf.set(section, 'write file', image_file_name)
            self.conf.set(section, 'write addr', startStr)
            if option == 0:
                self.conf.set(section, 'write execute', 'false')
            elif option == 2:
                self.conf.set(section, 'write execute', 'true')

        elif media in [DEV_NAND, DEV_SPINOR, DEV_SPINAND, DEV_SD_EMMC]:

            if media == DEV_NAND:
                section = 'NAND'
            elif media == DEV_SPINOR:
                section = 'SPINOR'
            elif media == DEV_SPINAND:
                section = 'SPINAND'
            else:
                section = 'SD'

            self.conf.set(section, 'write file', image_file_name)
            self.conf.set(section, 'write addr', startStr)

            if ispack:
                self.conf.set(section, 'write pack', 'true')
            else:
                self.conf.set(section, 'write pack', 'false')

        elif media == DEV_OTP:
            section = 'OTP'
            self.conf.set(section, 'write file', image_file_name)

        if option == OPT_NONE:
            self.conf.set(section, 'write option', "None")
        elif option == OPT_VERIFY:
            self.conf.set(section, 'write option', "Verify")
        elif option == OPT_RAW:
            self.conf.set(section, 'write option', "Raw")

        self.conf.write(open(self.iniFileName, 'w', encoding='utf-8'))

        try:
            if media == DEV_OTP:
                print(f'do_otp_program({image_file_name})')
                do_otp_program(image_file_name)
            elif ispack:
                print(f'do_pack_program({media}, {image_file_name}, {option})')
                do_pack_program(media, image_file_name, option)
            else:
                print(f'do_img_program({media}, {start}, {image_file_name}, {option})')
                do_img_program(media, start, image_file_name, option)
        except SystemExit as e:
            print(f'SystemExit: {e}')
            pass
        except Exception as e:
            print(f'An Error occurred: {e}')
            pass
        except:
            print('except')
            pass

    # def do_img_erase(media, start, length=0, option=OPT_NONE) -> None:
    @QtCore.pyqtSlot(int, str, str, int, bool)
    def doImgErase(self, media, startStr, lengthStr, option, isall=False):

        if isall:
            start = 0
            length = 0
        else:
            try:
                start = int(startStr, 0) & 0xffffffff
            except:
                start = 0

            try:
                length = int(lengthStr, 0) & 0xffffffff
            except:
                length = 0x1


        self.text_browser.clear()

        if media in [DEV_NAND, DEV_SPINOR, DEV_SPINAND, DEV_SD_EMMC]:

            if media == DEV_NAND:
                section = 'NAND'
            elif media == DEV_SPINOR:
                section = 'SPINOR'
            elif media == DEV_SPINAND:
                section = 'SPINAND'
            else:
                section = 'SD'

            self.conf.set(section, 'erase start', startStr)
            self.conf.set(section, 'erase length', lengthStr)

            if isall:
                self.conf.set(section, 'erase all', 'true')
            else:
                self.conf.set(section, 'erase all', 'false')

        self.conf.write(open(self.iniFileName, 'w', encoding='utf-8'))

        try:
            print(f'do_img_erase({media}, {start}, {length}, {option})')
            do_img_erase(media, start, length, option)
        except SystemExit as e:
            print(f'SystemExit: {e}')
            pass
        except Exception as e:
            print(f'An Error occurred: {e}')
            pass
        except:
            print('except')
            pass


        pass

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    # tool icon
    app.setWindowIcon(QtGui.QIcon(':/icons/app.ico'))
    myapp = Ui()
    myapp.show()
    sys.exit(app.exec_())
