"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

"""
This module is used to provide necessary util classes and methods for global usage.
"""

import csv
import json
import math
import os
import os.path
import shutil
import subprocess
import sys
import traceback
from datetime import datetime, date
from .core_logger import Logger

def read_file_lines(file_name):
    """
    :param file_name: type str
    :return: type list, lines of content
    """
    if os.path.isfile(file_name):
        with open(file_name, 'r') as fin:
            return fin.readlines()
    else:
        exception_handler(
            'the input %s is not a valid file.' %
            file_name, Exception)


def read_file(file_name):
    """
    :param file_name: type str
    :return: type str
    """
    if os.path.isfile(file_name):
        with open(file_name, 'r') as fin:
            return fin.read().strip()
    else:
        exception_handler(
            'the input %s is not a valid file.' %
            file_name, Exception)


def create_dirs(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def remove_dirs(dir_path):
    if not os.path.exists(dir_path):
        return
    files = os.listdir(dir_path)
    for name in files:
        os.remove(os.path.join(dir_path, name))
    os.rmdir(dir_path)


def save_file(file_name, content):
    """
    :param file_name: type str
    :param content: type str
    :return:
    """
    dir_path = os.path.dirname(file_name)
    create_dirs(dir_path)
    with open(file_name, 'w') as fout:
        fout.write(str(content))


def exception_handler(info, e):
    """
    :param info: type str
    :param e: type Exception
    :return:
    """
    logger = Logger.logger
    logger.error("Exception in user code:")
    logger.error("-" * 60)
    logger.error(info)
    logger.error(e)
    traceback.print_exc(file=sys.stdout)
    logger.error("-" * 60)
    sys.exit(1)


def check_response(r):
    """
    This method is used to check the http response. If >= 400, raise a status exception.
    :param r: requests http response
    :return:
    """
    if float(r.status_code) >= 400:
        logger = Logger.logger
        logger.error(r.status_code)
        logger.error(r.text)
        r.raise_for_status()


def rename_with_err(file_name):
    """
    This method is used to rename the file with err postfix.
    :param file_name:  type str
    :return:
    """
    return file_name.replace('.csv', '_err.csv')


def rename_with_schema(file_name):
    """
    This method is used to rename the file with schema postfix.
    :param file_name:  type str
    :return:
    """
    return file_name.replace('.csv', '_schema.json')


def run_shell_cmd(cmd):
    """
    This method is used to run the shell command.
    :param cmd:  shell command, type str
    :return: return code
    """
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    stdout_data, stderr_data = p.communicate()
    if p.returncode != 0:
        raise RuntimeError("%r failed, status code %s stdout %r stderr %r"
                           % (cmd, p.returncode, stdout_data, stderr_data))
    if stdout_data is not None and b"exception" in stdout_data:
        raise RuntimeError(
            "%r exception was found, stdout %r" % (cmd, stdout_data))
    if stderr_data is not None and b"exception" in stderr_data:
        raise RuntimeError(
            "%r exception was found, stderr %r" % (cmd, stderr_data))
    return p.returncode


def move_files(files, destination_folder):
    """
    This method is used to move the files to destination folder.
    :param files:  a list of files to move, type list
    :param destination_folder: type str
    :return:
    """
    for file_element in files:
        cmd = "/bin/mv " + file_element + " " + destination_folder
        try:
            run_shell_cmd(cmd)
        except Exception as e:
            info = "Can not move " + file_element + " to " + destination_folder
            exception_handler(info, e)


def remove_escape(s):
    """
    This method is used to replace all the escape characters.
    :param s: type str
    :return: type str
    """
    escape = (
        ("'", '&#39;'),
        ('"', '&quot;'),
        ('>', '&gt;'),
        ('<', '&lt;'),
        ('&', '&amp;'),
        ('\\', '&#92;'),
        ('\r', '\\r'),
        ('\n', '\\n'),
    )
    for code in escape:
        s = s.replace(code[1], code[0])
    return s


def _dict_raise_on_duplicates(ordered_pairs):
    """Reject duplicate keys."""
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            raise ValueError("duplicate key: %r" % (k,))
        else:
            d[k] = v
    return d


def is_valid_json(s):
    """
    Thid method is used to check whether a given string follows the json format.
    :param s: type str
    :return: type bool
    """
    try:
        _ = json.loads(s, object_pairs_hook=_dict_raise_on_duplicates)
    except ValueError as e:
        logger = Logger.logger
        logger.error(e)
        return False
    return True


def filter_disabled(s):
    """
    Filter out all disabled items.
    :param s:
    :return:
    """
    return list(filter(lambda x: "is_disabled" not in x or not x["is_disabled"], s))


def get_all_json_file(path):
    """
    This method is used to get all the json files
    :param path:
    :return:
    """
    return [os.path.join(path, f) for f in os.listdir(path) if
            f.endswith(".json") and os.path.isfile(os.path.join(path, f))]


def validate_config(config_map):
    """
    This method is used to validate all the items in config file have non-empty value.
    :param config_map:
    :return:
    """
    for key in config_map:
        #these fields are supposed to be empty because of the secret service change
        if(key == 'password' or key =='clientSecret' or key == 'clientID'):  
            continue
        if not config_map[key]:
            exception_handler(
                "the %s is empty." %
                key, Exception("null value exception"))


def truncate_digits(value):
    """
    This method is used to truncate the number to 3 decimal digits.
    :param value:
    :return:
    """
    return math.trunc(float(value) * 100) / 100.0


def copytree(src, dst, symlinks=False, ignore=None):
    """
    This method is used to copy srt to dst recursively
    :param src:
    :param dst:
    :param symlinks:
    :param ignore:
    :return:
    """
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def replace_postfix(s):
    return s.replace(
        '_alias',
        '').replace(
        '_in_ms',
        '').replace(
            '_per_min',
        '')



def import_class(cl):
    """
    import class in format of "module.class"
    """
    d = cl.rfind(".")
    classname = cl[d + 1:len(cl)]
    m = __import__(cl[0:d], globals(), locals(), [classname])
    return getattr(m, classname)

def get_current_file_path(file):
    """
    return the absolute path of the given file
    """
    dir_path = os.path.dirname(os.path.realpath(file))
    print("my path is: %s" % dir_path)
    return dir_path

def create_timestamp_csv(destination):
    """
    create csv file name based on timestamp
    """
    today = datetime.now()
    csvName = destination + "/" + today.strftime('%Y%m%d-%H-%M-%S') + ".csv"
    return csvName

def parse_ytd_date_field(date_key):
    """
    pass a date key in format of yyyy-mm-dd into datetime
    """
    return datetime.strptime(str(date_key), '%Y-%m-%d')

def format_date_key(date_field):
    """
    format a datetime into year-month-date format
    """
    return date_field.strftime('%Y-%m-%d')

def remove_from_string(str, tobeRemoveds):
    """
    remove list of strings from a string
    """
    for sub in tobeRemoveds:
        str = str.replace(sub, '')
    return str

def singleton(cls):
    """
    This method is used for provide singleton object.
    :param cls:
    :return: type method
    """
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance()

def save_as_csv(file_name, header, rows):
    with open(file_name, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        # print(header)
        writer.writerow(header)
        for row in rows:
            # print(row)
            writer.writerow(row)