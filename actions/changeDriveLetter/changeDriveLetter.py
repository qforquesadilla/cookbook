
import os
import sys
import re
import subprocess
from functools import partial

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QTableWidgetItem, QCheckBox, QPushButton, QHBoxLayout, QHeaderView
from PySide2.QtCore import QFile, Qt


class Action(object):

    def __init__(self):
        '''
        '''

        # variables
        self.actionName = 'Change Drive Letter'
        self.actionCategory = 'System'

        # config
        self.__actionRootDir = os.path.abspath(os.path.dirname(__file__))
        self.__configPath = os.path.normpath(os.path.join(self.__actionRootDir, 'data/config.json'))

        # ui & commands
        self.__buildUi()
        self.__linkCommands()

        self.__updateAssignment()


    def __buildUi(self):##########################INHERIT THIS
        '''
        '''

        # define ui file paths
        app = QApplication.instance()
        actionUiPath = os.path.normpath(os.path.join(self.__actionRootDir, 'interface/main.ui')).replace('\\', '/')

        # open ui files
        loader = QUiLoader()
        actionUiFile = QFile(actionUiPath)
        actionUiFile.open(QFile.ReadOnly)

        # create ui objects
        self.actionUi = loader.load(actionUiPath)


    def __linkCommands(self):##########################INHERIT THIS
        self.actionUi.assignmentAddPB.clicked.connect(partial(self.__onAddPressed, self.actionUi.assignmentTW))
        self.actionUi.assignmentRemovePB.clicked.connect(partial(self.__onRemovePressed, self.actionUi.assignmentTW))
        self.actionUi.configPB.clicked.connect(self.__onConfigPressed)
        self.actionUi.refreshPB.clicked.connect(self.__onRefreshPressed)


    ############
    # COMMANDS #
    ############


    def __onEditAssignment(self):
        print('edit assignment')


    def __onAddPressed(self, qTableWidget):
        qTableWidget.insertRow(0)


    def __onRemovePressed(self, qTableWidget):
        row = qTableWidget.currentRow()
        if row != -1:
            qTableWidget.removeRow(row)


    def __onChecked(self, drive, *args):###############
        ##############need to get latest path that is in the selected cell
        #print(self.__getTableWidget(self.actionUi.assignmentTW))
        #print(drive, path)
        #print(self.actionUi.assignmentTW.selectedIndexes())
        drivePath = self.__getTableWidget(self.actionUi.assignmentTW)
        print(drivePath[drive])


    def __onOpenPressed(self, drive):
        ##############need to get latest path that is in the selected cell
        drivePath = self.__getTableWidget(self.actionUi.assignmentTW)
        path = drivePath[drive]
        print(path)
        os.startfile(path)


    def __onConfigPressed(self):
        os.startfile(self.__configPath)


    def __onRefreshPressed(self):
        self.__updateAssignment()




    ###########
    # METHODS #
    ###########


    def __getDrive(self):
        command = 'net use'
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        drivePathText = ''
        drivePathDict = {}

        while True:
            line = proc.stdout.readline()
            drivePathText += str(line)
            drivePathText += '\n'

            if not line and proc.poll() is not None:
                break

        pattern = r'([A-Z]+):        ([A-Za-z0-9/\\.\$-]+)'
        for drivePath in re.findall(pattern, drivePathText):
            drive = drivePath[0]
            path = drivePath[1]
            drivePathDict[drive] = path

        return drivePathDict


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


    def __updateAssignment(self):
        drivePath = self.__getDrive()
        self.__setTableWidget(self.actionUi.assignmentTW, drivePath)


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


    def __getLineEdit(self, qLineEdit):
        return qLineEdit.text()


    def __getTextEdit(self, qTextEdit):
        return qTextEdit.toPlainText()


    def __getTableWidget(self, qTableWidget):
        drivePath = {}
        rowCount = qTableWidget.rowCount()
        for row in range(rowCount):

            drive = qTableWidget.item(row, 1)
            path = qTableWidget.item(row, 2)

            try:
                drive = drive.text()
            except AttributeError:
                continue  # TODO: UI should not allow this to be empty

            try:
                path = path.text()
            except AttributeError:
                path = ''

            drivePath[drive] = path

        return drivePath


    def __setTableWidget(self, qTableWidget, drivePath):
        for i in range(qTableWidget.rowCount() + 1):
            qTableWidget.removeRow(0)

        for i in range(len(drivePath)):
            qTableWidget.insertRow(0)

        if len(drivePath) == 0:
            qTableWidget.insertRow(0)
            return drivePath

        row = 0
        for drive, path in drivePath.items():
            #path = os.path.normpath(path)######################################

            # checkbox
            qWidgetCB = QWidget()
            qCheckBox = QCheckBox()
            qCheckBox.setChecked(True)
            qCheckBox.stateChanged.connect(partial(self.__onChecked, drive))
            qHBoxLayoutCB = QHBoxLayout(qTableWidget)
            qHBoxLayoutCB.addWidget(qCheckBox)
            qHBoxLayoutCB.setAlignment(Qt.AlignCenter)
            qHBoxLayoutCB.setContentsMargins(0, 0, 0, 0);
            qWidgetCB.setLayout(qHBoxLayoutCB)

            # drive
            driveItem = QTableWidgetItem()
            driveItem.setText(drive)

            # path
            pathItem = QTableWidgetItem()
            pathItem.setText(path)

            # push button
            qWidgetPB = QWidget()
            qPushButton = QPushButton()
            qPushButton.setText('...')
            qPushButton.setFixedSize(24, 21)
            qPushButton.clicked.connect(partial(self.__onOpenPressed, drive))
            qHBoxLayoutPB = QHBoxLayout(qTableWidget)
            qHBoxLayoutPB.addWidget(qPushButton)
            qHBoxLayoutPB.setAlignment(Qt.AlignCenter)
            qHBoxLayoutPB.setContentsMargins(0, 0, 0, 0);
            qWidgetPB.setLayout(qHBoxLayoutPB)

            qTableWidget.setCellWidget(row, 0, qWidgetCB)
            qTableWidget.setItem(row, 1, driveItem)
            qTableWidget.setItem(row, 2, pathItem)
            qTableWidget.setCellWidget(row, 3, qWidgetPB)
            row += 1

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

        return drivePath