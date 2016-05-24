# -*- coding: utf-8 -*-
from enum import Enum

from XlWorkers.CellInfo import *

__author__ = 'Vitor Chen'

DEBUG = False


# language list
class Lang(Enum):
    EN = ('en', 'English', ('', ))
    ZH = ('zh', '简中')
    ZH_rHK = ('zh_HANT', '繁體', ('zh-rHK', 'zh-rTW'))
    VI = ('vi', '越南语')
    IN = ('in', '印尼语')
    TR = ('tr', '土耳其语')
    TH = ('th', '泰语')
    ES = ('es', '西班牙语')
    FR = ('fr', '法语')
    DE = ('de', '德语')
    JA = ('ja', '日语')
    PT = ('pt', '葡萄牙语')
    IT = ('it', '意大利语')
    RU = ('ru', '俄语')
    KO = ('ko', '韩语')

    def __init__(self, code, title, region_codes=None):
        self.code = code
        self.title = title
        if region_codes is None:
            region_codes = (code, )
        self._region_codes = region_codes

    def reverse_region_codes(self):
        for region_code in self._region_codes:
            yield region_code


class Config(object):
    KEY_COL_POS = 1
    DESC_COL_POS = 2
    LANG_COL_START = 3

    CONTENT_ROW_START = 2

    HEADER_COL_LIST = [HeaderColInfo('String res key'),
                       HeaderColInfo('Description'), ]
    for lang_code in Lang:
        HEADER_COL_LIST.append(LangColInfo(lang_code.title, lang_code.code))

    LANG_COL_CODE_MAP = {}
    LANG_COL_POS_MAP = {}

    for i in range(1, len(HEADER_COL_LIST) + 1):
        headerCol = HEADER_COL_LIST[i - 1]
        if isinstance(headerCol, LangColInfo):
            cellPos = CellPos(1, i)
            LANG_COL_CODE_MAP[headerCol.code] = cellPos
            LANG_COL_POS_MAP[cellPos.col] = headerCol

    if DEBUG:
        print(HEADER_COL_LIST)
        print(LANG_COL_CODE_MAP)
        print(LANG_COL_POS_MAP)
