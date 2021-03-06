# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maxTouch_readout.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox
import os
from pywinauto.application import Application
import pywinauto
from pywinauto.controls.common_controls import TabControlWrapper
from pywinauto.controls.menuwrapper import Menu
import time
global targetdevice
currentPath = os.getcwd()

def saveFolder(folderName):
    currentPath = os.getcwd()
    # folderName = F"{self.fa_num.text()}_{self.device_name.currentText()}_IncomingRead"
    try:
        os.mkdir(folderName)
    except FileExistsError as error:
        os.rmdir(folderName)
        # print(F"Folder Exsists. Overwriting..")
        # print(F"Creating folder for: {fa_num}.")
        # os.mkdir(folderName)
        os.mkdir(folderName)

def maxTouchStudio():
    dialog_box = QMessageBox()
    dialog_box.setIcon(QMessageBox.Information)
    dialog_box.setText("Proceed to maxTouch Studio?")
    dialog_box.setWindowTitle("Device Stuck in bootloader mode")
    dialog_box.setStandardButtons(QMessageBox.Yes| QMessageBox.No)

    returnValue = dialog_box.exec()
    dialog_box.raise_()
    if returnValue == QMessageBox.Yes:
        print(F"FW Extractor - Target device: {targetdevice}")

def i2cError():
    dialog_box = QMessageBox()
    dialog_box.setIcon(QMessageBox.Information)
    dialog_box.setText("Device failed to communicate with the Object-based Server. Kindly check if it is a possible setup issue. Otherwise, you may perform I/V curve on I2C pins and/or power pins then endorse the unit for ATE testing.")

    dialog_box.setWindowTitle("No communication")
    dialog_box.setStandardButtons(QMessageBox.Ok)
    returnValue = dialog_box.exec()
    dialog_box.raise_()
    if returnValue == QMessageBox.Ok:
        print(F"FW Extractor - Target device: {targetdevice}")

def fwExtraction_complete(targetdevice):
    dialog_box = QMessageBox()
    dialog_box.setIcon(QMessageBox.Information)
    dialog_box.setText("FW extraction complete.")
    dialog_box.setWindowTitle("Device Stuck in bootloader mode")
    dialog_box.setStandardButtons(QMessageBox.Yes| QMessageBox.No)

    returnValue = dialog_box.exec()
    dialog_box.raise_()
    if returnValue == QMessageBox.Ok:
        print(F"FW Extractor - Target device: {targetdevice}")

def deviceStuck(targetdevice):
    dialog_box = QMessageBox()
    dialog_box.setIcon(QMessageBox.Information)
    dialog_box.setText("Device stuck in bootloader mode. Proceed extracting FW?")
    dialog_box.setWindowTitle("Device Stuck in bootloader mode")
    dialog_box.setStandardButtons(QMessageBox.Yes| QMessageBox.No)

    returnValue = dialog_box.exec()
    dialog_box.raise_()
    if returnValue == QMessageBox.Yes:
        print(F"FW Extractor - Target device: {targetdevice}")
    elif returnValue == QMessageBox.No:
        quit()

def ChipConfig():
    dialog_box = QMessageBox()
    dialog_box.setIcon(QMessageBox.Information)
    dialog_box.setText("Backing up - Chip configuration and Chip information")
    dialog_box.setWindowTitle("Incoming Read")
    #dialog_box.setStandardButtons(QMessageBox.Yes| QMessageBox.No)
    dialog_box.setStandardButtons(QMessageBox.Ok)
    dialog_box.exec()
    time.sleep(0.5)
    dialog_box.close()

