import requests
import threading


def _upload_document(name, basedir, fname):
    headers = {'Accept': 'application/xml;q=0.9,*/*;q=0.8'}
    data = {'resource': 'documentuploads', 'sync': 'N'}

    url = 'http://pluto.naresh.com/vauploads'
    with open(basedir+fname, 'rb') as fp:
        files = {'uploadfile':(fname, fp)}
        print('{0}: Uploading File - {1}'.format(name, fname))
        response = requests.post(url, data=data, files=files, headers=headers,
                                 auth=requests.auth.HTTPBasicAuth('SuplerC/suplerc1', 'confidential@12'),
                                 verify=True)
        print('{0}: {1}'.format(name, response.status_code))
        print('{0}: {1}'.format(name, response.text))

def _get_files_to_upload(basedir):
    from os import listdir
    from os.path import isfile, join
    return (f for f in listdir(basedir) if isfile(join(basedir, f)))

class DocumentUploadWorker(threading.Thread):
    def __init__(self, threadID, basedir, fname):
        super(DocumentUploadWorker, self).__init__()
        self.threadID = threadID
        self.name = 'Thread-{0}'.format(threadID)
        self.basedir = basedir
        self.fname = fname

    def run(self):
        print('Starting ' + self.name)
        _upload_document(self.name, self.basedir, self.fname)
        print('Exiting ' + self.name)


if __name__ == '__main__':
    # Create new threads
    basedir = '/home/nkhalasi/vayana/projects/testdata/pluto_test_dataset/Bug1464/'
    threads = [DocumentUploadWorker(idx, basedir, fname) for idx, fname in enumerate(_get_files_to_upload(basedir))]

    # Start new threads
    for thread in threads:
        thread.start()

    print('Exiting Main Thread')
