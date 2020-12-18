gen/index.html: makeindex.py $(patsubst inputs/%.imdb,gen/%.mp4,$(wildcard inputs/*.imdb))
	python3 $^ > $@

gen/%.imdb.html: inputs/%.imdb
	curl -fsLo $@ $$(<$<)

%.imdb.json: %.imdb.html
	perl -0777pe 's:.*<script type="application/ld\+json">(.*?)</script>.*:$$1:s' $< > $@

%.title: %.imdb.json
	python3 -c 'import json,sys,urllib.parse; print(urllib.parse.quote_plus(json.load(sys.stdin)["name"]))' < $< > $@

%.yt.html: %.title
	curl -fsLo $@ "https://www.youtube.com/results?search_query=$$(<$<)+trailer"

%.yt.json: %.yt.html
	perl -0777pe 's:.*<script nonce="[^"]*">var ytInitialData = ({.*?});</script>.*:$$1:s' $< > $@

%.signals.json: %.yt.json ytparse.py
	python3 ytparse.py < $< > $@

%.yt.video: ytscore.py %.imdb.json %.signals.json
	python3 $^ > $@.tmp
	@# don't touch the target if it's unchanged
	if cmp -s $@ $@.tmp; then rm $@.tmp; else mv $@.tmp $@; fi

%.mp4: %.yt.video
	rm -f $@
	youtube-dl -q -f 'bestvideo[ext=mp4][height<=?1080]+bestaudio[ext=m4a]/best' \
		-o $@ --merge-output-format mp4 --no-mtime $$(<$<)

.SECONDARY:
