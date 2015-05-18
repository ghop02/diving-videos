from apiclient.discovery import build
import os
if __name__ == "__main__":
    import sys
    _root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sys.path.append(_root)

from lib.models.video import Video
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
# always return as many videos in each request as possible
MAX_RESULTS = 50


class YoutubeFeed(object):
    """ Performs actions on a youtube feed """

    @classmethod
    def _get_upload_playlist_id(cls, youtube, username):
        """ Grab the upload playlists id for a given user """

        results = dict(youtube.channels().list(
            part='contentDetails', forUsername=username
        ).execute())
        upload_id = None
        for item in results['items']:
            playlists = item['contentDetails']['relatedPlaylists']
            if 'uploads' in playlists:
                upload_id = playlists['uploads']

        return upload_id

    @classmethod
    def _get_uploaded_videos(cls, youtube, upload_id):
        results = dict(youtube.playlistItems().list(
            part='snippet', playlistId=upload_id, maxResults=MAX_RESULTS
        ).execute())
        videos = []
        for result in results['items']:
            snippet = result['snippet']
            if snippet['resourceId']['kind'] == 'youtube#video':
                for_video = {
                    'id': snippet['resourceId']['videoId'],
                    'source': 'youtube',
                    'description': snippet['title'],
                    'thumbnail_url': snippet['thumbnails']['high']['url']
                }
                videos.append(Video(for_video))
        print videos
        return videos

    @classmethod
    def get_videos_from_username(cls, username):
        api_creds = os.environ.get('YOUTUBE_API_KEY')
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=api_creds)

        upload_id = cls._get_upload_playlist_id(youtube, username)
        cls._get_uploaded_videos(youtube, upload_id)
        print upload_id
        print username


if __name__ == "__main__":
    YoutubeFeed.get_videos_from_username(sys.argv[1])
