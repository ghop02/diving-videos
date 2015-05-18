from flask import Blueprint, jsonify
from lib.models.videos import Videos


videos = Blueprint('offers', __name__)


@videos.route('', methods=['GET'])
def index():
    serialized_videos = []
    for video in Videos.objects.all():
        serialized_videos.append(dict(video))

    return jsonify({'videos': serialized_videos})
