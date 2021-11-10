import os
import sys
import json
import subprocess
from functools import partial
from importlib import import_module

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox, QListWidgetItem, QFormLayout
from PySide2.QtCore import QFile

'''
Cookbook
'''


class Cookbook(object):

    def __init__(self):
        '''
        '''

        # variables
        self.__actions = {}

        # config
        self.__toolRootDir = os.path.abspath(os.path.dirname(__file__))
        self.__actionsDir = os.path.normpath(os.path.join(self.__toolRootDir, 'actions'))

        # ui & commands
        self.__buildUi()
        self.__mainUi.show()

        self.__linkCommands()
        
        # actions
        self.__setupActions()

        print('\n\n############\n# COOKBOOK #\n############\n')
        sys.exit(self.__app.exec_())


    def __buildUi(self):
        '''
        '''

        # define ui file paths
        self.__app = QApplication(sys.argv)
        mainUiPath = os.path.normpath(os.path.join(self.__toolRootDir, 'interface/main.ui')).replace('\\', '/')

        # open ui files
        loader = QUiLoader()
        mainUiFile = QFile(mainUiPath)
        mainUiFile.open(QFile.ReadOnly)

        # create ui objects
        self.__mainUi = loader.load(mainUiFile)


    def __linkCommands(self):
        '''
        '''

        self.__mainUi.menuLW.clicked.connect(self.__onChangeAction)
        self.__mainUi.funcPB.clicked.connect(partial(self.__onToggleMode, self.__mainUi.funcPB))
        self.__mainUi.codePB.clicked.connect(partial(self.__onToggleMode, self.__mainUi.codePB))


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
            self.__mainUi.codePB.setStyleSheet(styleSheetOff)

        if objectName == 'codePB':
            self.__mainUi.funcPB.setStyleSheet(styleSheetOff)
            self.__mainUi.codePB.setStyleSheet(styleSheetOn)


    def __onChangeAction(self):
        actionName = self.__getListWidget(self.__mainUi.menuLW)
        obj = self.__actions[actionName]
        actionUi = obj.actionUi
        print(self.__mainUi.actionFL)
        self.__mainUi.actionFL.itemAt(0).widget().setParent(None)
        self.__mainUi.actionFL.setWidget(0, QFormLayout.FieldRole, actionUi)
        


    ########
    # MISC #
    ########


    def __getListWidget(self, qListWidget):
        return qListWidget.currentItem().text()

    def __setListWidget(self, qListWidget, items):
        qListWidget.clear()
        for item in items:
            qListWidgetItem = QListWidgetItem()
            qListWidgetItem.setText(item)
            qListWidget.addItem(qListWidgetItem)
        return items






if __name__ == "__main__":
    Cookbook()