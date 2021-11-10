
import os
import sys

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile


class Action(object):

    def __init__(self):
        '''
        '''

        # variables
        self.actionName = 'Dummy'
        self.actionCategory = 'System'

        # config
        self.__actionRootDir = os.path.abspath(os.path.dirname(__file__))#########################INHERIT THIS

        # ui & commands
        self.__buildUi()


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
