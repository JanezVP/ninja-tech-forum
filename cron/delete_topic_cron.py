import datetime

from handlers.base import BaseHandler
from models.topic import Topic

class DeleteTopicsCron(BaseHandler):
    def get(self):
        topics = Topic.query(Topic.deleted == True,
                             Topic.updated < datetime.datetime.now() - datetime.timedelta(days=30)).fetch()

        for topic in topics:
            topic.key.delete()