import webapp2

from cron.delete_topic_cron import DeleteTopicsCron
from cron.delete_comment_cron import DeleteCommentsCron
from cron.subscriber_topic_cron import SubscribeTopicsCron
from handlers.base import MainHandler, CookieAlertHandler, AboutHandler
from handlers.comments import CommentAdd, CommentsList, CommentDelete
from handlers.subscriber import SubscriberHandler
from handlers.topics import TopicAdd, TopicDetails, TopicDelete
from workers.email_new_comment import EmailNewCommentWorker
from workers.email_new_topic import EmailNewTopicWorker

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieAlertHandler, name="set-cookie"),

    webapp2.Route('/about', AboutHandler, name="about"),
    webapp2.Route('/topic/add', TopicAdd, name="topic-add"),
    webapp2.Route('/topic/<topic_id:(\d+)>', TopicDetails, name="topic-details"),
    webapp2.Route('/topic/<topic_id:(\d+)>/comment/add', CommentAdd, name="comment-add"),
    webapp2.Route('/comments/list', CommentsList, name="comment-list"),
    webapp2.Route('/subscribe', SubscriberHandler, name="subscriber"),


    #topic and comment delete
    webapp2.Route('/topic/<topic_id:\d+>/delete', TopicDelete, name='topic-delete'),
    webapp2.Route('/comment/<comment_id:\d+>/delete', CommentDelete, name='comment-delete'),

    #Workers
    webapp2.Route('/task/email-new-comment', EmailNewCommentWorker, name="task-email-new-comment"),
    webapp2.Route('/task/email-new-topic', EmailNewTopicWorker, name="task-email-new-topic"),

    #Cron
    webapp2.Route('/cron/delete-topics', DeleteTopicsCron, name='cron-delete-topics'),
    webapp2.Route('/cron/delete-comments', DeleteCommentsCron, name='cron-delete-comments'),
    webapp2.Route('/cron/subscriber-topic', SubscribeTopicsCron, name='cron-subscribe-topic'),
], debug=True)
