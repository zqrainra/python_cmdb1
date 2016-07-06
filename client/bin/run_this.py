#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Bob'

import os,sys,platform

if platform.system() == 'Windows':
    BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
else:
    BASE_DIR = '/'.join(os.path.realpath(__file__).split('/')[:-2])
sys.path.append(BASE_DIR)

from core import HouseStark

if __name__ == '__main__':
    HouseStark.ArgvHandle(sys.argv)