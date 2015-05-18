from lib.models.base_model import BaseModel, StringField


class Feed(BaseModel):
    id = StringField()
    source = StringField
    url = StringField()
