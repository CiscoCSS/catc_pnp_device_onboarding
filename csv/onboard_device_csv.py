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

import argparse
import datetime
import logging
import os
import urllib3
from argparse import RawTextHelpFormatter
from cryptography.fernet import Fernet
from glom import glom
from requests.auth import HTTPBasicAuth
from time import perf_counter as times
from urllib3.exceptions import InsecureRequestWarning
import dnac_api as dnac_api
import util as util
from dnac_config import (
    CLAIM_REPORT,
    CSV_DIR,
    CSV_FILE,
    DNAC_URL_REGION1,
    DNAC_USER_REGION1,
    DNAC_PASS_REGION1,
    FILENAME,
    FILE_DIR,
    NOT_CLAIM_REPORT,
    REPORT_DIR,
    LOG_FILENAME
)


def decrypt_credential(filename: str, e_user: str, e_pass: str) -> HTTPBasicAuth:
    """
    This function decrypts credential and uses http basic auth
    :param filename: file name
    :param e_user: encrypted username
    :param e_pass: encrypted password
    :return http basic auth : http basic auth
    """
    with open(FILENAME, "rb") as file_object:
        for line in file_object:
            enc_key = line
    cipher_suite = Fernet(enc_key)
    dnac_uncipher_user1 = cipher_suite.decrypt(DNAC_USER_REGION1)
    dnac_uncipher_pwd1 = cipher_suite.decrypt(DNAC_PASS_REGION1)
    plain_text_enc_username = bytes(dnac_uncipher_user1).decode("utf-8")
    plain_text_enc_password = bytes(dnac_uncipher_pwd1).decode("utf-8")
    dnac_auth1 = HTTPBasicAuth(plain_text_enc_username, plain_text_enc_password)
    return dnac_auth1


if __name__ == "__main__":
    claim_list, unclaimed_list = [], []
    device_id, site_id, template_id = "", "", ""
    startTime = datetime.datetime.utcnow().strftime("%m-%d-%Y_%H%M%S.%f")[:-3]
    logging.basicConfig(
        # If you want to keep track in log then open this commented out application_run.log file
        # filename=LOG_FILENAME + '_'+ str(startTime) + '.log',
        # Logging INFO, ERROR, DEBUG
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    parser = argparse.ArgumentParser(
        description="Bulk Configuration with Templates.",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "--device", "-d", type=str, required=True, help="product id or pid"
    )
    parser.add_argument("--site", "-s", type=str, required=True, help="site/floor path")
    parser.add_argument(
        "--template", "-t", type=str, required=True, help="template name"
    )
    parser.add_argument("--project", "-p", type=str, required=True, help="project name")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="set logging:  DEBUG "
    )
    logging.info("Starting application .....")
    start = times()
    logging.info(start)
    #line added
    column_name = 'serial_number'
    DEVICE_FILE = FILE_DIR + CSV_DIR + os.sep + CSV_FILE
    data = util.csv_dataframe(DEVICE_FILE)
    ###
    args = parser.parse_args()
    device_type = args.device
    site_name = args.site
    template_name = args.template
    project_name = args.project
    auth1 = decrypt_credential(FILENAME, DNAC_USER_REGION1, DNAC_PASS_REGION1)
    decrypt_time = times()
    logging.info(f"Decryption time:{decrypt_time-start}")
    token = dnac_api.get_dnac_jwt_token(auth1, DNAC_URL_REGION1)
    site_id = dnac_api.get_site(token, DNAC_URL_REGION1, site_name)
    logging.info(f"Site id:{site_id}")
    template_id, project_id = dnac_api.get_templateid(
        token, template_name, project_name, DNAC_URL_REGION1
    )
    logging.info(f"template_id:{template_id}, project_id:{project_id}")
    unclaimed_count = dnac_api.get_unclaimed_device_count(
        token, DNAC_URL_REGION1, "Unclaimed"
    )
    unclaimed_devices = dnac_api.get_unclaimed_device_list(
        token, DNAC_URL_REGION1, unclaimed_count, "Unclaimed", device_type
    )
    for device in unclaimed_devices:
        not_claimed = {
            "serial_number": glom(device, "deviceInfo.serialNumber", default=""),
            "hostname": glom(device, "deviceInfo.hostname", default=""),
            "product_id": glom(device, "deviceInfo.pid", default=""),
            "device_id": glom(device, "id", default=""),
        }
        logging.info(f"Not claimed: {not_claimed}")
        logging.info(
            f"Project_id:{project_id}, site id: {site_id}, template_id:{template_id}"
        )
        logging.info(f"device_id: {not_claimed['device_id']}")
        ### Line added
        pos_arr = data[data[column_name] == str(not_claimed.get('serial_number').strip())].index.values
        index = pos_arr[0]
        logging.info(f'index: {pos_arr} : {index}')
        hostname = data[data.columns[0]][index]
        logging.info(f'host: {hostname}')
        #hostname = input("Please enter hostname: ")
        if not_claimed["device_id"] != "" and site_id != "" and template_id != "":
            claim_payload = dnac_api.payload_claim_device(
                site_id, not_claimed["device_id"], template_id, hostname
            )
            logging.info(f"Payload Claim:{claim_payload}")
            output = dnac_api.claim_device(claim_payload, token, DNAC_URL_REGION1)
            logging.info(f"Result claim_payload:{claim_payload} and output: {output}")
            if output == "Device Claimed":
                not_claimed["site_id"] = site_id
                not_claimed["template_id"] = template_id
                claim_list.append(not_claimed)
        else:
            logging.info(
                f"Could not claim device: Device ID:{device_id} Site ID:{site_id} Template ID: {template_id}"
            )
            logging.info(
                f"Serial Number: {not_claimed['serial_number']} and Product ID: {not_claimed['product_id']}"
            )
            unclaimed_list.append(not_claimed)
    logging.info(
        f"PnP Claimed Device List: {claim_list}, and failed to claim list: {unclaimed_list}"
    )
    util.make_dir(REPORT_DIR)
    if len(claim_list) > 0:
        util.build_report(claim_list, CLAIM_REPORT, REPORT_DIR)
    if len(unclaimed_list) > 0:
        util.build_report(unclaimed_list, NOT_CLAIM_REPORT, REPORT_DIR)
    end = times()
    logging.info("Completed in: {} seconds.".format(end - start))
    dnac_api.logout(token, DNAC_URL_REGION1)
