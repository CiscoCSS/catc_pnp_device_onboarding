# catc_pnp_device_onboarding  
# 2023 developed script on a lower version of Catalyst Center
**Advanced Feature Deep Dive: DNA Center Device Onboarding PnP with Encrypted Credential**

**Business Challenge:** CSDL compatible DNAC credential encryption based device onboarding of Plug and play unclaimed devices to DNAC Inventory – a scalable approach. Goal: Use encrypted credentials in DNAC Api used scripts as well as provide a encryption method that meets vault, database or file store of the same.

**Solution:** This solution checks DNAC for Unclaimed PnP devices and helps on Onboard Devices with their Product ID to DNAC. As a result script allows to claim all unclaimed devices, that in DNAC gui gets provisioned under plug and play and gets added to DNAC inventory.

**Result:** Successful pnp unclaimed device onboarding takes around 3.48 seconds without user input. It takes 3.99 seconds for one device onboard with user input of hostname. Onboarding 100 devices is estimated to take 5.8 minutes and 1000 devices will take 58 minutes. It scales.

**Pre-requisite:**

Python 3.8+. If python is not installed, please follow: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* pip3 or pip installed. If pip3 is not installed, please follow instructions at: 
[https://pip.pypa.io/en/stable/installing/virtualenv](https://pip.pypa.io/en/stable/installing/virtualenv) installed
* If virtualenv not installed already, install through bash$ pip3 install virtualenv. Follow this for further 
instructions: [https://pypi.org/project/virtualenv/](https://pypi.org/project/virtualenv/)
* git installed ◦if git is not installed, please try referring: https://git-scm.com/downloads
Operating System: Linux based OS or windows or mac

## Setup

```bash
python3 -m venv demoenv
```
Activate virtual environment

```bash
source demo_env/bin/activate
```

Run the command below with pip or pip3

```bash
pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

or run make install on Makefile it will achieve the same.

## Installation

Git clone: 
```bash
git clone https://github.com/CiscoDevNet/catc_pnd_device_onboarding.git
```

Go to your project folder

```bash
cd device_onboarding
```
Set up a Python venv First make sure that you have Python 3 installed on your machine. We will then be using venv to create an isolated environment with only the necessary packages.
Install virtualenv via pip

```bash
pip install virtualenv
```

Create the venv
```bash
python3 -m venv venv
```
Activate your venv

```bash
source venv/bin/activate
```

Install dependencies: 

```bash
pip install -r requirements.txt 
```
or run make install on Makefile it will achieve the same.

**Setup:** ▪python3 -m venv env3 ▪source env3/bin/activate Run the command below with pip or pip3 ▪pip install --upgrade pip ▪pip install -r requirements.txt

**Scripts:** 6 python files

generate_key.py
generate_enc_credentials.py
onboard_device.py
dnac_config.py
dnac_api.py
util.py

## Usage:

## Step I. 

Modify dnac_config.py file. Change the variables below per your environment.

```python
# Update this section with the DNA Center server info
DNAC_URL_REGION1 = "https://<ip_address>"
DNAC_USER_REGION1 = b"<<encrypted username>"
DNAC_PASS_REGION1 = b"<encrypted password>"
FILE_DIR = "<<absolute path to directory where you are running the script from>>"
REPORT_DIR = "<absolute path to directory where you going to drop the reports created to>>/report"
```

## Step II. 
**Run your Script:** 
Step 1. Generate key: python generate_key.py 
Step 2. Generate encrypted user and password or credentials - python generate_enc_credentials.py dnac_enc_user1.txt, dnac_enc_pass1.txt are generated when you run generate_enc_credentials.py 
Step 3. Use it with DNAC files. Add encrypted username from dnac_enc_user1.txt and password from dnac_enc_pass1.txt to dnac_config file. 
Step 4. Run DNAC file: python onboard_device.py -d "C9300-48U" -s "Global/RTP/RTP-10/Floor-2" -t "usethisforpnp" -p "Onboarding Configuration"

**Testing Instructions:** Test the script in your lab settings prior to testing in production to avoid any issues. First try onboarding one device then onboard-multiple devices with it. First try one kind of product ID then try another kind of product ID to make sure it works.

**Recommend:** Testing on your lab setting against devices and tweaking code as needed. Not all edge cases were handled. Please do a comprehensive test of all edge cases. Check for other status code on each API, this code only handles positive pathway status code 200. Extensive testing against all scenarios needed and code needs to be modified as appropriate. Also note code was developed for lower version of Catalyst Center. Make appropriate modification as necessary to make it work. 

**Cisco Sample Code License, Version 1.1**
These terms govern this Cisco Systems, Inc. (“Cisco”), example or demo source code and its associated documentation (together, the “Sample Code”). By downloading, copying, modifying, compiling, or redistributing the Sample Code, you accept and agree to be bound by the following terms and conditions (the “License”). If you are accepting the License on behalf of an entity, you represent that you have the authority to do so (either you or the entity, “you”). Sample Code is not supported by Cisco TAC and is not tested for quality or performance. This is your only license to the Sample Code and all rights not expressly granted are reserved.

1. LICENSE GRANT: Subject to the terms and conditions of this License, Cisco hereby grants to you a perpetual, worldwide, non-exclusive, non-transferable, non-sublicensable, royalty-free license to copy and modify the Sample Code in source code form, and compile and redistribute the Sample Code in binary/object code or other executable forms, in whole or in part, solely for use with Cisco products and services. For interpreted languages like Java and Python, the executable form of the software may include source code and compilation is not required.

2. CONDITIONS: You shall not use the Sample Code independent of, or to replicate or compete with, a Cisco product or service. Cisco products and services are licensed under their own separate terms and you shall not use the Sample Code in any way that violates or is inconsistent with those terms (for more information, please visit: www.cisco.com/go/terms ).

3. OWNERSHIP: Cisco retains sole and exclusive ownership of the Sample Code, including all intellectual property rights therein, except with respect to any third-party material that may be used in or by the Sample Code. Any such third-party material is licensed under its own separate terms (such as an open source license) and all use must be in full accordance with the applicable license. This License does not grant you permission to use any trade names, trademarks, service marks, or product names of Cisco. If you provide any feedback to Cisco regarding the Sample Code, you agree that Cisco, its partners, and its customers shall be free to use and incorporate such feedback into the Sample Code, and Cisco products and services, for any purpose, and without restriction, payment, or additional consideration of any kind. If you initiate or participate in any litigation against Cisco, its partners, or its customers (including cross-claims and counter-claims) alleging that the Sample Code and/or its use infringe any patent, copyright, or other intellectual property right, then all rights granted to you under this License shall terminate immediately without notice.

4. LIMITATION OF LIABILITY: CISCO SHALL HAVE NO LIABILITY IN CONNECTION WITH OR RELATING TO THIS LICENSE OR USE OF THE SAMPLE CODE, FOR DAMAGES OF ANY KIND, INCLUDING BUT NOT LIMITED TO DIRECT, INCIDENTAL, AND CONSEQUENTIAL DAMAGES, OR FOR ANY LOSS OF USE, DATA, INFORMATION, PROFITS, BUSINESS, OR GOODWILL, HOWEVER CAUSED, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

6. DISCLAIMER OF WARRANTY: SAMPLE CODE IS INTENDED FOR EXAMPLE PURPOSES ONLY AND IS PROVIDED BY CISCO “AS IS” WITH ALL FAULTS AND WITHOUT WARRANTY OR SUPPORT OF ANY KIND. TO THE MAXIMUM EXTENT PERMITTED BY LAW, ALL EXPRESS AND IMPLIED CONDITIONS, REPRESENTATIONS, AND WARRANTIES INCLUDING, WITHOUT LIMITATION, ANY IMPLIED WARRANTY OR CONDITION OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, SATISFACTORY QUALITY, NON-INTERFERENCE, AND ACCURACY, ARE HEREBY EXCLUDED AND EXPRESSLY DISCLAIMED BY CISCO. CISCO DOES NOT WARRANT THAT THE SAMPLE CODE IS SUITABLE FOR PRODUCTION OR COMMERCIAL USE, WILL OPERATE PROPERLY, IS ACCURATE OR COMPLETE, OR IS WITHOUT ERROR OR DEFECT.

7. GENERAL: This License shall be governed by and interpreted in accordance with the laws of the State of California, excluding its conflict of laws provisions. You agree to comply with all applicable United States export laws, rules, and regulations. If any provision of th
