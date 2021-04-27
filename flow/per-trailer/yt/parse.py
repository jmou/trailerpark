import json
import sys


VIDEO_TEXT_FIELDS = (
    'descriptionSnippet',
    'lengthText',  # 2:24
    'longBylineText',  # Pixar
    'ownerText',  # Pixar
    'publishedTimeText',  # 9 months ago
    'title',
    'viewCountText',  # 4,214,634 views
)


def text(content):
    if content is None:
        return ''
    text = content.get('simpleText')
    if text is not None:
        return text
    # runs of formatted text
    return ''.join(r['text'] for r in content['runs'])


def badges(contents):
    if not contents:
        return
    for item in contents:
        badge = item['metadataBadgeRenderer']
        if badge['style'] == 'BADGE_STYLE_TYPE_VERIFIED':
            yield 'VERIFIED'
        elif badge['style'] == 'BADGE_STYLE_TYPE_SIMPLE':
            yield badge['label']


def tidy_result(result):
    try:
      result['views'] = int(result.pop('viewCountText').split(' ')[0].replace(',', ''))
    except Exception:
      result['views'] = 1


def search_results(ytInitialData):
    primaryContents = (ytInitialData['contents']
                       ['twoColumnSearchResultsRenderer']['primaryContents'])
    # YouTube returns results in varying formats.
    if 'sectionListRenderer' in primaryContents:
        contents = (primaryContents["sectionListRenderer"]["contents"][0]
                    ["itemSectionRenderer"]["contents"])
    else:
        contents = primaryContents['richGridRenderer']['contents']
        contents = [item['richItemRenderer']['content']
                    for item in contents
                    if 'richItemRenderer' in item]
    for content in contents:
        video = content.get('videoRenderer')
        if video:
            result = {field: text(video.get(field)) for field in VIDEO_TEXT_FIELDS}
            result['videoId'] = video['videoId']  # Gs--6c7Hn_A
            result['badges'] = list(badges(video.get('badges')))
            result['ownerBadges'] = list(badges(video.get('ownerBadges')))
            tidy_result(result)
            yield result


if __name__ == '__main__':
    data = json.load(open('@OUT(yt/scrape.sh,out/json)'))
    results = search_results(data)
    json.dump(list(results), sys.stdout, indent=4)
