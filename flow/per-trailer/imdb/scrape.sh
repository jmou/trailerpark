perl -0777pe 's:.*<script type="application/ld\+json">(.*?)</script>.*:$1:s' \
    '@OUT(imdb/download.py,out/body)' > out/json
