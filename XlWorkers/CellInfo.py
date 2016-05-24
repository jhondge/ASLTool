# -*- coding: utf-8 -*-


__author__ = 'Vitor Chen'


class CellPos(object):
    def __init__(self, row=0, col=0):
        super().__init__()
        self.row = row
        self.col = col


class HeaderColInfo(object):
    def __init__(self, display_name=''):
        super().__init__()
        self.display_name = display_name


class LangColInfo(HeaderColInfo):
    def __init__(self, display_name='', code=''):
        super().__init__(display_name=display_name)
        self.code = code
