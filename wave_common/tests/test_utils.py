"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# -*- coding: utf-8 -*-

import sys
import os
import mock
import unittest
import re
import tempfile
from datetime import datetime, date
import shutil
import wave_common.utils as utils

class CustomHTTPException(Exception):
    pass

class UtilsTestSuite(unittest.TestCase):
    """Utils test cases."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False)
        self.tmp_file.write(
            b"col1,col2,col3\nval11,val12,val13\nval21,val22,val23\n")
        self.tmp_file.close()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.tmp_dir)
        os.unlink(self.tmp_file.name)
        assert not os.path.exists(self.tmp_file.name)

    def test_read_file_lines(self):
        file_name = "file-do-not-exist"
        with self.assertRaises(SystemExit) as cm:
            utils.read_file_lines(file_name)
        self.assertEqual(cm.exception.code, 1)

        self.assertEqual(utils.read_file_lines(self.tmp_file.name),
                         ["col1,col2,col3\n", "val11,val12,val13\n",
                          "val21,val22,val23\n"])

    def test_read_file(self):
        with self.assertRaises(SystemExit) as cm:
            utils.read_file("file-do-not-exist")
        self.assertEqual(cm.exception.code, 1)

        self.assertEqual(utils.read_file(self.tmp_file.name),
                         "col1,col2,col3\nval11,val12,val13\nval21,val22,val23")

    def test_save_file(self):
        utils.save_file(self.tmp_file.name, "some content")
        self.assertEqual(utils.read_file(self.tmp_file.name), "some content")

    def test_exception_handler(self):
        with self.assertRaises(SystemExit) as cm:
            utils.exception_handler("error info", Exception)
        self.assertEqual(cm.exception.code, 1)

    def test_check_response(self):
        mock_response = mock.Mock(status_code=200, text="success")
        http_error = CustomHTTPException()
        mock_response.raise_for_status.side_effect = http_error
        self.assertEqual(0, mock_response.raise_for_status.call_count)

        mock_response = mock.Mock(status_code=400, text="failed")
        http_error = CustomHTTPException()
        mock_response.raise_for_status.side_effect = http_error
        try:
            self.assertRaises(http_error, utils.check_response(mock_response))
        except CustomHTTPException:
            self.assertEqual(1, mock_response.raise_for_status.call_count)

    def test_rename_with_err(self):
        self.assertEqual(
            utils.rename_with_err("fake_file_name.csv"),
            "fake_file_name_err.csv")
        self.assertEqual(
            utils.rename_with_err("fake_file_name.json"),
            "fake_file_name.json")

    def test_rename_with_schema(self):
        self.assertEqual(
            utils.rename_with_schema("fake_file_name.csv"),
            "fake_file_name_schema.json")
        self.assertEqual(
            utils.rename_with_schema("fake_file_name.json"),
            "fake_file_name.json")

    def test_is_valid_json(self):
        self.assertTrue(utils.is_valid_json('{ "age":100}'))
        self.assertTrue(utils.is_valid_json("{\"age\":100 }"))
        self.assertTrue(utils.is_valid_json('{"age":100 }'))
        self.assertFalse(utils.is_valid_json("{asdf}"))
        self.assertFalse(utils.is_valid_json('{"foo":[5,6.8],"foo":"bar"}'))

    def test_run_shell_cmd(self):
        try:
            mock.Mock(utils.run_shell_cmd("fake-cmd"))
        except RuntimeError:
            pass
        self.assertEqual(utils.run_shell_cmd("ls"), 0)

    def test_move_files(self):
        self.temp_file = tempfile.NamedTemporaryFile()
        self.assertIsNone(utils.move_files([self.temp_file.name], "."))

        with self.assertRaises(SystemExit) as cm:
            utils.move_files("file-does-not-exist", ".")
        self.assertEqual(cm.exception.code, 1)

        # cleanup
        os.unlink("./" + os.path.basename(self.temp_file.name))

    def test_remove_escape(self):
        self.assertEqual(
            utils.remove_escape("testing: &#39; &quot; &gt; &lt; &amp; &#92; \\r \\n"),
            "testing: ' \" > < & \\ \r \n")

    def test_dict_raise_on_duplicates(self):
        duplicate_dict = {("floor", 25), ("seat", 7), ("floor", 15)}
        with self.assertRaises(ValueError):
            utils._dict_raise_on_duplicates(duplicate_dict)
        no_duplicate_dict = {("floor", 25), ("seat", 7)}
        self.assertEqual(utils._dict_raise_on_duplicates(
            no_duplicate_dict), dict({("floor", 25), ("seat", 7)}))

    def test_filter_disabled(self):
        self.assertEqual(utils.filter_disabled(
            [{"is_disabled": 0}, {"is_disabled": 1}]), [{"is_disabled": 0}])

    def test_get_all_json_file(self):
        utils.run_shell_cmd("touch " + self.tmp_dir + "/fake-json1.json")
        utils.run_shell_cmd("touch " + self.tmp_dir + "/fake-json2.json")
        utils.run_shell_cmd("touch " + self.tmp_dir + "/fake-non-json")
        utils.run_shell_cmd("mkdir " + self.tmp_dir + "/fake-fir")
        test_fullpath1 = self.tmp_dir + "/fake-json1.json"
        test_fullpath2 = self.tmp_dir + "/fake-json2.json"
        test_files = [test_fullpath1, test_fullpath2]
        all_files = utils.get_all_json_file(self.tmp_dir)
        self.assertEqual(len(all_files), len(test_files))
        for f in test_files:
            self.assertTrue(f in all_files)

    def test_truncate_digits(self):
        self.assertEqual(utils.truncate_digits(36.987654), 36.98)
        self.assertEqual(utils.truncate_digits(36), 36)
        self.assertEqual(utils.truncate_digits(-1.876423), -1.87)

    def test_replace_postfix(self):
        self.assertEqual(utils.replace_postfix("fake-file_alias"), "fake-file")
        self.assertEqual(utils.replace_postfix(
            "fake-file_per_min"), "fake-file")
        self.assertEqual(utils.replace_postfix("fake-file_in_ms"), "fake-file")

    def test_singleton(self):
        instance_first = utils.singleton(list)
        instance_second = utils.singleton(list)
        self.assertEqual(instance_first, instance_second)
        self.assertIsInstance(utils.singleton(list), list)

    def test_validate_config(self):
        self.assertIsNone(utils.validate_config({"age": 24, "name": "SHD"}))
        with self.assertRaises(SystemExit) as cm:
            utils.validate_config({"age": 24, "name": "SHD", "address": None})
        self.assertEqual(cm.exception.code, 1)

    def test_copy_tree(self):
        self.src_dir = tempfile.mkdtemp()
        utils.run_shell_cmd("touch " + self.src_dir + "/src_file")
        utils.run_shell_cmd("mkdir " + self.src_dir + "/src_subdir")
        self.dst_dir = tempfile.mkdtemp()
        utils.copytree(self.src_dir, self.dst_dir)
        assert os.path.exists(self.dst_dir)
        assert os.path.exists(self.src_dir + "/src_file")

        # cleanup
        shutil.rmtree(self.src_dir)
        shutil.rmtree(self.dst_dir)
        assert not os.path.exists(self.dst_dir)
        assert not os.path.exists(self.src_dir)

    def test_get_current_file_path(self):
        my_path = utils.get_current_file_path(__file__)
        self.assertTrue(my_path.endswith('tests'))

    def test_create_timestamp(self):
        file_name = utils.create_timestamp_csv("testfolder")
        self.assertTrue(
            re.match(
                "testfolder/\d*-\d*-\d*-\d*.csv",
                file_name) is not None)

    def test_parse_ytd_date_field(self):
        dt = utils.parse_ytd_date_field('2017-04-12')
        self.assertEquals(dt.year, 2017)
        self.assertEquals(dt.month, 4)
        self.assertEquals(dt.day, 12)

    def test_format_date_key(self):
        dt = datetime(2017, 4, 12)
        self.assertEquals( utils.format_date_key(dt), '2017-04-12' )

    def test_remove_from_string(self):
        str = utils.remove_from_string('sda..io. 1', ['a', '.io. '])
        self.assertEquals('sd.1', str)

    def test_save_as_csv(self):
        file_name = self.tmp_dir + '/tmp.csv'
        header = ["col1", "col2", "col3"]
        rows = [
            [1.1, 1.2, 1.3],
            [2.1, 2.2, 2.3],
            [3.1, 3.2, 3.3]
        ]
        utils.save_as_csv(file_name, header, rows)
        self.assertTrue(os.path.exists(file_name))
        file_content = []
        with open(file_name, 'r') as csv_file:
            for row in csv_file:
                file_content.append(row.strip())
        self.assertEquals(len(file_content), 4)
        self.assertEquals(file_content[0], "col1,col2,col3")
        self.assertEquals(file_content[1], "1.1,1.2,1.3")
        self.assertEquals(file_content[2], "2.1,2.2,2.3")
        self.assertEquals(file_content[3], "3.1,3.2,3.3")

if __name__ == '__main__':
    unittest.main()
