import datetime

from handlers.base import BaseHandler
from models.topic import Topic
from models.subscribe import Subscriber

class SubscribeTopicsCron(BaseHandler):
    def get(self):
        topics = Topic.query(Topic.created < datetime.datetime.now() - datetime.timedelta(days=1),
                             Topic.updated < datetime.datetime.now() - datetime.timedelta(days=1)).fetch()

        for topic in topics:
            mail.send_mail(sender="janez.voler@gmail.com",
                           to=email.subscribe_email,
                           subject="New Topic",
                           body="New Topic created".format(topic_title,
                                                           topic_id))