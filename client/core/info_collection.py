#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Bob'

import platform,sys
from plugins.Linux import sysinfo as linux_info

class InfoCollect(object):
    def __init__(self):
        pass

    def get_sysinfo(self):
        sys_info = platform.system()
        return sys_info

    def collect(self):
        sys_type = self.get_sysinfo()
        if hasattr(self,sys_type):
            obj = getattr(self,sys_type)
            return obj()
        else:
            sys.exit('Only support Linux and Windows')

    def Linux(self):
        print('going to collect info')
        return linux_info.collect()

    def Windows(self):
        print('going to collect info windows')
