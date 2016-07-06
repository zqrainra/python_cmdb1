#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Bob'

import sys,info_collection,json

class ArgvHandle(object):
    def __init__(self,argv):
        self.argv = argv
        self.handle()

    def handle(self):
        if len(self.argv) < 2:
            sys.exit('\033[31;1m2 argument expected,recived 1\033[0m')
        if hasattr(self,self.argv[1]):
            parse_data = getattr(self,self.argv[1])
            parse_data()
        else:
            self.help_msg()

    def help_msg(self):
        help_data = '''\tUSAGE:\r\n\t\033[032;1mcollect_data\r\n\treport_data\033[0m'''
        print(help_data)

    def collect_data(self):
        obj = info_collection.InfoCollect()
        print(json.dumps(obj.collect()))

    def report_data(self):
        print('going to report data')
        pass

