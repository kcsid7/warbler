"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()
 

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        user1 = User.signup("user1", "user1@gmail.com", "user1pwd", None)
        user2 = User.signup("user2", "user2@gmail.com", "user2pwd", None)
        user1.id = 1
        user2.id = 2
        db.session.commit()

        self.u1 = User.query.get(1)
        self.u2 = User.query.get(2)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_signup(self):
        test_user = User.signup("testUser123", "test@gmail.com", "testPassword", None)
        uid = 12345
        test_user.id = uid
        db.session.commit()

        test_user = User.query.get(uid)
        self.assertEqual(test_user.username, "testUser123")
        self.assertEqual(test_user.email, "test@gmail.com")
        self.assertNotEqual(test_user.password, "testPassword")