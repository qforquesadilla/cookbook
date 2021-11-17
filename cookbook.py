import os
import sys
import json
import subprocess
from functools import partial
from importlib import import_module

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox, QListWidgetItem, QFormLayout
from PySide2.QtCore import QFile, Qt

'''
Cookbook
'''


class Cookbook(object):

    def __init__(self):
        '''
        '''

        # variables
        self.__actions = {}
        self.__actionSelected = None
        self.__actionMode = 'func'

        # config
        self.__toolRootDir = os.path.abspath(os.path.dirname(__file__))
        self.__configPath = os.path.normpath(os.path.join(self.__toolRootDir, 'data/config.json'))
        self.__actionsDir = os.path.normpath(os.path.join(self.__toolRootDir, 'actions'))

        self.__setupConfig()

        # ui & commands
        self.__buildUi()
        self.__mainUi.show()

        self.__linkCommands()
        
        # actions
        self.__setupActions()
        if self.__actionSelected:
            self.__selectListWidget(self.__mainUi.menuLW, self.__actionSelected)
            self.__changeAction(self.__actionSelected, self.__actionMode)

        print('\n\n############\n# COOKBOOK #\n############\n')
        sys.exit(self.__app.exec_())


    def __setupConfig(self):
        '''
        '''

        # load config
        try:
            configData = self.__readJson(self.__configPath)
        except Exception as err:
            print('Failed to load config: {}'.format(self.__configPath))
            print(str(err))
            return False

        # restore values
        self.__actionSelected = configData.get('actionSelected', None)

        return True


    def __buildUi(self):
        '''
        '''

        # define ui file paths
        self.__app = QApplication(sys.argv)
        mainUiPath = os.path.normpath(os.path.join(self.__toolRootDir, 'interface/main.ui')).replace('\\', '/')
        noteUiPath = os.path.normpath(os.path.join(self.__toolRootDir, 'interface/note.ui')).replace('\\', '/')

        # open ui files
        loader = QUiLoader()
        mainUiFile = QFile(mainUiPath)
        mainUiFile.open(QFile.ReadOnly)
        noteUiFile = QFile(noteUiPath)
        noteUiFile.open(QFile.ReadOnly)

        # create ui objects
        self.__mainUi = loader.load(mainUiFile)
        self.__noteUi = loader.load(noteUiFile)


    def __linkCommands(self):
        '''
        '''

        self.__mainUi.menuLW.clicked.connect(self.__onChangeAction)
        self.__mainUi.funcPB.clicked.connect(partial(self.__onToggleMode, self.__mainUi.funcPB))
        self.__mainUi.notePB.clicked.connect(partial(self.__onToggleMode, self.__mainUi.notePB))


    def __setupActions(self):
        '''
        '''

        # load actions
        actions = os.listdir(self.__actionsDir)
        for action in actions:

            if not os.path.isdir(os.path.join(self.__actionsDir, action)):
                continue

            if action == '__pycache__':
                continue
            
            module = import_module('actions.{}.{}'.format(action, action))
            obj = module.Action()
            
            actionName = obj.actionName
            self.__actions[actionName] = obj
            
            self.__setListWidget(self.__mainUi.menuLW, self.__actions.keys())




    ############
    # COMMANDS #
    ############


    def __onToggleMode(self, qPushButton):
        objectName = qPushButton.objectName()

        styleSheetOn = 'background-color: #D7E646; color: #313333'
        styleSheetOff = 'background-color: #313333; color: #f8f8f8;'
        
        if objectName == 'funcPB':
            self.__mainUi.funcPB.setStyleSheet(styleSheetOn)
            self.__mainUi.notePB.setStyleSheet(styleSheetOff)
            self.__actionMode = 'func'

        if objectName == 'notePB':
            self.__mainUi.funcPB.setStyleSheet(styleSheetOff)
            self.__mainUi.notePB.setStyleSheet(styleSheetOn)
            self.__actionMode = 'note'

        actionName = self.__getListWidget(self.__mainUi.menuLW)
        self.__changeAction(actionName, self.__actionMode)


    def __onChangeAction(self):
        actionName = self.__getListWidget(self.__mainUi.menuLW)
        self.__changeAction(actionName, self.__actionMode)
        self.__actionSelected = actionName
        self.__writeJson(self.__configPath, {"actionSelected": actionName})


    ###########
    # METHODS #
    ###########


    def __changeAction(self, actionName, mode):
        obj = self.__actions[actionName]
        actionUi = obj.actionUi

        if self.__actionMode == 'func':
            self.__mainUi.actionFL.itemAt(0).widget().setParent(None)
            self.__mainUi.actionFL.setWidget(0, QFormLayout.FieldRole, actionUi)
        else:
            self.__mainUi.actionFL.itemAt(0).widget().setParent(None)
            self.__mainUi.actionFL.setWidget(0, QFormLayout.FieldRole, self.__noteUi)
            note = obj.getNote()
            self.__setTextEdit(self.__noteUi.noteTE, note)


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
        

    def __getListWidget(self, qListWidget):
        return qListWidget.currentItem().text()


    def __setListWidget(self, qListWidget, items):
        qListWidget.clear()
        for item in items:
            qListWidgetItem = QListWidgetItem()
            qListWidgetItem.setText(item)
            qListWidget.addItem(qListWidgetItem)
        return items


    def __selectListWidget(self, qListWidget, item):
        qListWidgetItem = qListWidget.findItems(item, Qt.MatchExactly)
        qListWidget.setCurrentItem(qListWidgetItem[0])
        return qListWidgetItem


    def __setTextEdit(self, qTextEdit, text):
        qTextEdit.setText(text)
        return text





if __name__ == "__main__":
    Cookbook()