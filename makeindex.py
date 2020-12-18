import sys
import urllib.parse


if __name__ == '__main__':
    print('<style>video { max-width: 100%; min-height: 320px; max-height: 40vh }</style>')
    for mp4 in sys.argv[1:]:
        mp4 = mp4.split('/')[-1]
        base = mp4.split('.')[0]
        imdb = open(f'inputs/{base}.imdb').read().strip()
        title = urllib.parse.unquote_plus(open(f'gen/{base}.title').read().strip())
        print(f'<div><h3><a href="{imdb}">{title}</a></h3>')
        print(f'<video controls src="{mp4}"></div>')
