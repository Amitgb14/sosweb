# -*- coding: utf-8 -*-

import ConfigParser
import os
import sys


name = '/etc/sosweb/sosweb.cfg'
if not os.path.exists(name):
    raise Exception('Please add a proper cofig file under /etc/sosweb/')

config = ConfigParser.RawConfigParser()
config.read(name)

HOST        =  config.get('sosweb', 'host') or '127.0.0.1'
PORT        =  config.getint('sosweb', 'port') or 9770
DEBUG       =  config.getboolean('sosweb', 'debug')

REPORT_PATH =  config.get('sosweb', 'path')

PAGESIZE    =  config.getint('sosweb', 'pagesize')
