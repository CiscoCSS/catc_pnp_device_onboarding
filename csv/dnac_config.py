"""

Copyright (c) 2025 Cisco and/or its affiliates.

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

# Update this section with the DNA Center server info
DNAC_URL_REGION1 = "https://<ip_address>"

DNAC_USER_REGION1 = b"<<encrypted username>"
DNAC_PASS_REGION1 = b"<encrypted password>"

FILE_DIR = "<<absolute path to directory where you are running the script from>>"
KEY_FILE = "key.txt"
USER_FILE = "enc_user1.txt"
PASS_FILE = "enc_pass1.txt"
FILENAME = FILE_DIR + KEY_FILE
ENC_USER1_FILE = FILE_DIR + USER_FILE
ENC_PASS1_FILE = FILE_DIR + PASS_FILE
APP_JSON = "application/json"
REPORT_DIR = "<absolute path to directory where you going to drop the reports created to>>"
CLAIM_REPORT = "claim"
NOT_CLAIM_REPORT = "not_claimed"
SWITCH_BASENAME = "edge"
LIMIT = 50
LOG_FILENAME = "onboarding"
CSV_DIR = 'Device'
CSV_FILE = 'device_list.csv'
