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

import logging
from datetime import datetime
from math import ceil

import requests

from dnac_config import APP_JSON, LIMIT


def get_dnac_jwt_token(auth: object, url: str) -> str:
    """
    Create the authorization token required to access DNAC
    :param auth - DNAC Basic Auth object
    :param  url: IP Address of DNAC for Different Regions
    :return dnac_jwt_token: Authentication token
    """
    auth_token = ""
    region_url = url + "/api/system/v1/auth/token"
    header = {"content-type": APP_JSON}
    # If DNAC has a certificate signed by a trusted authority change verify to True
    try:
        response = requests.post(region_url, auth=auth, headers=header, verify=False)
        if response.status_code == 200:
            auth_token = response.json()["Token"]
    except requests.exceptions.HTTPError as errHttp:
        logging.error(errHttp)
    except requests.exceptions.ConnectionError as errConnection:
        logging.error(errConnection)
    except requests.exceptions.Timeout as errTimeOut:
        logging.error(errTimeOut)
    except requests.exceptions.RequestException as err:
        logging.error(err)
    except Exception as parseException:
        logging.error(parseException)
    return auth_token


def get_site(auth_token: str, url: str, site_name: str) -> str:
    """
    Finds site id in DNAC for a site name
    :param auth_token - DNAC token
    :param  url: IP Address of DNAC for Different Regions
    :param site_name: site name
    :return site: site_id
    """
    site_id = ""
    region_url = f"{url}/dna/intent/api/v1/site?name={site_name}"
    header = {"content-type": APP_JSON, "x-auth-token": auth_token}
    # If DNAC has a certificate signed by a trusted authority change verify to True
    try:
        response = requests.get(region_url, headers=header, verify=False)
        logging.info(f"Response:{response}")
        if response.status_code == 200:
            site = response.json()["response"]
            size = len(site)
            for i in range(size):
                logging.debug(f"site: {site[i]}")
                if site[i]["siteNameHierarchy"] == site_name:
                    site_id = site[i]["id"]
                    return site_id
    except requests.exceptions.HTTPError as errHttp:
        logging.error(errHttp)
    except requests.exceptions.ConnectionError as errConnection:
        logging.error(errConnection)
    except requests.exceptions.Timeout as errTimeOut:
        logging.error(errTimeOut)
    except requests.exceptions.RequestException as err:
        logging.error(err)
    except Exception as parseException:
        logging.error(parseException)
    return site_id


def get_templateid(dnac_awt_token, temp_name, prj_name, dnac_url):
    """
    Get Template ID, Project ID
    :param dnac_awt_token: DNAC token
    :param temp_name: template name
    :param dnac_url: DNAC url
    :param prj_name: project name
    :return: template id and project id
    """
    result = {}
    tag_list = []
    temp_id, project_id = None, None
    url = (
        dnac_url
        + f"/dna/intent/api/v1/template-programmer/template?name={temp_name}&projectName={prj_name}"
    )
    logging.info("Region url {}".format(url))
    header = {"content-type": "application/json", "x-auth-token": dnac_awt_token}
    # If DNAC has a certificate signed by a trusted authority change verify to True
    try:
        response = requests.get(url, headers=header, verify=False)
        if response.status_code == 200:
            project_list = response.json()
            size = len(project_list)
            for item in project_list:
                if item["name"] == temp_name and item["projectName"] == prj_name:
                    size = len(item["tags"])
                    temp_id = item.get("templateId", "")
                    project_id = item.get("projectId", "")
                    return temp_id, project_id
    except requests.exceptions.HTTPError as errHttp:
        logging.error(errHttp)
    except requests.exceptions.ConnectionError as errConnection:
        logging.error(errConnection)
    except requests.exceptions.Timeout as errTimeOut:
        logging.error(errTimeOut)
    except requests.exceptions.RequestException as err:
        logging.error(err)
    except Exception as parseException:
        logging.error(parseException)
    return temp_id, project_id


def get_unclaimed_device_count(dnac_token: str, url: str, state: str) -> int:
    """
    Get pnp unclaimed devices total count
    :param dnac_token: Cisco DNA Center token
    :param url: Cisco DNA Center region url
    :param state: filter specified state - unclaimed
    :return: Cisco DNA Center pnp device unclaimed total count
    """
    count = 0
    region_url = f"{url}/dna/intent/api/v1/onboarding/pnp-device/count?state={state}"
    header = {"content-type": "application/json", "x-auth-token": dnac_token}
    try:
        response = requests.get(region_url, headers=header, verify=False)
        if response.status_code == 200:
            count = response.json()["response"]
            return count
    except requests.exceptions.HTTPError as errHttp:
        logging.error(errHttp)
    except requests.exceptions.ConnectionError as errConnection:
        logging.error(errConnection)
    except requests.exceptions.Timeout as errTimeOut:
        logging.error(errTimeOut)
    except requests.exceptions.RequestException as err:
        logging.error(err)
    except Exception as parseException:
        logging.error(parseException)
    return count


