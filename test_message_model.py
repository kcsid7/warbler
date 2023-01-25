import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class MessageModelTest(TestCase):
    
    def setUp(self):
    
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

        new_user = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        new_user.id = 98765
        db.session.commit()
        self.userId = new_user.id
        self.user = User.query.get(new_user.id)

    
    def test_message_model(self):

        new_message = Message(
            text="New Message",
            user_id=self.userId
        )
        db.session.add(new_message)
        db.session.commit()

        self.assertEqual(len(self.user.messages), 1)
        self.assertEqual(self.user.messages[0].text, "New Message")


    