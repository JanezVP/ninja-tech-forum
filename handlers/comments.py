from handlers.base import BaseHandler
from models.topic import Topic
from models.comment import Comment
from google.appengine.api import users
from google.appengine.ext import ndb
from utils.decorators import validate_csrf

class CommentAdd(BaseHandler):
    @validate_csrf
    def post(self, topic_id):

        user = users.get_current_user()


        text = self.request.get('comment-text')
        topic = Topic.get_by_id(int(topic_id))

        Comment.create(content=text, user=user, topic=topic)

        return self.redirect_to("topic-details", topic_id=topic.key.id())


class CommentsList(BaseHandler):
    def get(self):

        user = users.get_current_user()

        comments = Comment.query(Comment.author_email == user.email()).fetch()

        topics_titles = set(comment.topic_title for comment in comments)

        params = {'comments': comments,
                  'topics_titles': topics_titles}

        return self.render_template('comments_list.html', params=params)


class CommentDelete(BaseHandler):
    @validate_csrf
    def post(self, comment_id):
        comment = Comment.get_by_id(int(comment_id))
        user = users.get_current_user()

        if comment.author_email == user.email() or users.is_current_user_admin():
            comment.deleted = True
            comment.put()

        return self.redirect_to("topic-details", topic_id=comment.topic_id)