def get_unclaimed_device_list(auth_token: str, url: str, total_count: int, state: str, p_id: str):
    """
    Get all unclaimed devices with a specific product ID
    :param auth_token: DNAC auth token
    :param url: DNAC region url
    :param total_count: number of all unclaimed devices
    :param state: state of devices - unclaimed
    :param p_id: product ID
    :return: all devices list that are of
    """
    network_device = []
    offset_value = 0
    logging.info("Limit:{} offset: {}".format(LIMIT, offset_value))
    iterator_num = ceil(total_count / LIMIT)
    logging.info(f"iterator num: {iterator_num}")
    for idx in range(0, iterator_num):
        device_list = []
        device_list = get_unclaimed_device(auth_token, url, state, offset_value, p_id)
        #logging.info(f"size of device_list{len(network_device)}")
        #logging.info(
        #    f"Print Device List {network_device}, size of device_list{len(network_device)}"
        #)
        network_device.extend(device_list)
        offset_value += LIMIT
    logging.info(f"Print Network Device List {network_device}")
    return network_device


def get_unclaimed_device(dnac_token: str, url: str, state: str, offset: int, pid: str) -> list:
    """
    Gets all pnp devices available on DNAC of specific production id type
    :param dnac_token: Cisco DNA Center token
    :param url: Cisco DNA Center region url
    :param state: filter specified state - unclaimed
    :param offset: offset to start
    :param pid: product id
    :return: Cisco DNA Center pnp device list for a product id that are unclaimed
    """
    pnp_list = []
    region_url = (
        f"{url}/dna/intent/api/v1/onboarding/pnp-device?state={state}&pid={pid}"
    )
    header = {"content-type": "application/json", "x-auth-token": dnac_token}
    querystring = {"limit": LIMIT, "offset": offset}
    try:
        response = requests.get(
            region_url, headers=header, verify=False, params=querystring
        )
        if response.status_code == 200:
            pnp_list = response.json()
            logging.info(f"pnp_list: {pnp_list}, pnp list size:{len(pnp_list)}")
            return pnp_list
    except requests.exceptions.HTTPError as errHttp:
        logging.error(errHttp)
    except requests.exceptions.ConnectionError as errConnection:
        logging.error(errConnection)
    except requests.exceptions.Timeout as errTimeOut:
        logging.error(errTimeOut)
    except requests.exceptions.RequestException as err:
        logging.error(err)
    except Exception as parseException:
        logging.error(parseException)
    return pnp_list


def payload_claim_device(
    site_id: str, device_id: str, template_id: str, device_name: str
) -> dict:
    """
    Generate payload for claiming pnp device to a site template
    :param site_id: site id
    :param device_id: device id
    :param template_id: template id
    :param device_name: hostname of the device on DNA Center
    :return : claim to site payload dictionary
    """
    payload_claim = {
        "deviceId": device_id,
        "siteId": site_id,
        "type": "Default",
        "configInfo": {"configId": template_id, "configParameters": []},
    }
    
    return payload_claim


def payload_claim_device_csv(
    site_id: str, device_id: str, template_id: str, device_name: str
) -> dict:
    """
    Generate payload for claiming pnp device to a site template
    :param site_id: site id
    :param device_id: device id
    :param template_id: template id
    :param device_name: hostname of the device on DNA Center
    :return : claim to site payload dictionary
    """
    payload_claim = {
        "deviceId": device_id,
        "siteId": site_id,
        "type": "Default",
        "configInfo": {"configId": template_id, "configParameters": [{"key": "hostname",
                                                                    "value": device_name}]},
        }

    return payload_claim


def claim_device(payload: dict, token: str, url: str) -> str:
    """
    Claim device to site
    :param payload: pnp device claim payload
    :param token: Cisco DNA Center token
    :param url: Cisco DNAC Center Region URL
    :return
    """
    result = ""
    region_url = f"{url}/dna/intent/api/v1/onboarding/pnp-device/site-claim"
    header = {"content-type": "application/json", "x-auth-token": token}
    try:
        response = requests.post(region_url, headers=header, json=payload, verify=False)
        if response.status_code == 200:
            device_info = response.json()
            result = device_info["response"]
            logging.info(
                f"Claim device to site with payload: {payload} result:{result}"
            )
            return result
    except requests.exceptions.HTTPError as errHttp:
        logging.error(errHttp)
    except requests.exceptions.ConnectionError as errConnection:
        logging.error(errConnection)
    except requests.exceptions.Timeout as errTimeOut:
        logging.error(errTimeOut)
    except requests.exceptions.RequestException as err:
        logging.error(err)
    except Exception as parseException:
        logging.error(parseException)
    return result


def logout(dnac_jwt_token: str, url: str):
    """
    Logout from DNAC
    :param dnac_jwt_token: DNAC token
    :param url: DNA Center url
    :return:
    """
    headers = {"content-type": "application/json", "x-auth-token": dnac_jwt_token}
    url = f"{url}/logout?nocache"
    response = requests.get(url, headers=headers, verify=False)
    if not response.ok:
        logging.error(
            "Time:{0} Status Code:{1}".format(
                time=str(datetime.datetime.now()), status=str(response.status_code)
            )
        )
    logging.info("logout")
    return
