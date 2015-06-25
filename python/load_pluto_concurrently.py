import logging
import sys
import asyncio
import requests
from datetime import datetime as dt

log = logging.getLogger(__name__)


def _post_using_basic_auth(app_url, username, password, enable_http_debug=False, timeout=600.0, max_retries=5):
    def _post_multipart(fields, files, response_type='xml'):
        """
        Post fields and files to an http host as multipart/form-data.
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return the server's response page.
        """
        headers = {'Accept-encoding': 'gzip,deflate'}
        if response_type == 'xml':
            headers["Accept"] = "application/xml;q=0.9,*/*;q=0.8"
        else:
            headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"

        log.debug('Upload file to {0} using requests'.format(app_url))
        r = requests.post(app_url, data=dict(fields), files=files,
                                   headers=headers,
                                   auth=requests.auth.HTTPBasicAuth(username, password),
                                   timeout=timeout)
        return r.status_code, r.text
    return _post_multipart

post_file_command = _post_using_basic_auth('http://pluto.naresh.com/vauploads', 'SuplerC/suplerc1', 'confidential@12')

def _get_files_to_upload(basedir):
    from os import listdir
    from os.path import isfile, join
    return [f for f in listdir(basedir) if isfile(join(basedir, f))]

def _file_data(filepath):
    with open(filepath, 'rb') as fd:
        return fd.read()

@asyncio.coroutine
def _upload_file(basedir, filename):
    from os.path import join
    return post_file_command([('document_type', 'inv'), ('resource', 'documentuploads'), ('sync', 'N')], 
                             {'uploadfile': (filename, _file_data(join(basedir, filename)))},
                             response_type='html')

def _upload_files(basedir, loop):
    uploaded, tobe_uploaded = loop.run_until_complete(asyncio.wait([_upload_file(basedir, f) for f in _get_files_to_upload(basedir)]))
    for task in uploaded:
        print(task.result())

def main(basedir):
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        _upload_files(basedir, loop)
    finally:
        loop.close()

if __name__ == '__main__':
    main('/home/nkhalasi/vayana/projects/testdata/pluto_test_dataset/Bug1464')