from handlers.base import BaseHandler
from google.appengine.api import mail


class EmailNewCommentWorker(BaseHandler):
    def post(self):
        topic_author_email = self.request.get("topic_author_email")
        topic_title = self.request.get("topic_title")
        topic_id = self.request.get("topic_id")

        mail.send_mail(sender="janez.voler@gmail.com",  # add here YOUR email address (the owner of Ninja Tech Forum)
                       to=topic_author_email,  # receiver is the person who created the topic
                       subject="New comment on your topic",
                       body="Your topic received a new comment.".format(topic_title,
                                                                        topic_id))
