"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from .utils import validate_config

#
# Copyright (c) 2018, salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause

__author__ = "Shaohui Liu, Sankar Rao Bhogi, and Colin Zhu"
__copyright__ = "Copyright 2019, wavekit"
__credits__ = ["Shaohui Liu", "Sankar Rao Bhogi", "Colin Zhu",
               "Lisa Wang", "Jiang Zhang"]
__license__ = "BSD-3-Clause"
__version__ = "1.0.0"
__maintainer__ = "Shaohui Liu"
__email__ = "shaohui.liu@salesforce.com"
__status__ = "Production"

class LoginInfo(object): 
    """
    User defined login info. allow secret service stored password if
    """
    def __init__(self, section_name, config):
        login_section = section_name
        self.username = config.get(login_section, 'username')
        self.password = config.get(login_section, 'password')
        self.clientID = config.get(login_section, 'clientID')
        self.clientSecret = config.get(login_section, 'clientSecret')
        self.grantType = config.get(login_section, 'grantType')
        validate_config(self.__dict__)


class DBConfig:
    """
    User defined database configuration info.
    """
    def __init__(self, hostname, database, username, password, timeout):
        self.hostname = hostname
        self.database = database
        self.username = username
        self.password = password
        self.timeout = timeout
        validate_config(self.__dict__)
