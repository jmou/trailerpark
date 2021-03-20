ytid=$(<@STDOUT(yt/score.py))

youtube-dl -q -f 'bestvideo[ext=mp4][height<=?1080]+bestaudio[ext=m4a]/best' \
    --merge-output-format mp4 --no-mtime -- $ytid

# We can't directly refer to store/save because we need to implicitly include
# store/root. How should store parameterization work more generally?
chmod +x '@PARAM(store/)bin/save'
'@PARAM(store/)bin/save' *.mp4 > out/stored
