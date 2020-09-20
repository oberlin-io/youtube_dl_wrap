import pandas as pd
import os
from datetime import datetime as dt
import yaml

if os.path.exists('meta.yaml'):
    with open('meta.yaml') as f:
        meta=yaml.safe_load(f.read())
else:
    meta={
        'data': [
            {
                'url': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSbU1AMpo532LANEW3kkuDdyzGDYk4r8dxnycnJzmGkdxHGiDMxfcGjotU8tih7OiL4Wv2EtaYJavj6/pub?gid=0&single=true&output=csv',
                'name': 'gdrive_list',
            },
        ],
        'cli': 'youtube-dl -x --audio-format mp3 -o',
        'log': []
    }

# Download a particular entry in meta
gdrive_list_dx=next((i for i, item in enumerate(meta['data']) if item['name']==\
'gdrive_list'),None)


def proceessVid(url, artist, subgenre, genre,):
    ts=dt.now().strftime('%Y-%m-%d %H:%M:%S')
    id_=hex(abs(hash((url))))      #bug Why is id_ different yet same URL input?
    filename=' '.join([genre, subgenre, artist, id_])
    filename='.'.join([filename,'mp3'])
    filename=os.path.join('../audio', filename)
    filenameQ="'{}'".format(filename)
    if not os.path.exists(filename):
        cmd=' '.join([meta['cli'], filenameQ, url])
        try:
            os.system(cmd)
            msg='Processed'
        except Exception as e:
            msg=e
    else:
        msg='File already exists'
    x='{}: {} {}'.format(filename, ts, msg)
    meta['log'].append(x)
    print(x)


gdrive_list=pd.read_csv(meta['data'][gdrive_list_dx]['url'])

gdrive_list['filename']=gdrive_list.apply(
    lambda r: proceessVid(r['url'], r['artist'], r['subgenre'], r['genre']),
    axis=1
)

with open('meta.yaml', 'w') as f:
    yaml.dump(meta, f)



'''
dicts = [
    { "name": "Tom", "age": 10 },
    { "name": "Mark", "age": 5 },
    { "name": "Pam", "age": 7 },
    { "name": "Dick", "age": 12 }
]
next((i for i, item in enumerate(dicts) if item["name"] == "Pam"), None)
'''