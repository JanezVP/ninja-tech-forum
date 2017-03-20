from handlers.base import BaseHandler
from models.subscribe import Subscriber
from google.appengine.ext import ndb
from utils.decorators import validate_csrf

class SubscriberHandler(BaseHandler):
    def get(self):
        return self.render_template_with_csrf("subscribe.html")

    @validate_csrf

    def post(self):

        # get subscribers mail
        subscribe_email = self.request.get("subscription_email")

        # put email in Datastore
        Subscriber.create(subscribe_email=subscribe_email)

        return self.redirect_to("main-page")