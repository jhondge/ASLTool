# -*- coding: utf-8 -*-

__author__ = 'Vitor Chen'

import sys


def is_str_valid(tar_str):
    if isinstance(tar_str, str) and len(tar_str) > 0:
        return True
    else:
        return False


def to_str(s):
    if bytes != str:
        if type(s) == bytes:
            return s.decode('utf-8')
    return s


def print_err(msg):
    print(msg, file=sys.stderr)
