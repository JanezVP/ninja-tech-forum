from google.appengine.ext import ndb
from google.appengine.api import taskqueue

class Subscriber(ndb.Model):
    subscribe_email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, subscribe_email):
        subscriber = Subscriber(subscribe_email=subscribe_email)
        subscriber.put()


        # run background task to send email to topic author
        """taskqueue.add(url='/task/email-new-topic', params={"topic_author_email": topic.author_email,
                                                            "topic_title": topic.title,
                                                            "topic_id": topic.key.id()})


        return topic"""

        return subscriber