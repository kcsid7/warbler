import os
from unittest import TestCase

from models import db, connect_db, Message, User, Likes

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


class UserViewsTest(TestCase):

    def setUp(self):
    
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

        new_user = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        new_user.id = 98765

        self.user1 = User.signup("user1", "user1@gmail.com", "user1pwd", None)
        self.user2 = User.signup("user2", "user2@gmail.com", "user2pwd", None)
        self.user1.id = 11111
        self.user2.id = 22222
        db.session.commit()

        self.userId = new_user.id
        self.user = User.query.get(new_user.id)
    
    def show_user(self):
        with self.client as c:
            resp = c.get(f"/users/{self.userId}")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("@testuser", str(resp.data))

    def search_users(self):
        with self.client as c:
            resp = c.get("/users?q=user")

            self.assertIn("@user1", str(resp.data))
            self.assertIn("@user2", str(resp.data))
            self.assertIn("@testuser", str(resp.data))

    def like_message(self):
        new_message = Message(id=1111, text="Hello World", user_id=self.userId)
        db.session.add(new_message)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.userId

            resp = c.post("/messages/1111/like", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            all_likes = Likes.query.filter(Likes.message_id==1111).all()
            self.assertEqual(len(all_likes), 1)