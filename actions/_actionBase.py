
import os
import sys

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile


class _ActionBase(object):

    def __init__(self, actionFilePath, actionName, actionCategory):
        '''
        '''

        # variables
        self.actionName = actionName
        self.actionCategory = actionCategory
        self.actionUi = None

        # config
        self._actionDir = os.path.abspath(os.path.dirname(actionFilePath))
        self._notePath = os.path.normpath(os.path.join(self._actionDir, 'data/note.txt'))
        self._configPath = os.path.normpath(os.path.join(self._actionDir, 'data/config.json'))

        # ui & commands
        self._buildUi()


    def _buildUi(self):
        '''
        '''

        # define ui file paths
        app = QApplication.instance()
        actionUiPath = os.path.normpath(os.path.join(self._actionDir, 'interface/main.ui')).replace('\\', '/')

        # open ui files
        loader = QUiLoader()
        actionUiFile = QFile(actionUiPath)
        actionUiFile.open(QFile.ReadOnly)

        # create ui objects
        self.actionUi = loader.load(actionUiPath)


    def getNote(self):
        if os.path.exists(self._notePath):
            with open(self._notePath) as f:
                lines = f.readlines()
                note = '\n'.join(lines)
        else:
            note = ''
        return note
