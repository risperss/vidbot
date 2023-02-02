import json
import os
import re
import requests
import time


BEARER_TOKEN = os.environ['TWITTER_BEARER_TOKEN']
X_GUEST_TOKEN = os.environ['TWITTER_GUEST_TOKEN']


# TODO: consider qs params when parsing
# Url format: https://twitter.com/JakMimmi/status/1620880851147038723
def parse_url(url: str) -> str:
    tweet_id = url.split('/')[-1]

    return tweet_id


def get_tweet_data(tweet_id: str) -> dict:
    variables = {
        'focalTweetId': tweet_id,
        'with_rux_injections': False,
        'includePromotedContent': False,
        'withCommunity': False,
        'withQuickPromoteEligibilityTweetFields': False,
        'withBirdwatchNotes': False,
        'withSuperFollowsUserFields': False,
        'withDownvotePerspective': False,
        'withReactionsMetadata': False,
        'withReactionsPerspective': False,
        'withSuperFollowsTweetFields': False,
        'withVoice': False,
        'withV2Timeline': False,
    }
    features = {
        'responsive_web_twitter_blue_verified_badge_is_enabled': False,
        'verified_phone_label_enabled': False,
        'responsive_web_graphql_timeline_navigation_enabled': False,
        'longform_notetweets_consumption_enabled': False,
        'tweetypie_unmention_optimization_enabled': False,
        'vibe_api_enabled': False,
        'responsive_web_edit_tweet_api_enabled': False,
        'graphql_is_translatable_rweb_tweet_is_translatable_enabled': False,
        'view_counts_everywhere_api_enabled': False,
        'standardized_nudges_misinfo': False,
        'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': False,
        'interactive_text_enabled': False,
        'responsive_web_text_conversations_enabled': False,
        'responsive_web_enhance_cards_enabled': False
    }

    url = 'https://api.twitter.com/graphql/6lWNh96EXDJCXl05SAtn_g/TweetDetail'
    headers = {
        'authorization': BEARER_TOKEN,
        # TODO: figure out how to get an up to date token every time
        'x-guest-token': '1620975371221966851',
    }
    params = {
        'variables': json.dumps(variables),
        'features': json.dumps(features),
    }

    r = requests.get(url, headers=headers, params=params)
    tweet_obj = r.json()

    return tweet_obj


def parse_tweet_obj(tweet_obj: dict) -> str:
    pattern = r'\"variants\":\s*\[[\s\S]*?\]'
    variants = re.search(pattern, json.dumps(tweet_obj))

    if not variants:
        raise ValueError("Tweet does not contain a video")

    urls_obj = f'{{{variants.group()}}}'
    video_variants = json.loads(urls_obj)
    def best_bitrate(x: dict): return x.get('bitrate') or -1
    video_obj = max(video_variants['variants'], key=best_bitrate)
    mp4_url = video_obj['url']

    return mp4_url


def save_mp4_url(url: str, tweet_id: str = None) -> None:
    filename = tweet_id or str(int(time.time()))
    filename += '.mp4'

    content = requests.get(url).content

    with open(filename, "wb") as file:
        file.write(content)


if __name__ == '__main__':
    url = 'https://twitter.com/JakMimmi/status/1620880851147038723'
    tweet_id = parse_url(url)
    tweet_obj = get_tweet_data(tweet_id)
    mp4_url = parse_tweet_obj(tweet_obj)
    save_mp4_url(mp4_url)
