import json
import urllib.parse

data = json.load(open('@OUT(imdb/scrape.sh,out/json)'))
print(urllib.parse.quote_plus(data['name'].lower()))
