curl -fsLo out/html "https://www.youtube.com/results?search_query=$(<@STDOUT(imdb/title.py))+trailer"
perl -0777pe 's:.*<script nonce="[^"]*">var ytInitialData = (\{.*?});</script>.*:$1:s' out/html > out/json
