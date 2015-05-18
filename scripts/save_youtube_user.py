import sys
import os
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(_root)

from lib.feed.youtube import YoutubeFeed
from config.app_config import init_config, init_cassandra


def main(username):
    env = os.environ.get('RIPPLEENV')
    init_config(env)
    init_cassandra(env)
    videos = YoutubeFeed.get_videos_from_username(sys.argv[1])
    # save all videos
    for video in videos:
        video.save()


if __name__ == "__main__":
    main(sys.argv[1])
