
import os
import sys

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile

from .._actionBase import _ActionBase


class Action(_ActionBase):

    def __init__(self):
        '''
        '''

        super().__init__(__file__, 'Dummy', 'Misc')

        self._buildUi()
