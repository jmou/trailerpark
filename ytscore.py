import json
import math
import os
import re
import sys
from datetime import date, timedelta


DEBUG = True if os.environ.get('DEBUG') else False


def parse_published(publishedTime):
    match = re.fullmatch(r'(?:Streamed )?(\d+) (\w+) ago', publishedTime)
    num, unit = int(match[1]), match[2]
    unit += '' if unit[-1] == 's' else 's'
    if unit == 'months':
        num *= 30
        unit = 'days'
    elif unit == 'years':
        num *= 365
        unit = 'days'
    return date.today() - timedelta(**{unit: num})


def score_age(lead_days):
    # aim for 2-6 month with falloff
    x = lead_days - 150
    # Wolfram Alpha: plot y=5e^-(((x-130)/150)^2/2), x=-100..400
    boost = 5 * math.e ** -((x/150) ** 2 / 2)
    # Wolfram Alpha: plot y=(x/300)^6, x=-600..600
    # penalty = (x/300) ** 6
    return boost


def score_candidates(imdb, candidates):
    published = date(*(int(c) for c in imdb['datePublished'].split('-')))
    for rank, candidate in enumerate(candidates):
        yt_published = parse_published(candidate['publishedTimeText'])
        lead_days = (published - yt_published).days
        agescore = score_age(lead_days)
        logView = math.log(candidate['views'])
        verified = 'VERIFIED' in candidate['ownerBadges']
        byline = candidate['longBylineText']
        cc = 'CC' in candidate['badges']
        rankscore = 20 - rank
        penalty = sum(badword in candidate['title'].lower() for badword in
                      ('teaser', 'trailer 2', 'trailer 3', 'new'))
        score = rankscore + logView + agescore + verified + cc - penalty
        if DEBUG:
            print(candidate['title'], file=sys.stderr)
            print(score, penalty, rank, candidate['videoId'], byline, file=sys.stderr)
            print(f'{rankscore:02} {lead_days} {agescore:f} {logView} V:{verified} CC:{cc}', file=sys.stderr)
            print(file=sys.stderr)
        candidate['score'] = score
        yield candidate


if __name__ == '__main__':
    _, imdb, signals = sys.argv
    with open(imdb) as fh:
        imdb = json.load(fh)
    with open(signals) as fh:
        ranked = sorted(score_candidates(imdb, json.load(fh)), key=lambda c: c['score'])
    pick = ranked[-1]
    print(f"pick: {pick['title']} @@ {pick['longBylineText']}", file=sys.stderr)
    print(pick['videoId'])
