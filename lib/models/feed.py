from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Feed(BaseModel):
    id = StringField()
    source = StringField
    url = StringField()
