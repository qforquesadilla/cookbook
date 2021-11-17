
import os
import sys
import re
import json
import subprocess
from functools import partial
from string import ascii_uppercase
from collections import OrderedDict

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QTableWidgetItem, QCheckBox, QComboBox, QPushButton, QHBoxLayout, QHeaderView
from PySide2.QtCore import QFile, Qt

from .._actionBase import _ActionBase


class Action(_ActionBase):

    def __init__(self):
        '''
        '''

        super().__init__(__file__, 'Set Network Drive', 'System')

        self._buildUi()
        self.__linkCommands()

        self.__updateAssignment()


    def __linkCommands(self):
        self.actionUi.assignmentAddPB.clicked.connect(partial(self.__onAddPressed, self.actionUi.assignmentTW))
        self.actionUi.assignmentRemovePB.clicked.connect(partial(self.__onRemovePressed, self.actionUi.assignmentTW))
        self.actionUi.configPB.clicked.connect(self.__onConfigPressed)
        self.actionUi.refreshPB.clicked.connect(self.__onRefreshPressed)


    ############
    # COMMANDS #
    ############


    def __onEditPath(self):
        print('edit path')


    def __onAddPressed(self, qTableWidget):
        row = qTableWidget.rowCount()
        qTableWidget.insertRow(row)
        self.__createTableWidgetCells(self.actionUi.assignmentTW, row)


    def __onRemovePressed(self, qTableWidget):
        row = qTableWidget.currentRow()
        if row != -1:
            qTableWidget.removeRow(row)


    def __onChecked(self, index, *args):
        drivePath = self.__getTableWidget(self.actionUi.assignmentTW)
        drive = drivePath[index][0]
        path = drivePath[index][1]
        print(index, drive, path)


    def __onDriveChanged(self, index, *args):
        drivePath = self.__getTableWidget(self.actionUi.assignmentTW)
        drive = drivePath[index][0]
        path = drivePath[index][1]
        print(index, drive, path)


    def __onOpenPressed(self, index):
        drivePath = self.__getTableWidget(self.actionUi.assignmentTW)
        try:
            path = drivePath[index][1]
        except IndexError:
            path = ''

        if os.path.exists(path):
            os.startfile(path)


    def __onConfigPressed(self):
        os.startfile(self.__configPath)


    def __onRefreshPressed(self):
        self.__updateAssignment()




    ###########
    # METHODS #
    ###########


    def __getActiveDrivePath(self):
        command = 'net use'
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        drivePathText = ''
        drivePathList = []

        while True:
            line = proc.stdout.readline()
            drivePathText += str(line)
            drivePathText += '\n'

            if not line and proc.poll() is not None:
                break

        pattern = r'([A-Z]+):        ([A-Za-z0-9/\\.\$-_]+)'
        for drivePath in re.findall(pattern, drivePathText):
            drive = drivePath[0]
            path = drivePath[1]
            if r'\\' in path:
                path = path.replace(r'\\', '\\')
            drivePathList.append([drive, path])

        return drivePathList


    def __getCustomDrivePath(self):
        drivePath = self.__readJson(self._configPath)
        drivePathList = drivePath['customDrivePath']
        return drivePathList


    def __mountDrive(self, drive, path):
        return
        command = 'net use /y {}: \{}'.format(drive, path)
        os.system(command)


    def __unmountDrive(self):
        return
        command = 'net use /y {} /delete'.format(drive)
        os.system(command)


    def __updateConfig(self):
        self.__updateJson(self.__configPath, {})
        # store only custom made rows in config


    def __editAssignment(self):
        pass
        # check if path is valid
        # unmount and uncheck if drive letter is used
        # mount and check


    def __updateAssignment(self):
        activeDrivePath = self.__getActiveDrivePath()
        customDrivePath = self.__getCustomDrivePath()
        print(activeDrivePath)
        print(customDrivePath)
        self.__setTableWidget(self.actionUi.assignmentTW, activeDrivePath, customDrivePath)


    ########
    # MISC #
    ########


    def __readJson(self, jsonPath):
        with open(jsonPath) as d:
            data = json.load(d)
        return data


    def __writeJson(self, jsonPath, keyValue):
        with open(jsonPath, 'w') as d:
            dump = json.dumps(keyValue, indent=4, sort_keys=True, ensure_ascii=False)
            d.write(dump)


    def __updateJson(self, jsonPath, keyValue):
        data = self.__readJson(jsonPath)
        for key in keyValue:
            value = keyValue[key]
            data[key] = value
        self.__writeJson(jsonPath, data)


    #def __getLineEdit(self, qLineEdit):
    #    return qLineEdit.text()


    #def __getTextEdit(self, qTextEdit):
    #    return qTextEdit.toPlainText()


    def __getComboBox(self, qComboBox):
        return qComboBox.currentText()


    def __setComboBox(self, qComboBox, value):
        index = qComboBox.findText(value)
        if qComboBox != 1:
            qComboBox.setCurrentIndex(index)
        return index


    def __getTableWidget(self, qTableWidget):
        drivePath = []
        rows = qTableWidget.rowCount()

        for row in range(rows):

            qWidgetComboBox = qTableWidget.cellWidget(row, 1)####################
            qComboBox = qWidgetComboBox.findChild(QComboBox)
            qTableWidgetItem = qTableWidget.item(row, 2)

            drive = qComboBox.currentText() ##################################This becomes ''
            path = qTableWidgetItem.text()

            drivePath.append([drive, path])

        return drivePath


    def __setTableWidget(self, qTableWidget, activeDrivePath, customDrivePath):
        for i in range(qTableWidget.rowCount() + 1):
            qTableWidget.removeRow(0)

        for i in range(len(activeDrivePath) + len(customDrivePath)):
            qTableWidget.insertRow(0)

        #if len(drivePath) == 0:
        #    qTableWidget.insertRow(0)
        #    return drivePath

        activeRows = len(activeDrivePath)
        for activeRow in range(activeRows):
            drive = activeDrivePath[activeRow][0]
            path = activeDrivePath[activeRow][1]
            self.__createTableWidgetCells(qTableWidget, activeRow, True, drive, path)

        customRows = len(customDrivePath)
        for customRow in range(customRows):
            drive = customDrivePath[customRow][0]
            path = customDrivePath[customRow][1]
            self.__createTableWidgetCells(qTableWidget, activeRows + customRow, False, drive, path)

        qTableWidget.setColumnWidth(0, 45)
        qTableWidget.setColumnWidth(1, 45)
        qTableWidget.setColumnWidth(2, 200)
        qTableWidget.setColumnWidth(3, 45)
        
        qTableWidget.setSortingEnabled(False)
        qHeaderView = qTableWidget.horizontalHeader()
        qHeaderView.setSectionResizeMode(0, QHeaderView.Interactive)
        qHeaderView.setSectionResizeMode(1, QHeaderView.Interactive)
        qHeaderView.setSectionResizeMode(2, QHeaderView.Stretch)
        qHeaderView.setSectionResizeMode(3, QHeaderView.Interactive)
        qHeaderView.setStretchLastSection(False)

        return activeDrivePath, customDrivePath
    
    
    def __createTableWidgetCells(self, qTableWidget, row, status=False, drive='', path=''):

        #print(index)
        #print(drivePath)
        #print(drivePath.items())
        #drive = list(drivePath.items())[row][0]
        #path = list(drivePath.items())[row][1]

        # QCheckBox index
        qWidgetCheckBox = QWidget()
        qCheckBox = QCheckBox()
        if status:
            qCheckBox.setChecked(True)
        qCheckBox.stateChanged.connect(partial(self.__onChecked, row))
        qHBoxLayoutCheckBox = QHBoxLayout(qTableWidget)
        qHBoxLayoutCheckBox.addWidget(qCheckBox)
        qHBoxLayoutCheckBox.setAlignment(Qt.AlignCenter)
        qHBoxLayoutCheckBox.setContentsMargins(0, 0, 0, 0);
        qWidgetCheckBox.setLayout(qHBoxLayoutCheckBox)

        # QComboBox
        qWidgetComboBox = QWidget()
        qComboBox = QComboBox()
        abc = dict.fromkeys(ascii_uppercase, 0)
        qComboBox.addItems(sorted(abc.keys()))
        if drive:
            self.__setComboBox(qComboBox, drive)
        qComboBox.currentIndexChanged.connect(partial(self.__onDriveChanged, row))
        qHBoxLayoutComboBox = QHBoxLayout(qTableWidget)
        qHBoxLayoutComboBox.addWidget(qComboBox)
        qHBoxLayoutComboBox.setAlignment(Qt.AlignCenter)
        qHBoxLayoutComboBox.setContentsMargins(0, 0, 0, 0);
        qWidgetComboBox.setLayout(qHBoxLayoutComboBox)

        # QTableWidgetItem
        qTableWidgetItem = QTableWidgetItem()
        if path:
            qTableWidgetItem.setText(path)

        # QPushButton
        qWidgetPushButton = QWidget()
        qPushButton = QPushButton()
        qPushButton.setText('...')
        qPushButton.setFixedSize(24, 21)
        qPushButton.clicked.connect(partial(self.__onOpenPressed, row))
        qHBoxLayoutPushButton = QHBoxLayout(qTableWidget)
        qHBoxLayoutPushButton.addWidget(qPushButton)
        qHBoxLayoutPushButton.setAlignment(Qt.AlignCenter)
        qHBoxLayoutPushButton.setContentsMargins(0, 0, 0, 0);
        qWidgetPushButton.setLayout(qHBoxLayoutPushButton)

        qTableWidget.setCellWidget(row, 0, qWidgetCheckBox)
        qTableWidget.setCellWidget(row, 1, qWidgetComboBox)
        qTableWidget.setItem(row, 2, qTableWidgetItem)
        qTableWidget.setCellWidget(row, 3, qWidgetPushButton)
