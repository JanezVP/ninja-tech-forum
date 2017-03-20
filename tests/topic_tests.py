import os
import unittest
import webapp2
import webtest
import uuid


from google.appengine.ext import testbed
from google.appengine.api import memcache
from handlers.topics import TopicAdd, TopicDetails
from handlers.base import MainHandler
from models.topic import Topic


class TopicTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/topic/add', TopicAdd, name="topic-add"),
                webapp2.Route('/topic/<topic_id:\d+>', TopicDetails, name="topic-details"),
                webapp2.Route('/', MainHandler, name="main-page"),

            ])

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_mail_stub()
        self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'janez.voler@gmail.com'
        os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    def test_topic_add_handler(self):
        # GET
        get = self.testapp.get('/topic/add')  # do a GET request
        self.assertEqual(get.status_int, 200)

        # POST
        csrf_token = str(uuid.uuid4())  # create a CSRF token
        memcache.add(key=csrf_token, value=True, time=600)  # save token to memcache

        title = "Some new topic"
        text = "Just for testing."

        params = {"title": title, "text": text, "csrf_token": csrf_token}

        post = self.testapp.post('/topic/add', params)  # POST request
        self.assertEqual(post.status_int, 302)

        topic = Topic.query().get()  # get the topic
        self.assertTrue(topic.title, title)
        self.assertTrue(topic.content, text)

    def test_topic_detail_handler(self):
        topic = Topic(title="Another topic", content="Some text in the topic", author_email="some.user@example.com")
        topic.put()

        get = self.testapp.get('/topic/{}'.format(topic.key.id()))  # do a GET request
        self.assertEqual(get.status_int, 200)

