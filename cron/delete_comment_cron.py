import datetime

from handlers.base import BaseHandler
from models.comment import Comment

class DeleteCommentsCron(BaseHandler):
    def get(self):
        comments = Comment.query(Comment.deleted == True,
                                         Comment.updated < datetime.datetime.now() - datetime.timedelta(days=30)).fetch()

        for comments in comments:
            comments.key.delete()