class Ui_Dialog(object):
    def showCTE_T46configuration(self):

        dialog_box = QMessageBox()
        dialog_box.setIcon(QMessageBox.Information)
        dialog_box.setText("Check jumper settings for CAPEXT and VDDIOXL.\n\n Internal charge pump: Close CAPEXT\n No Boost: Close VDDIOXL and V4")
        dialog_box.setWindowTitle("T46 CTE Configuration check")
        dialog_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = dialog_box.exec()

        if returnValue == QMessageBox.Ok:
            print("ok")
            self.continue641read = True
            return self.continue641read


    def fwExtractor(self,device_name,folderName):
        print(F"FW Extractor - Target device: {self.device_name.currentText()}")
        fwExtractorFolder = F"{currentPath}\FW extractor"
        #fwApp = Application(backend="win32").start(r'C:\Users\a50291\PycharmProjects\FA Bench\Modules\Maxtouch guide\FW extractor\CONFIDENTIAL maXTouch flash extraction tool V1.0.0.0.exe')
        fwApp = Application(backend="win32").start(F"{fwExtractorFolder}\CONFIDENTIAL maXTouch flash extraction tool V1.0.0.0.exe")
        fw_spec = fwApp.window(title='Atmel maXTouch Bootloader Tool v1.0.0.0')
        actionable_dlg = fw_spec.wait('visible')

        pywinauto.mouse.click(button='left', coords=(712, 301))  # show hidden buttons

        try:
            fwApp.TForm1.TButton2.click()  # check if CHG button is disabled
            if device_name in ['ATMXT224', 'ATMXT224E']:
                print('GENERIC_mXT224-mXT224E.secret')
                fwApp.TForm1.Edit4.set_edit_text(F'{fwExtractorFolder}\GENERIC_mXT224-mXT224E.secret')

            elif device_name in ['ATMXT768E', 'ATMXT540E', 'ATMXT1386']:
                print('GENERIC_mXT768e-mXT540e-mXT1386.secret')
                fwApp.TForm1.Edit4.set_edit_text(F'{fwExtractorFolder}\GENERIC_mXT768e-mXT540e-mXT1386.secret')

            elif device_name in ['ATMXT1664S', 'ATMXT1188S']:
                print('GENERIC_mXT1664S.secret')
                fwApp.TForm1.Edit4.set_edit_text(F'{fwExtractorFolder}\GENERIC_mXT1664S.secret')

            elif device_name in ['ATMXT641T', 'ATMXT449T', 'ATMXT1189T', 'ATMXT1665T', 'ATMXT799T', 'ATMXT2952T','ATMXT1067T']:
                print('GENERIC_mXT2952T.secret')
                fwApp.TForm1.Edit4.set_edit_text(F'{fwExtractorFolder}\GENERIC_mXT2952T.secret')

            fwApp.TForm1.capture_as_image().save(F'{currentPath}\{folderName}\ window.png')  # Save Screenshot
            fwApp.TForm1.TButton3.click()  # Find Bootloader
            fwApp.TForm1.TEdit3.set_edit_text("")  # Clear Field
            init_nvm_content = fwApp.TForm1.TEdit3.texts()  # Initial Value
            read_nvm_content = fwApp.TForm1.TEdit3.texts()

            while (init_nvm_content == read_nvm_content):
                read_nvm_content = fwApp.TForm1.TEdit3.texts()
                if (init_nvm_content != read_nvm_content):
                    break
            fwApp.TForm1.capture_as_image().save('Extracted FW.png')
            savefile = open(F'{currentPath}\{folderName}\ NVM content.txt', 'w')  # write to notepad
            savefile.write(read_nvm_content[0])
            savefile.close()
            print('not good')

        except pywinauto.base_wrapper.ElementNotEnabled:
            print ('error')
        fw_spec.close()
        #os.system("taskkill /F /IM \"CONFIDENTIAL maXTouch flash extraction tool V1.0.0.0.exe\"")


    def t25_self_test(self,currentPath,folderName):
        print ("Performing T25 self test.")

        self.page_control = self.app.TfrmMain.child_window(class_name="TPageControl")
        self.tab_control = TabControlWrapper(self.page_control.wrapper_object())
        self.tab_control.select(0)
        self.app.TfrmMain.TTabSheet.TListBox.select(u'Self Test T25', select=True)
        self.app.TForm_spt_selftest_t25.TGroupBox0.Edit.set_edit_text(250)
        self.app.TForm_spt_selftest_t25.RadioButton7.click()
        if self.app.TForm_spt_selftest_t25.CheckBox1.is_checked() == False:
            self.app.TForm_spt_selftest_t25.CheckBox1.check()
        if self.app.TForm_spt_selftest_t25.CheckBox2.is_checked() == False:
            self.app.TForm_spt_selftest_t25.CheckBox2.check()
        self.app.TForm_spt_selftest_t25.capture_as_image().save(F'{currentPath}\{folderName}\ T25 settings.png')
        self.app.TForm_spt_selftest_t25.Write.click()
        self.app.TForm_spt_selftest_t25.capture_as_image().save(F'{currentPath}\{folderName}\ SELF TEST T25 Pin fault test 2 result.png')
        self.app.TForm_spt_selftest_t25.close()
        #CHECK ENABLE


    def t46_cte (self,currentPath,folderName):
        print("T46 CTE Configuration check")
        self.page_control = self.app.TfrmMain.child_window(class_name="TPageControl")
        self.tab_control = TabControlWrapper(self.page_control.wrapper_object())
        self.tab_control.select(0)
        self.app.TfrmMain.TTabSheet.TListBox.select(u'CTE Configuration T46', select=True)
        self.app.TForm_spt_cteconfig_t46.print_control_identifiers()
        self.app.TForm_spt_cteconfig_t46.RadioButton5.get_check_state()#NO BOOST STATE
        self.app.TForm_spt_cteconfig_t46.RadioButton6.get_check_state()#Internal charge pump
        self.app.TForm_spt_selftest_t25.capture_as_image().save(F'{currentPath}\{folderName}\ T46 CTE configuration settings.png')
        if self.app.TForm_spt_cteconfig_t46.RadioButton5.get_check_state() == 1:
            print ("X Line Voltage Mode: No Boost")
        elif self.app.TForm_spt_cteconfig_t46.RadioButton6.get_check_state() == 1:
            print("X Line Voltage Mode: Internal charge pump (XVdd voltage doubler)")
        self.app.TForm_spt_cteconfig_t46.close()

    def customer_config(self,currentPath,folderName):
        print ("Saving customer configuration.")
        self.app.TfrmMain.menu_select('File->Save Config...')
        self.app.SaveAs.Edit.set_edit_text(F'{currentPath}\{folderName}\ SN1 customer config')
        self.app.SaveAs.Toolbar1.click()
        self.app.SaveAs.SaveButton.click()
        win1 = pywinauto.timings.wait_until_passes(10, 0.5, lambda: self.app.window(title=u'Confirm Save As'))

        try:
            self.app.ConfirmSaveAs.Yes.click()
        except:
            self.app.TOKRightDlgConfigFileHeaderInfo.wait('visible')
            self.app.TOKRightDlgConfigFileHeaderInfo.OK.click()
            win1 = pywinauto.timings.wait_until_passes(10, 0.5, lambda: self.app.window(title=u'Save Config File'))
            time.sleep(2)
            self.app.window(title=u'Save Config File').OK.click()

    def chip_config_chip_info(self,currentPath,folderName):
        print ("Chip configuration..")
        self.app.TfrmMain.capture_as_image().save(F'{currentPath}\{folderName}\ Chip configuration.png')
        self.tab_control.select(1)
        print("Chip information..")
        self.app.TfrmMain.capture_as_image().save(F'{currentPath}\{folderName}\ Chip information.png')

    def QtSrvr(self,folderName):
        os.system("taskkill /f /im QTSrvr_Object.exe")
        #self.app = Application(backend="win32").start(r"C:\Users\a50291\Documents\WORKING TOOLS\New Version\QTSrvr_Object.exe")
        self.app = Application(backend="win32").start(F"{currentPath}\QTSrvr_Object.exe")
        self.dlg_spec = self.app.window(title='Object-Based Server v4.10.272.0')
        self.actionable_dlg = self.dlg_spec.wait('visible')
        self.dlg_spec.set_focus()
        self.page_control = self.app.TfrmMain.child_window(class_name="TPageControl")
        self.tab_control = TabControlWrapper(self.page_control.wrapper_object())

        try:
            check_I2C = pywinauto.timings.wait_until_passes(5, 0.5, lambda: self.app.window(title=u'Device Scan Failed'))
            device_scan_failed_visible = check_I2C.wait('visible')
            self.app.TfrmMain.capture_as_image().save(F'{currentPath}\{folderName}\ I2C error.png')
            self.i2cAddress = "I2C error"
        except:
            # self.app.TfrmMain.print_control_identifiers()
            if self.app.TfrmMain.StatusBar.get_part_text(
                    0) == 'Connection: I2C (address 0x4D)' or self.app.TfrmMain.StatusBar.get_part_text(
                    0) == 'Connection: I2C (address 0x4C)' or self.app.TfrmMain.StatusBar.get_part_text(
                    0) == 'Connection: I2C (address 0x4A)' or self.app.TfrmMain.StatusBar.get_part_text(
                    0) == 'Connection: I2C (address 0x4B)':  # check I2C comms
                print('I2C address detected. ')
                self.i2cAddress = "Good communication" #

            elif self.app.TfrmMain.StatusBar.get_part_text(0) == 'Connection: None':
                print('No I2C communication')
                self.app.TfrmMain.capture_as_image().save(F"{currentPath}\{folderName}\ No I2C communication.png")
                self.i2cAddress = "I2C error"

            #for stuck in bootloader mode
            elif self.app.TfrmMain.StatusBar.get_part_text(0) == 'Connection: I2C (address 0x24)' or self.app.TfrmMain.StatusBar.get_part_text(0) == 'Connection: I2C (address 0x26)' or self.app.TfrmMain.StatusBar.get_part_text(0) == 'Connection: I2C (address 0x25)' or self.app.TfrmMain.StatusBar.get_part_text(0) == 'Connection: I2C (address 0x27)':
                print ('Device stuck in bootloader mode.')
                self.app.TfrmMain.capture_as_image().save(F'{currentPath}\{folderName}\ Device stuck in bootloader mode.png')
                self.i2cAddress = "stuck in bootloader"

        return self.i2cAddress
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(251, 149)
        font = QtGui.QFont()
        font.setFamily("Nirmala UI Semilight")
        font.setPointSize(12)
        Dialog.setFont(font)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 211, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.fa_num = QtWidgets.QLineEdit(Dialog)
        self.fa_num.setGeometry(QtCore.QRect(11, 46, 231, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fa_num.setFont(font)
        self.fa_num.setText("")
        self.fa_num.setObjectName("fa_num")
        self.sn_num = QtWidgets.QLineEdit(Dialog)
        self.sn_num.setGeometry(QtCore.QRect(11, 71, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sn_num.setFont(font)
        self.sn_num.setText("")
        self.sn_num.setObjectName("sn_num")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 110, 156, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(10)
        self.buttonBox.setFont(font)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.device_name = QtWidgets.QComboBox(Dialog)
        self.device_name.setGeometry(QtCore.QRect(130, 71, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.device_name.setFont(font)
        self.device_name.setEditable(True)
        self.device_name.setCurrentText("")
        self.device_name.setObjectName("device_name")

        self.retranslateUi(Dialog)
        self.device_name.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(self.Readout)

        device_list = ["ATMXT1067T","ATMXT1189T","ATMXT144U","ATMXT1665T","ATMXT2113T","ATMXT225T","ATMXT288U","ATMXT2912T","ATMXT449T","ATMXT641T","ATMXT540E","ATMXT768E","ATMXT224E","ATMXT224S","ATMXT336S"]

        self.device_name.addItems(sorted(device_list))

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "maXTouch Incoming Read"))
        self.fa_num.setPlaceholderText(_translate("Dialog", "FA Request Number"))
        self.sn_num.setPlaceholderText(_translate("Dialog", "Sample Number"))

    def Readout(self):
        folderName = F"{self.sn_num.text()}_{self.fa_num.text()}_{self.device_name.currentText()}_IncomingRead"
        saveFolder(folderName)
        targetdevice = self.device_name.currentText()

        if self.device_name.currentText() == "ATMXT449T" or "ATMXT641T":
            print(F"FA Request Number: {self.fa_num.text()} \nDevice: {self.device_name.currentText()}")
            self.QtSrvr(folderName)
            if self.i2cAddress == "Good communication":
                print ("ok")
                self.chip_config_chip_info(currentPath,folderName) #tested
                self.showCTE_T46configuration()
                self.t46_cte(currentPath, folderName)
                if self.continue641read == True:
                    self.customer_config(currentPath,folderName) #tested
                    self.t25_self_test(currentPath,folderName)  # tested
                    #time.sleep(1)
                    #self.t25_self_test(currentPath, folderName)
                    self.fwExtractor(targetdevice,folderName)
            elif self.i2cAddress == "stuck in bootloader":
                #print ('Device stuck in bootloader')
                deviceStuck(targetdevice)
                self.fwExtractor(targetdevice,folderName)

        else:
            print(F"FA Request Number: {self.fa_num.text()} \nDevice: {self.device_name.currentText()}")
            self.QtSrvr(folderName)
            if self.i2cAddress == "Good communication":
                print ("ok")
                self.chip_config_chip_info(currentPath,folderName) #tested
                self.customer_config(currentPath,folderName) #tested
                self.t25_self_test(currentPath,folderName)  # tested
                self.fwExtractor(targetdevice,folderName)
            elif self.i2cAddress == "stuck in bootloader":
                print ('Device stuck in bootloader.')
                deviceStuck(targetdevice)
                self.fwExtractor(targetdevice)

            #self.chip_config_chip_info()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
