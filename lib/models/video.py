from lib.models.base_model import Model, StringField


class Video(Model):
    id = StringField()
    description = StringField()
    feed_id = StringField()
    thumbnail_url = StringField()
    source = StringField()
