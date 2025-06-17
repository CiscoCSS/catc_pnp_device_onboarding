# catc_pnp_device_onboarding - 2023 developed script on a lower version of Catalyst Center
Advanced Feature Deep Dive: DNA Center Device Onboarding PnP with Encrypted Credential

Business Challenge: CSDL compatible DNAC credential encryption based device onboarding of Plug and play unclaimed devices to DNAC Inventory – a scalable approach. Goal: Use encrypted credentials in DNAC Api used scripts as well as provide a encryption method that meets vault, database or file store of the same.

Solution: This solution checks DNAC for Unclaimed PnP devices and helps on Onboard Devices with their Product ID to DNAC. As a result script allows to claim all unclaimed devices, that in DNAC gui gets provisioned under plug and play and gets added to DNAC inventory.

Result: Successful pnp unclaimed device onboarding takes around 3.48 seconds without user input. It takes 3.99 seconds for one device onboard with user input of hostname. Onboarding 100 devices is estimated to take 5.8 minutes and 1000 devices will take 58 minutes. It scales.

Pre-requisite: Python 3.8. If python is not installed, please follow: https://www.python.org/downloads/   ▪ pip3 or pip installed. If pip3 is not installed, please follow instructions at: https://pip.pypa.io/en/stable/installing/virtualenv installed  ▪ If virtualenv not installed already, install through bash$ pip3 install virtualenv. Follow this for further instructions: https://pypi.org/project/virtualenv/  ▪ git installed ◦if git is not installed, please try referring: https://git-scm.com/downloads   ▪ Operating System: Linux based OS or windows

Setup: ▪python3 -m venv env3 ▪source env3/bin/activate Run the command below with pip or pip3 ▪pip install --upgrade pip ▪pip install -r requirements.txt

Scripts: 6 python files

generate_key.py
generate_enc_credentials.py
onboard_device.py
dnac_config.py
dnac_api.py
util.py
How to setup: On dnac_config.py file update below variables with your local inputs: DNAC_URL_REGION1 = "https://<>" DNAC_USER_REGION1 = b"<>" DNAC_PASS_REGION1 = b"<>" FILE_DIR = "<>" REPORT_DIR = "<>/report"
Testing Instructions: Test the script in your lab settings prior to testing in production to avoid any issues. First try onboarding one device then onboard-multiple devices with it. First try one kind of product ID then try another kind of product ID to make sure it works.

Recommend: Testing on your lab setting against devices and tweaking code as needed. Not all edge cases were handled. Please do a comprehensive test of all edge cases
Run your Script: Step 1. Generate key: python generate_key.py Step 2. Generate encrypted user and password or credentials - python generate_enc_credentials.py dnac_enc_user1.txt, dnac_enc_pass1.txt are generated when you run generate_enc_credentials.py Step 3. Use it with DNAC files. Add encrypted username from dnac_enc_user1.txt and password from dnac_enc_pass1.txt to dnac_config file. Step 4. Run DNAC file: python onboard_device.py -d "C9300-48U" -s "Global/RTP/RTP-10/Floor-2" -t "usethisforpnp" -p "Onboarding Configuration"

Cisco DNA Center License: This project is licensed to you under the terms of the Cisco Sample Code License.

Disclaimer: This document is Cisco Confidential information provided for your internal business use in connection with the Cisco Services purchased by you or your authorized reseller on your behalf. This document contains guidance based on Cisco’s recommended practices. You remain responsible for determining whether to employ this guidance, whether it fits your network design, business needs, and whether the guidance complies with laws, including any regulatory, security, or privacy requirements applicable to your business.

