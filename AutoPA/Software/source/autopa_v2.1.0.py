# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import glob
import re
from datetime import datetime, date
import json
import math
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os
import collections
import logging
from pathlib import Path

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

class DuplicateFilter(object):
    def __init__(self):
        self.msgs = collections.deque(maxlen=3)
       
    def filter(self, record):
        rv = record.msg not in self.msgs
        self.msgs.append(record.msg)
        return rv

class AutoPA(QtWidgets.QDialog, QtWidgets.QPlainTextEdit):
    def setupUi(self, Dialog):
        Dialog.setObjectName("AutoPA")
        Dialog.resize(400, 300)
        self.formLayout = QtWidgets.QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.software = QtWidgets.QComboBox(Dialog)
        self.software.setCurrentText("")
        self.software.setObjectName("software")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.software)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.accuracy_input = QtWidgets.QLineEdit(Dialog)
        self.accuracy_input.setObjectName("accuracy")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.accuracy_input)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.azimuthOffset = QtWidgets.QLineEdit(Dialog)
        self.azimuthOffset.setObjectName("azimuthOffset")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.azimuthOffset)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.altitudeOffset = QtWidgets.QLineEdit(Dialog)
        self.altitudeOffset.setObjectName("altitudeOffset")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.altitudeOffset)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.telescopeName = QtWidgets.QLineEdit(Dialog)
        self.telescopeName.setObjectName("telescopeName")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.telescopeName)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.serialportInput = QtWidgets.QLineEdit(Dialog)
        self.serialportInput.setObjectName("serialportInput")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.serialportInput)
        self.verbose = QtWidgets.QCheckBox(Dialog)
        self.verbose.setObjectName("verbose")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.verbose)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startButton = QtWidgets.QPushButton(Dialog)
        self.startButton.setObjectName("startButton")
        self.startButton.clicked.connect(self.start)
        self.horizontalLayout.addWidget(self.startButton)
        self.stopButton = QtWidgets.QPushButton(Dialog)
        self.stopButton.setObjectName("stopButton")
        self.stopButton.clicked.connect(self.stop)
        self.horizontalLayout.addWidget(self.stopButton)
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(self.close)
        self.horizontalLayout.addWidget(self.cancelButton)
        self.formLayout.setLayout(6, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        
        logTextBox = QTextEditLogger(self)
        logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger = logging.getLogger()
        self.logger.addHandler(logTextBox)
        self.logger.addFilter(DuplicateFilter())
        self.logger.setLevel(logging.INFO)
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.SpanningRole, logTextBox.widget)

        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.alignment)

        self.lastEntry = datetime.now()
        self.aligned = True
        self.stillAdjusting = False
        self.adjustmentFinished = datetime.now()
        self.after_id = None
        self.serialport = ""
        self.indiclient = None
        self.ser = None
        self.solveCounter = 0
        self.autorun = False
        if len(sys.argv) > 1:
            if sys.argv[1] == "--autorun":
                self.autorun = True
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        if self.autorun:
            self.startButton.click()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "AutoPA"))
        self.label.setText(_translate("Dialog", "Choose your AutoPA software:"))
        self.software.addItems(software_options.keys())
        self.label_4.setText(_translate("Dialog", "Accuracy to align to (Default 60 arcseconds):"))
        self.accuracy_input.setText(_translate("Dialog", "60"))
        self.accuracy_input.setPlaceholderText(_translate("Dialog", "60"))
        self.label_2.setText(_translate("Dialog", "+/- Azimuth Offset (Default 0 arcminutes):"))
        self.azimuthOffset.setText(_translate("Dialog", "0"))
        self.azimuthOffset.setPlaceholderText(_translate("Dialog", "0"))
        self.label_3.setText(_translate("Dialog", "+/- Altitude Offset (Default 0 arcminutes):"))
        self.altitudeOffset.setText(_translate("Dialog", "0"))
        self.altitudeOffset.setPlaceholderText(_translate("Dialog", "0"))
        self.label_5.setText(_translate("Dialog", "Telescope Name (ASCOM: \"OpenAstroTracker\", INDI: \"LX200 GPS\""))
        self.telescopeName.setPlaceholderText(_translate("Dialog", "Override default?"))
        self.label_6.setText(_translate("Dialog", "Serial Port of OAT [Ekos only] (Default /dev/ttyACM0):"))
        self.serialportInput.setPlaceholderText(_translate("Dialog", "Override default? (Ekos only)"))
        self.verbose.setText(_translate("Dialog", "Verbose Output"))
        self.startButton.setText(_translate("Dialog", "Start"))
        self.stopButton.setText(_translate("Dialog", "Stop"))
        self.cancelButton.setText(_translate("Dialog", "Close"))

    def getLatestLogEntry(self, logpath, expression):
        if sys.platform == "win32":
            try:
                import win32file
                list_of_files = glob.glob(logpath)
                latest_file = max(list_of_files, key=os.path.getctime)
                logging.debug(latest_file)
                f = win32file.CreateFile(latest_file, win32file.GENERIC_READ, win32file.FILE_SHARE_DELETE | win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE, None, win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None)
                bufSize = 4096
                code, data = win32file.ReadFile(f, bufSize)
                buf = data
                while len(data) == bufSize:
                    result, data = win32file.ReadFile(f, bufSize, None)
                    buf += data
                result = re.findall(expression, buf.decode("utf-8"))[-1]
                logfileModification = os.path.getmtime(latest_file)
                return(result, logfileModification)
            except:
                raise FileNotFoundError   
        elif sys.platform == "linux":
            try:
                list_of_files = glob.glob(logpath)
                latest_file = max(list_of_files, key=os.path.getctime)
                logging.debug(latest_file)
                FileObject = open(latest_file,"r")
                contents = FileObject.readlines()
                result = re.findall(expression, contents.decode("utf-8"))[-1]
                logfileModification = os.path.getmtime(latest_file)
                return(result, logfileModification)
            except:
                raise FileNotFoundError
        
    def altitudeError(self, error, pole):
        return(self.dmsTodeg(pole)-self.dmsTodeg(error))

    def azimuthError(self, error, pole):
        return(((self.dmsTodeg(pole) + 180) % 360 - 180)-((self.dmsTodeg(error) + 180) % 360 - 180))

    def dmsTodeg(self, input):
        temp = input.split(':')
        d = float(temp[0])
        m = float(temp[1]) / 60
        s = float(temp[2]) / 3600
        return (d + m + s)

    def degToArcmin(self, input):
        return(input * 60)

    def parseError(self, software, input, azimuthOffset, altitudeOffset):
        error = []
        if software == "NINA":
            data = json.loads(input[1])
            error.append((self.degToArcmin(data["AltitudeError"]) - altitudeOffset)*(-1))
            error.append((self.degToArcmin(data["AzimuthError"]) - azimuthOffset)*(-1))
            error.append(math.hypot(error[0], error[1]))
        elif software == "Sharpcap3.2" or software == "Sharpcap4.0":
            error.append(self.degToArcmin(self.altitudeError(input[1], input[3])) - altitudeOffset)
            error.append(self.degToArcmin(self.azimuthError(input[2], input[4])) - azimuthOffset)
            error.append(math.hypot(error[0], error[1]))  
        elif software == "Ekos":
            error.append((self.degToArcmin(float(input[1])) - altitudeOffset)*(-1))
            error.append((self.degToArcmin(float(input[1])) - azimuthOffset)*(-1))
            error.append(math.hypot(error[0], error[1]))  
        logging.debug(f"Error from log: {error}.")
        return(error)

    def sendCommand(self, command, software, telescope, serialport, baudrate=19200):
        if software != "Ekos":
            import win32com.client
            logging.debug(f"Command sent: \"{command}\"")
            logging.debug(f"Telescope name: \"{telescope}\"")
            tel = win32com.client.Dispatch(f"ASCOM.{telescope}.Telescope")
            if tel.Connected:
                logging.debug("Telescope was already connected")
            else:
                tel.Connected = True
                if not tel.Connected:
                    logging.error("Unable to connect to telescope.")
                    return False
            result = tel.Action("Serial:PassThroughCommand", command)
            tel.Connected = False
        else:
            #Send command     
            logging.debug("Sending command...")
            self.ser.flush()
            self.ser.write(str.encode(command))
            result = self.ser.readline()
            result = result[:-1].decode('utf-8')
            logging.debug("Command response received")
        return result
            
    def isAdjusting(self, software, telescope, serialport):
        try:  
            logging.debug("Getting mount status...")
            result = self.sendCommand(":GX#,#", software, telescope, serialport)
            if not result:
                raise Exception
            logging.debug(result)
            status = re.search(",(......),", result)[1]
            if status[3]=="-" and status[4]=="-":
                return False
            else:
                return True
        except:
            if software == "Ekos":
                logging.error("Problem determining mount status. Verify mount is connected to INDI. Stopping AutoPA.")
            else:
                logging.error("Problem determining mount status. Verify mount is connected to ASCOM. Stopping AutoPA.")
            self.timer.stop()
            raise ConnectionError

    def start(self):
        if self.verbose.isChecked():
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)
        if self.aligned:
            logging.info("Starting AutoPA routine")
            self.aligned = False
            self.accuracy = float(self.accuracy_input.text()) / 60
            self.timer.start(1000)
        if self.telescopeName.text() == "":
            if self.software.currentText() == "Ekos":
                self.telescope = "LX200 GPS"
            else:
                self.telescope = "OpenAstroTracker"
        if self.serialportInput.text() == "":
            if self.software.currentText() == "Ekos":
                self.serialport = "/dev/ttyACM0"
            else:
                self.serialport = self.serialportInput.text()
        if self.software.currentText() == "Ekos":
            import indi, serial
            #Connect to indi server
            self.indiclient, self.blobEvent = indi.indiserverConnect()
            logging.debug("AutoPA connected to INDI server")

            #Disconnect OAT from indi to free up serial port
            indi.disconnectScope(self.indiclient, self.telescope)
            logging.debug("Telescope disconnected from INDI")
            
            print("Opening serial port on " + self.serialport + '...')
            self.ser = serial.Serial(self.serialport, 19200, timeout = 0.2)
        
    def stop(self):
        self.aligned = True
        self.timer.stop()
        if self.software.currentText() == "Ekos":
            import indi
            self.ser.close()
            #Reconnect OAT to indi and disconnect from server
            indi.connectScope(self.indiclient, self.telescope)
            logging.debug("Telescope reconnected to INDI")
            indi.indiserverDisconnect(self.indiclient)
            logging.debug("AutoPA disconnected from INDI server")
        logging.info("Stopping AutoPA routine")
        
    def close(self):
        sys.exit(self)
           
    def alignment(self):
        if not self.aligned:
            try:
                if self.isAdjusting(self.software.currentText(), self.telescope, self.serialport):
                    logging.info("Mount is still adjusting position.")
                    self.stillAdjusting = True
                else:
                    if self.stillAdjusting:
                        logging.info(f"Mount adjustment finished.")
                        self.stillAdjusting = False
                        self.adjustmentFinished = datetime.now()
                        self.solveCounter = 0
                    logging.info(f"Getting latest log entry from {self.software.currentText()}.")
                    try:
                        log = self.getLatestLogEntry(softwareTypes[self.software.currentText()]["logpath"], softwareTypes[self.software.currentText()]["expression"])
                    except FileNotFoundError:
                        log = None
                        logging.error(f"Error retrieving log from {self.software.currentText()}. Logfile may not exist or does not contain alignment info.")
                        if self.autorun:
                            sys.exit("Polar alignment values not found.")
                    if log is not None:
                        #Entry date is based on file timestamp, entry time is based on log entry data
                        currentEntry = datetime.strptime(datetime.fromtimestamp(log[1]).strftime("%Y-%m-%d") + " " + log[0][0][:-1], '%Y-%m-%d %H:%M:%S.%f')
                        if currentEntry != self.lastEntry and currentEntry > self.adjustmentFinished:
                            self.solveCounter += 1 #Increment counter if the latest unused entry was entered into the log after the adjustment was finished.
                        if (self.software.currentText() != "NINA" and self.solveCounter >= 1) or (self.software.currentText() == "NINA" and self.solveCounter >= 3):
                            #If using NINA, wait for three complete solves after adjustment is finished to prevent using old data
                            self.solveCounter = 0
                            error = self.parseError(self.software.currentText(), log[0], float(self.azimuthOffset.text()), float(self.altitudeOffset.text()))
                            logging.info(f"Altitude error in arcminutes: {error[0]:.3f}\'")
                            logging.info(f"Azimuth error in arcminutes: {error[1]:.3f}\'")
                            logging.info(f"Total error in arcminutes: {error[2]:.3f}\'")
                            if abs(error[2]) < self.accuracy:
                                logging.info(f"Polar aligned to within {error[0]*60:.0f}\" altitude and {error[1]*60:.0f}\" azimuth.")
                                self.stop()
                                if self.autorun:
                                    sys.exit(self)
                                return
                            else:
                                logging.info("Correction needed.")
                                result = self.sendCommand(f":MAL{error[0]}#", self.software.currentText(), self.telescope, self.serialport)
                                logging.debug(f"Adjusting altitude by {error[0]:.3f} arcminutes.")
                                result = self.sendCommand(f":MAZ{error[1]*(-1)}#", self.software.currentText(), self.telescope, self.serialport)
                                logging.debug(f"Adjusting altitude by {error[0]:.3f} arcminutes.")
                                self.lastEntry = currentEntry
                        else:
                            logging.info(f"Waiting for {self.software.currentText()} to re-solve since last adjustment finished.")
                    else:
                        logging.info(f"{self.software.currentText()} has not yet determined the polar alignment error.")
            except ConnectionError:
                self.stop()
                if self.autorun:
                    sys.exit("AutoPA could not connect to mount.")
                return

