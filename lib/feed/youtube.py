import os
from apiclient.discovery import build
from lib.models.videos import Videos
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
                video_details = {
                    'id': snippet['resourceId']['videoId'],
                    'source': 'youtube',
                    'description': snippet['title'],
                    'thumbnail_url': snippet['thumbnails']['high']['url'],
                }
                videos.append(video_details)
        return videos

    @classmethod
    def get_videos_from_username(cls, username):
        """ Queries the Youtube api to get the first 50 uploaded videos
        from a users uploaded videos

        Arguments:
            username: String of the youtube username of a user

        Returns:
            videos: List of Videos models
        """

        api_creds = os.environ.get('YOUTUBE_API_KEY')
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=api_creds)

        upload_id = cls._get_upload_playlist_id(youtube, username)
        videos = cls._get_uploaded_videos(youtube, upload_id)
        for video in videos:
            video.update({
                'username': username,
                'feed_id': upload_id,
            })
            yield Videos(**video)
