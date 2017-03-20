from handlers.base import BaseHandler
from google.appengine.api import users
from models.topic import Topic
from models.comment import Comment
from utils.decorators import validate_csrf

class TopicAdd(BaseHandler):

    def get(self):
        return self.render_template_with_csrf('topic_add.html')

    @validate_csrf
    def post(self):

        user = users.get_current_user()

        #if not user:
        #return self.write('Please login before post!')

        title = self.request.get("title")
        text = self.request.get("text")
        
        new_topic = Topic.create(title=title, content=text, user=user)

        return self.redirect_to('topic-details', topic_id=new_topic.key.id())

class TopicDetails(BaseHandler):

    def get(self, topic_id):

        params = {}
        user = users.get_current_user()
        topic = Topic.get_by_id(int(topic_id))
        comments = Comment.query(Comment.topic_id == topic.key.id(),
                                 Comment.deleted == False).order(Comment.created).fetch()
        if user:
            if user.email() not in topic.subscribers:
                params['subscriber'] = True


        params['topic'] = topic
        params['comments'] = comments

        return self.render_template_with_csrf('topic_details.html', params=params)

    @validate_csrf
    def post(self, topic_id):
        user = users.get_current_user()

        topic = Topic.get_by_id(int(topic_id))

        subscribe_button = self.request.get('subscribe-button')

        if subscribe_button == 'subscribe':
            topic.subscribers.append(user.email())
        else:
            topic.subscribers.remove(user.email())

        topic.put()

        self.redirect_to("topic-details", topic_id=topic_id)

class TopicDelete(BaseHandler):
    @validate_csrf
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))

        user = users.get_current_user()

        if topic.author_email == user.email() or users.is_current_user_admin():
            topic.deleted = True
            topic.put()

        return self.redirect_to('main-page')