software_options = collections.OrderedDict([
    ('NINA', ''),
    ('Sharpcap4.0', ''),
    ('Sharpcap3.2', ''),
    ('Ekos', '')
])

today = date.today().strftime("%Y-%m-%d")
softwareTypes = {
"NINA":{        "expression": "(\d{2}:\d{2}:\d{2}.\d{3})\s-\s({.*})", 
                "logpath": f"{Path.home()}\Documents\\N.I.N.A\PolarAlignment\*.log"},
"Sharpcap3.2":{ "expression": "(?:Info:)\t(\d{2}:\d{2}:\d{2}.\d{7}).*(?:AltAzCor=)(?:Alt=)(.*)[,](?:Az=)(.*).\s(?:AltAzPole=)(?:Alt=)(.*)[,](?:Az=)(.*).[,]\s(?:AltAzOffset=).*", 
                "logpath": f"{os.getenv('LOCALAPPDATA')}\SharpCap\logs\*.log"},
"Sharpcap4.0":{ "expression": "(?:Info)\W*(\d{2}:\d{2}:\d{2}.\d{6}).*(?:AltAzCor=)(?:Alt=)(.*)[,](?:Az=)(.*).\s(?:AltAzPole=)(?:Alt=)(.*)[,](?:Az=)(.*).[,]\s(?:AltAzOffset=).*", 
                "logpath": f"{os.getenv('LOCALAPPDATA')}\SharpCap\logs\*.log"},
"Ekos":{ "expression": "(\d{2}:\d{2}:\d{2}.\d{3}).*(?:PAA Refresh).*(?:Corrected az:).*(?:\()(\s?-?\d\.\d{3}).*(?:alt:).*(\s?-?\d\.\d{3}).*(?:total:)", 
                "logpath": f"{Path.home()}/.local/share/kstars/logs/{today}/*.txt"}
}            
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QDialog()
    ui = AutoPA()
    ui.setupUi(window)

    window.show()
    sys.exit(app.exec_())

