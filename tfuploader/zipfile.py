import os
import zipfile
import requests

API_URL = "https://tensorflow.wq.io/sources.json"
DETAIL_URL = "https://tensorflow.wq.io/sources/%s"


def generate_zipfile(dirname, name, image_paths):
    filename = os.path.join(dirname, name)
    with zipfile.ZipFile(filename, 'w') as zf:
        for path in image_paths:
            zf.write(os.path.join(dirname, path), path)
    print("Exported to %s" % filename)


def upload_zipfile(dirname, name, url=API_URL, public=True):
    with open(os.path.join(dirname, name), 'rb') as f:
        response = requests.post(
            url,
            data={
                'name': name,
                'description': 'Uploaded via tfuploader',
                'public': public,
            },
            files={
                'file': (name, f)
            }
        )
        if response.status_code == 201:
            sid = response.json().get('id')
            print("Uploaded to " + DETAIL_URL % sid)
            return(sid)
        else:
            print("Upload failed:")
            print(response.content.decode('utf8'))
