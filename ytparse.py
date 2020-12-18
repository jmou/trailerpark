import json
import sys


VIDEO_TEXT_FIELDS = (
    'descriptionSnippet',
    'lengthText',  # 2:24
    'longBylineText',  # Pixar
    'ownerText',  # Pixar
    'publishedTimeText',  #  9 months ago
    'title',
    'viewCountText',  # 4,214,634 views
)


def text(content):
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
    result['views'] = int(result.pop('viewCountText').split(' ')[0].replace(',', ''))


def search_results(ytInitialData):
    contents = (ytInitialData["contents"]["twoColumnSearchResultsRenderer"]
                ["primaryContents"]["sectionListRenderer"]["contents"][0]
                ["itemSectionRenderer"]["contents"])
    for content in contents:
        video = content.get('videoRenderer')
        if video:
            result = {field: text(video[field]) for field in VIDEO_TEXT_FIELDS}
            result['videoId'] = video['videoId']  # Gs--6c7Hn_A
            result['badges'] = list(badges(video.get('badges')))
            result['ownerBadges'] = list(badges(video.get('ownerBadges')))
            tidy_result(result)
            yield result


if __name__ == '__main__':
    results = search_results(json.load(sys.stdin))
    json.dump(list(results), sys.stdout, indent=4)
