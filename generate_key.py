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

from cryptography.fernet import Fernet

FILE_DIR = "/Users/shirkhan/PycharmProjects/Device_Onboarding"
FILENAME = FILE_DIR + "/key.txt"

if __name__ == "__main__":
    key = Fernet.generate_key()
    # Save this key in file or db
    with open(FILENAME, "wb") as file_object:
        file_object.write(key)
