import unittest
# import httpretty
import json
from lib.feed.youtube import YoutubeFeed
import os
from apiclient.http import HttpMockSequence


class TestYoutubeFeed(unittest.TestCase):

    def test_get_videos_normal_response(self):
        valid_channel_response = {
            "items": [
                {
                    "contentDetails": {
                        "relatedPlaylists": {
                            "uploads": "UUfJQfm0E_aJJVo_mAp_QwcA"
                        },
                        "googlePlusUserId": "106672441458000734735"
                    },
                    "kind": "youtube#channel",
                    "etag": "\"xGnq791Msb9ZkY5Z0mmlqml8ilI\"",
                    "id": "UCfJQfm0E_aJJVo_mAp_QwcA"
                }
            ],
            "kind": "youtube#channelListResponse",
            "etag": "\"NO6QTeg0--oH8udsxFxbESj8IGWzWe_A\"",
            "pageInfo": {
                "resultsPerPage": 5,
                "totalResults": 1
            }
        }

        valid_playlist_response = {
            "nextPageToken": "CAEQAA",
            "items": [
                {
                    "snippet": {
                        "playlistId": "UUfJQfm0E_aJJVo_mAp_QwcA",
                        "thumbnails": {
                            "default": {
                                "url": "https://i.ytimg.com/vi/xsphY674k6A/default.jpg",
                                "width": 120,
                                "height": 90
                            },
                            "high": {
                                "url": "https://i.ytimg.com/vi/xsphY674k6A/hqdefault.jpg",  # NOQA
                                "width": 480,
                                "height": 360
                            },
                        },
                        "title": "Jack Haslam 5337d for 92 points",
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": "xsphY674k6A"
                        },
                        "channelId": "UCfJQfm0E_aJJVo_mAp_QwcA",
                        "publishedAt": "2015-03-08T17:06:19.000Z",
                        "channelTitle": "leedsajax",
                        "position": 0,
                        "description": "Great 5337d by Jack Haslam in the final of the men's 3 metre at the G-Star competition"  # NOQA
                    },
                    "kind": "youtube#playlistItem",
                    "etag": "\"NO6QTeg_mzWJs/leBzWzqujQe7BuOTLKpzWMVF7Z4\"",
                    "id": "UUlVk8-RRFkB_gCM709y0vzLBw3h-"
                }
            ],
            "kind": "youtube#playlistItemListResponse",
            "etag": "\"NO6QTeg0-3ShswIJs/CAyQ_7DV_BYEMzaYyR9TXMJHGOM\"",
            "pageInfo": {
                "resultsPerPage": 1,
                "totalResults": 357
            }
        }
        data = json.loads('/Users/chris/projects/diving-videos/tests/youtube-discover.json')
        http = HttpMockSequence(
            ({'status': '200'}, data),
            ({'status': '200'}, valid_channel_response),
            ({'status': '200'}, valid_playlist_response),
        )
        # httpretty.register_uri(
        #     httpretty.GET,
        #     'https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest',
        #     status=200,
        #     body=json.dumps({
        #         'rootUrl': 'https://www.googleapis.com/', 'servicePath': 'youtube/v3/'
        #     })
        # )


        # httpretty.register_uri(
        #     httpretty.GET,
        #     'https://www.googleapis.com/youtube/v3/channels',
        #     status=200,
        #     body=json.dumps(valid_channel_response)
        # )

        # httpretty.register_uri(
        #     httpretty.GET,
        #     'https://www.googleapis.com/youtube/v3/playlistItems',
        #     status=200,
        #     body=json.dumps(valid_playlist_response)
        # )

        for v in YoutubeFeed.get_videos_from_username('leedsajax'):
            print v
        self.assertFalse(True)
