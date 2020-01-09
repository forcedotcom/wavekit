"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys
import subprocess
import time

from configparser import ConfigParser


# Author: jiang.zhang

# Class to check the Capad status and upload csv dataset to gus
class StatusChecker():
    config = None
    ROOT_DIR = ""
    LAST_PROCESSED_FILE = None
    SOURCE = ""
    RUNNING_ENV = ""
    PULL_TIMESPAN = 0
    PULLER_DELAY_OFFSET_SEC = 0
    last_ts = 0
    new_ts = ""

    PYTHON_PATH = ""
    UPLOADER_DIR = ""
    UPLOADER_EXE = ""
    UPLOADER_CONF = ""
    UPLOADER_MODE = ""
    EMAIL_RECIPIENTS = ""

    def __init__(self):
        pass

    # get configs from ini file
    def get_configs(self, config_file):
        # instantiate
        print("config file is %s"%config_file)
        self.config = ConfigParser()
        # parse existing file
        self.config.read(config_file)
        self.set_vars(config_file)

    # Initialize Variables
    def set_vars(self, config):
        print("Setting config variables")
        self.ROOT_DIR = self.config.get('checker', 'ROOT_DIR')
        self.LAST_PROCESSED_FILE = self.ROOT_DIR + "/last_processed"
        self.SOURCE = self.config.get('checker', 'SOURCE')
        self.RUNNING_ENV = self.config.get('checker', 'RUNNING_ENV')
        self.PULL_TIMESPAN = int(self.config.get('checker', 'PULL_TIMESPAN'))
        self.PULLER_DELAY_OFFSET_SEC = int(self.config.get('checker', 'PULLER_DELAY_OFFSET_SEC'))

        self.PYTHON_PATH = self.config.get('uploader', 'PYTHON_PATH')
        self.UPLOADER_DIR = self.config.get('uploader', 'UPLOADER_DIR')
        self.UPLOADER_EXE = self.config.get('uploader', 'UPLOADER_EXE')
        self.UPLOADER_CONF = self.config.get('uploader', 'UPLOADER_CONF')
        self.UPLOADER_MODE = self.config.get('uploader', 'UPLOADER_MODE')
        self.EMAIL_RECIPIENTS = self.config.get('uploader', 'EMAIL_RECIPIENTS')

    # run any shell command and get success/error result - returns 0 for success , otherwise error code
    def runShellCmd(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        stdout_data, stderr_data = p.communicate()
        if p.returncode != 0:
            raise RuntimeError(
                "%r failed, status code %s stdout %r stderr %r" % (cmd, p.returncode, stdout_data, stderr_data))
        return p.returncode

    # Send email on Failure
    def email_and_exit(self, msg):
        email_subject = self.RUNNING_ENV + " " +  self.SOURCE + " data uploader failed for day " + str(self.last_ts)
        cmnd = 'echo "' + msg + '" | mail -s "' + email_subject + '" ' + self.EMAIL_RECIPIENTS
        self.runShellCmd(cmnd)
        exit(1)

    # Check current ts and upload csv data
    def check_ts_and_upload(self):
        with open(self.LAST_PROCESSED_FILE, 'r') as date_file:
            self.last_ts = int(date_file.read().strip())
        print("last processed %d " % self.last_ts)

        self.new_ts = self.last_ts + self.PULL_TIMESPAN
        print("new data %d " % self.new_ts)

        # wait for 4 hours for data to appear
        if (time.time() - self.new_ts) < self.PULLER_DELAY_OFFSET_SEC * 60 * 60 :
            print("running in future...exiting")
            sys.exit(1)

        cmd = self.PYTHON_PATH + " " + self.UPLOADER_DIR + "/" + self.UPLOADER_EXE + " " + self.UPLOADER_DIR + "/" + self.UPLOADER_CONF + " --" + self.UPLOADER_MODE
        print("uploader command is:\n" + cmd)
        try:
            self.runShellCmd(cmd)
        except RuntimeError as e:
            print(e)
            self.email_and_exit("csv uploader failed...exiting")

        with open(self.LAST_PROCESSED_FILE, 'w') as date_file:
            print("writing the date processed file")
            date_file.write(str(self.new_ts))


if __name__ == '__main__':
    checker = StatusChecker()
    checker.get_configs(sys.argv[1])
    checker.check_ts_and_upload()
