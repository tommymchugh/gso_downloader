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
import requests
import zipfile
import urllib.parse
import urllib.request
import src.utils as utils
import src.model_pb2 as model_pb
from typing import Dict, List, Type

strings = utils.get_strings()

def get_model_download_url(author: str, model: str) -> str:
    url_params_str = '{}/models/{}/1/{}.zip'.format(author,
                                                    model,
                                                    model)
    url_params = urllib.parse.quote(url_params_str)
    return '{}/{}'.format(strings['base_url'], url_params)

def get_collection_page_url(author: str, collection: str, page: int) -> str:
    url_params_str = '{}/collections/{}/models'.format(author, collection)
    url_params = urllib.parse.quote(url_params_str)
    return '{}/{}?page={}'.format(strings['base_url'], url_params, page)

def get_collection_page(url: str) -> List[Dict[str, str]]:
    page_req = requests.get(url)
    page_resp = page_req.content.decode('utf-8')
    return json.loads(page_resp)

def collection_entry_to_model(entry: Dict[str, str]) -> Type[model_pb.Model]:
    model = model_pb.Model()
    model.name = entry['name']
    model.owner = entry['owner']
    model.description = entry['description']
    model.created_date = entry['createdAt']
    for category_name in entry.get('categories', []):
        category = model_pb.Category()
        category.name = category_name
        model.categories.extend([category])
    return model

def download_model(url: str, name: str, location: str) -> None:
    zip_name = '{}.zip'.format(name)
    zip_path = os.path.join(location, zip_name)
    output_folder_path = os.path.join(location, name)
    urllib.request.urlretrieve(url, zip_path)
    os.mkdir(output_folder_path)
    with zipfile.ZipFile(zip_path) as zip_ref:
        zip_ref.extractall(output_folder_path)
    os.remove(zip_path)

def get_collection_entries(page: int) -> List[Dict[str, str]]:
    page_url = get_collection_page_url(strings['author'],
                                                strings['collection'],
                                                page)
    return get_collection_page(page_url)
