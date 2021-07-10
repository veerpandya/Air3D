import os
from unittest import TestCase

from datetime import date
 
from air3d_app import app, db, bcrypt
from air3d_app.models import User

"""
Run these tests with the command:
python3 -m unittest air3d_app.auth.tests
"""

#################################################
# Setup
#################################################


def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        """
        Test that a new user's credentials are added to 
        the database after signing up for an account.
        """
        # Make a POST request to /signup, sending a username & password
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        self.app.post('/signup', data=post_data)

        # Check that the user now exists in the database
        user = User.query.filter_by(username='me1').one()
        password_check = bcrypt.check_password_hash(user.password, 'password')

        self.assertEqual(user.username, 'me1')
        self.assertTrue(password_check)


    def test_signup_existing_user(self):
        """
        Test that a new user cannot sign up with a username that already 
        exists for another user in the database.
        """
        # Create a user
        create_user()
        # Make a POST request to /signup, sending the same username & password
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        # Convert reloaded page with error message into text
        signup_page = self.app.post('/signup', data=post_data, follow_redirects=True)
        page_text = signup_page.get_data(as_text=True)

        # Check that the form is displayed again with an error message
        self.assertIn('That username is taken. Please choose a different one.', page_text)

    def test_login_correct_password(self):
        """
        Test that a user can successfully login by checking if the login button
        is not present after the user signs in correctly.
        """
        # Create a user
        create_user()
        # Make a POST request to /login, sending the created username & password
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        # Convert new page into text
        login_page = self.app.post('/login', data=post_data, follow_redirects=True)
        login_page_text = login_page.get_data(as_text=True)

        # Check that the "login" button is not displayed on the homepage
        self.assertNotIn('Log In', login_page_text)

    def test_login_nonexistent_user(self):
        """
        Test that a user cannot login with a username that 
        does not exist in the database.
        """
        # Make a POST request to /login, sending a username & password
        post_data = {
            'username': 'nonexistent_user',
            'password': 'password'
        }
        # Convert reloaded page with error message into text
        login_page = self.app.post('/login', data=post_data, follow_redirects=True)
        login_page_text = login_page.get_data(as_text=True)

        # Check that the login form is displayed again, with an appropriate
        #   error message
        self.assertIn('No user with that username. Please try again.', login_page_text)
        

    def test_login_incorrect_password(self):
        """
        Test that a new user's credentials are added to 
        the database after signing up for an account.
        """
        # Create a user
        create_user()
        # Make a POST request to /login, sending the created username &
        #   an incorrect password
        post_data = {
            'username': 'me1',
            'password': 'wrong_password'
        }
        # Convert reloaded page with error message into text
        login_page = self.app.post('/login', data=post_data, follow_redirects=True)
        login_page_text = login_page.get_data(as_text=True)

        # Check that the login form is displayed again, with an appropriate
        #   error message
        self.assertIn("Password doesn&#39;t match. Please try again.", login_page_text)

    def test_logout(self):
        """Tests that a user logs out by checking the return 
        homepage for the login button."""
        # Create a user
        create_user()
        # Log the user in (make a POST request to /login)
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        self.app.post('/login', data=post_data, follow_redirects=True)

        # Make a GET request to /logout
        logged_out = self.app.get('/logout', follow_redirects=True)
        homepage_text = logged_out.get_data(as_text=True)

        # Check that the "login" button appears on the homepage
        self.assertIn('Sign in', homepage_text)
