"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from wave_dto import DatasetRepresentation, DashboardRepresentation

def filter_dashboards_by_type(dashboards, type_name):
    """
    This file is used to filter the dashboards by type
    :param dashboards: list of dashboard object
    :param type_name:  string type, one of ['entry', 'main', 'data_dict', 'detail']
    :return:
    """
    return filter(lambda x: x.get_type() == type_name, dashboards)

def validate_link(obj, link_name, link_type, link_destination, check_type):
    """
    This file is use dto validate the link with given field.
    :param obj:  wave dashboard object
    :param link_name: string type
    :param link_type: string type, one of ['lens', 'dashboard']
    :param link_destination: string type
    :param check_type: string type, one of ['equal', 'include']
    :return:
    """

    assert isinstance(obj, DashboardRepresentation)
    assert link_name in obj.state.widgets
    assert obj.state.widgets[link_name]['type'] == 'link'
    assert obj.state.widgets[link_name]['parameters']['destinationType'] == link_type
    if 'destination' in obj.state.widgets[link_name]['parameters']:
        if check_type == 'equal':
            assert obj.state.widgets[link_name]['parameters']['destination'] == link_destination
        elif check_type == 'include':
            assert obj.state.widgets[link_name]['parameters']['destination'] in link_destination

def validate_single_dataset(json_object, conn, dataset_id, dataset_name, folder_id, app_name):
    """
    This method is used to validate the json files for datasets.
    :return:
    """
    json_object.validate(
        id=dataset_id,
        name=dataset_name,
        folder_id=folder_id,
        folder_label=app_name
    )