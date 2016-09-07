#!/usr/bin/python
# -*- coding: utf-8 -*-

''' 
 IRRecord - API for LIRC IRRecord 

 You may use any Web Server Admin project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2016 Emilio Mariscal (emi420 [at] gmail.com)
 
 
'''

import pexpect
from os import remove, path

class IRRecord(object):

    _CFG_FILE = 'testlirc.conf'
    _LAUNCH_CMD = 'irrecord -d /dev/lirc0 '
    launched = False

    def __init__(self):
        self.launched = False

    def launch(self):
        if self.process:
            self.process.kill(0)
        if path.isfile(self._CFG_FILE):
            remove(self._CFG_FILE)
        cmd = self._LAUNCH_CMD + self._CFG_FILE
        self.process = pexpect.spawn(cmd)
        self.launched = True
        return ''

    def enter(self):
        self.process.sendline('')
        return ''

    def get_last_config(self):
        if path.isfile(self._CFG_FILE):
            content = ""
            p = pexpect.spawn('cat ' + self._CFG_FILE)
            while True:
                out = p.readline()
                if out == '' and p.eof() is not None:
                    break
                if out:
                    content = content + out
        else:
            content = "File not found. \n"
        return content

    def get_namespace(self):
        content = ""
        p = pexpect.spawn('irrecord --list-namespace | grep KEY')
        while True:
            out = p.readline()
            if out == '' and p.eof() is not None:
                break
            if out:
                content = content + out
        return content

    def mode2(self):
        if not self.launched:
            self.launched = True
            self.process = pexpect.spawn('mode2 -d /dev/lirc0')
            return ''
        else:
            return 'Stop irrecord first. \n'

    def send(self, command):
        self.process.sendline(command)
        return ''

    def status(self):
        try:
            out = self.process.read_nonblocking(size=1024, timeout=1)
        except:
            if not self.process.isalive():
                out = '[EOF]'
            else:
                out = ''
        return out

    def kill(self):
        self.process.kill(0)
        self.launched = False
        return ''

