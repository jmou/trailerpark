# venv: @OUT(venvs/requests.venv,out/python.sh)
import requests
import toml  # unused; just checks we're in the venv

with open('@PARAM(imdb_url)') as fh:
    url = fh.read().strip()
with open('out/body', 'w') as fh:
    fh.write(requests.get(url).text)
