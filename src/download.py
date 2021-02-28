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
import src.utils as utils
import src.ignition as ignition
from pathlib import Path

# Output arguments
output_initial_path = str(Path.home())
output_dir = 'google_scanned_objects'
output_path = os.path.join(output_initial_path, output_dir)

# Static variables
strings = utils.get_strings()
collection_pages = int(strings['pages'])

if __name__ == '__main__':
    # Create the output path and change into that directory
    os.mkdir(output_path)
    os.chdir(output_path)

    # Loop through each collection and create an entry
    count = 1
    for page in list(range(1, collection_pages+1)):
        page_url = ignition.get_collection_page_url(strings['author'],
                                                    strings['collection'],
                                                    page)
        collection_page = ignition.get_collection_page(page_url)
        for collection_entry in collection_page:
            print('Downloading object #{}'.format(count))
            model = ignition.collection_entry_to_model(collection_entry)
            os.mkdir(model.name.lower())
            output_metadata_path = os.path.join(model.name.lower(),
                                                strings['pb_filename'])
            with open(output_metadata_path, 'wb') as pb_file:
                pb_file.write(model.SerializeToString())
            model_url = ignition.get_model_download_url(strings['author'],
                                                        model.name)
            ignition.download_model(model_url,
                                    strings['model_dirname'],
                                    model.name.lower())
            count += 1
