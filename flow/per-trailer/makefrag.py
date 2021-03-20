import subprocess
import urllib.parse

subprocess.check_call(['chmod', '+x', '@PARAM(store/)bin/url'])
videopath = subprocess.check_output(['@PARAM(store/)bin/url',
                                     '@OUT(yt/dl.sh,out/stored)'],
                                    text=True).strip()

imdb_url = open('@PARAM(imdb_url)').read().strip()
title = urllib.parse.unquote_plus(open('@STDOUT(imdb/title.py)').read().strip())

print('<style>video { max-width: 100%; min-height: 320px; max-height: 40vh }</style>')
print(f'<div><h3><a href="{imdb_url}">{title}</a></h3>')
print(f'<video controls src="{videopath}"></div>')
