"""

Copyright (c) 2021 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""
__author__ = "Shirin Khan <shirkhan@cisco.com>"
__copyright__ = "Copyright (c) {{current_year}} Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import os
import pandas as pd
from datetime import datetime


DATEFORMAT = "%m-%d-%Y_%H%M%S.%f"


def make_dir(dir_full_path):
    """
    Create dir if not exists
    :param dir_full_path: Full path of dir to create
    """
    if not os.path.exists(dir_full_path):
        os.makedirs(dir_full_path)


def build_report(result, report_name, dir_report):
    """
    This function creates a report on result
    :param: device_vlan list
    :return:
    """
    current = datetime.utcnow().strftime(DATEFORMAT)[:-3]
    query_report = dir_report + os.sep + report_name + "_" + current + ".csv"
    list_to_csv(result, query_report)


def list_to_csv(data, filename):
    """
    This function converts list to csv file
    :param data: data
    :param filename: full path csv filename
    :return: no return value
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
