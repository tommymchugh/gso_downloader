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
import itertools
import tempfile
import shutil
import fire
import src.utils as utils
import src.ignition as ignition
from pathlib import Path
from multiprocessing import Pool
from typing import Dict
from functools import partial 

strings = utils.get_strings()
default_initial_path = utils.get_default_root_initial_path()
default_num_processes = 8

def download_model(output_path: str,
                   collection_entry: Dict[str, str],
                   index: int) -> None:
    with tempfile.TemporaryDirectory() as temp_dirpath:
        os.chdir(temp_dirpath)
        output_dirname = str(index)
        model = ignition.collection_entry_to_model(collection_entry)
        os.mkdir(output_dirname)
        output_metadata_path = os.path.join(output_dirname,
                                            strings['pb_filename'])
        with open(output_metadata_path, 'wb') as pb_file:
            pb_file.write(model.SerializeToString())
        model_url = ignition.get_model_download_url(strings['author'],
                                                    model.name)
        ignition.download_model(model_url,
                                strings['model_dirname'],
                                output_dirname)
        shutil.move(os.path.join(temp_dirpath, output_dirname), output_path)

def download(initial_path: str = default_initial_path,
             process_count: int = default_num_processes,
             override_root: bool = False) -> None:
    output_path = utils.get_download_root_path(initial_path)
    collection_page_count = int(strings['pages'])
    collection_entries = list()
    process_entry_pool = Pool(processes=process_count)
    download_entry_pool = Pool(processes=process_count)

    if override_root and utils.root_exists(initial_path):
        shutil.rmtree(output_path)

    utils.init_download_root(initial_path)
    page_range = list(range(1, collection_page_count+1))
    page_entries = list(process_entry_pool.map(ignition.get_collection_entries,
                                               page_range))
    process_entry_pool.close()
    process_entry_pool.join()

    merged_entries = list()
    entry_index = 1
    for entries in page_entries:
        for entry in entries:
            merged_entries.append((entry, entry_index))
            entry_index += 1

    partial_download_model = partial(download_model, output_path)
    download_entry_pool.starmap(partial_download_model, merged_entries)
    download_entry_pool.close()
    download_entry_pool.join()

if __name__ == '__main__':
    fire.Fire(download)
