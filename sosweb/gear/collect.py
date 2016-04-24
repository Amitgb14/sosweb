# -*- coding: utf-8 -*-

import sys
import datetime
import os
import time

from stat import *
from operator import itemgetter
from subprocess import Popen, PIPE

import sosweb
import readfile

report_path = sosweb.REPORT_PATH
report_ext = ['.tar.xz']


def connect_node(node):
    if node == "127.0.0.1":
        return


def number_to_character(permission):
    per = {4: 'r', 2: 'w', 1: 'x', 0: '-'}
    perm = ''
    permission = permission[-3:]
    for number in permission:
        number = int(number)
        tmplen = 0
        if number >= 4:
            if number >= 4:
                number -= 4
            perm += per[4]
            tmplen += 1

        if number >= 2 and number < 4:
            if number >= 2:
                number -= 2
            perm += per[2]
            tmplen += 1

        if number == 1:
            perm += per[1]
            number -= 1
            tmplen += 1

        if number == 0:
            while tmplen < 3:
                perm += per[0]
                tmplen += 1
    return perm


def get_status(path):
    return os.stat(path)


def get_info(path):
    data = {}
    status = os.stat(path)
    data['created_on'] = datetime.datetime.fromtimestamp(status.st_mtime)
    data['report_size'] = status.st_size
    data['acc_permission'] = number_to_character(oct(status.st_mode))
    return data


def reports():
    # connect_node(node)
    repo = []
    for files in os.listdir(report_path):
        for ext in report_ext:
            if files.endswith(ext):
                data = get_info(report_path+'/'+files)
                data['report_name'] = files
                data['format'] = ext
                data['fstatus'] = os.access(report_path+'/'+files, os.R_OK)
                data['dfile'] = os.path.isdir(report_path +
                                              '/'+files[:-len(ext)])
                data['dstatus'] = os.access(report_path +
                                            '/'+files[:-len(ext)], os.R_OK)
                if data['dfile']:
                    dfile = get_status(report_path +
                                       '/'+files[:-len(ext)])
                    data['acc_permission'] = number_to_character(
                                              oct(dfile.st_mode))
                repo.append(data)
    repo = sorted(repo, key=itemgetter('created_on'), reverse=True)
    return repo


def read(filename, rformat=None):
    if rformat:
        return report_path+filename+'/sos_reports/sos.{}'.format(
               rformat.lower())
    if os.path.exists(report_path+filename+'/sos_reports/sos.json'):
        return readfile.plugin_read(report_path+filename)
    else:
        return False


def extract(filename):
    try:
        tmpdir = os.getcwd()
        cmd = "tar -xvf {} > /tmp/null_{}".format(
              report_path+filename, os.getpid())
        execute = Popen(cmd, shell=True, bufsize=1024,
                        stdin=PIPE, stdout=PIPE, stderr=PIPE,
                        close_fds=True, cwd=report_path)
        status = execute.wait()
        if status != 0:
            return execute.communicate()[-1], status
        return "Success", 200
    except Exception as e:
        error = "".join(e.args)
        return "File not extract successfully : <br>{}".format(error), 500
