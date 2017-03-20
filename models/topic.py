from google.appengine.ext import ndb
from google.appengine.api import taskqueue

class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)
    subscribers = ndb.StringProperty(repeated=True)

    @classmethod
    def create(cls, title, content, user):
        topic = Topic(title=title, content=content, author_email=user.email(),
                      subscribers=[user.email()])
        topic.put()

        # run background task to send email to topic author
        taskqueue.add(url='/task/email-new-topic', params={"topic_author_email": topic.author_email,
                                                            "topic_title": topic.title,
                                                            "topic_id": topic.key.id()})


        return topic