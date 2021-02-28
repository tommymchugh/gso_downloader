#  Copyright 2021 Northwestern Inclusive Technology Lab
# 
#  Licensed under the Apache License, Version 2.0 (the 'License');
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an 'AS IS' BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import json
from pathlib import Path

strings_filename = 'strings.json'

def get_strings() -> str:
    strings_path = os.path.join(os.path.dirname(__file__), strings_filename)
    with open(strings_path) as strings_file:
        strings_text = strings_file.read()
        return json.loads(strings_text)

def get_download_root_path(initial_path: str) -> str:
    strings = get_strings()
    return os.path.join(initial_path, strings['output_dirname'])

def init_download_root(initial_path: str) -> None:
    root_path = get_download_root_path(initial_path)
    os.mkdir(root_path)
    os.chdir(root_path)

def root_exists(initial_path: str) -> bool:
    root_path = get_download_root_path(initial_path)
    return os.path.isdir(root_path) or os.path.isfile(root_path)

def root_is_corrupt(initial_path: str) -> bool:
    root_path = get_download_root_path(initial_path)
    return os.path.isfile(root_path)

def get_default_root_initial_path() -> str:
    return str(Path.home())
