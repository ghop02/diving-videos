from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Videos(Model):
    id = columns.Text(partition_key=True)
    description = columns.Text(partition_key=True)
    feed_id = columns.Text()
    thumbnail_url = columns.Text()
    source = columns.Text()
