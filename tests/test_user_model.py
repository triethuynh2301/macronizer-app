from unittest import TestCase
from config import TestConfig
from macronizer_cores import create_app 
from macronizer_cores.models import db, User


class UserModelTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
      """Make demo data."""

      # set up test configuration
      self.app = create_app(TestConfig)
      self.app_context = self.app.app_context()
      self.app_context.push()

      # create test db
      db.drop_all()
      db.create_all()

      # mock data
      test_user = User(
        name="John Doe",
        email="john@example.com",
        username="johndoelearntocode",
        password="password"
      )
      (username, password) = User.register(test_user.username, test_user.password)
      test_user.password = password
      db.session.add(test_user)
      db.session.commit()

      self.test_user = test_user


    def tearDown(self):
      """Clean up fouled transactions."""

      db.session.rollback()
      self.app_context.pop()


    def test_authenticate_valid_user(self) -> None:
      '''
      Test that User.authenticate() successfully authenticate valid user 
      '''

      # act
      expected_user = User.authenticate("johndoelearntocode", "password")

      # assert
      self.assertEqual(expected_user, self.test_user)


    def test_authenticate_invalid_username(self) -> None:
      '''
      Test that User.authenticate() returns false on invalid username
      '''

      # act
      expected_user = User.authenticate("anotherjohndoe", "password")

      # assert
      self.assertFalse(expected_user)


    def test_authenticate_invalid_password(self) -> None:
      '''
      Test that User.authenticate() returns false on invalid password
      '''

      # act
      expected_user = User.authenticate("johndoelearntocode", "wrongpassword")

      # assert
      self.assertFalse(expected_user)
