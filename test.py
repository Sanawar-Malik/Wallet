import os
os.environ['DATABASE_URL'] = 'sqlite:////tmp/test.db'  # use an in-memory database for tests

import re
import unittest
from flask import app
from app import app, db
from app.models import User


class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = app()
        self.app.config['WTF_CSRF_ENABLED'] = False  # no CSRF during tests
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.populate_db()
        self.client = self.app.test_client()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def populate_db(self):
        user = User(username='malik', email='malik78@gmail.com')
        user.set_password('mnmnmn')
        db.session.add(user)
        db.session.commit()

    def login(self):
        self.client.post('/login', data={
            'username': 'susan',
            'password': 'foo',
        })

    # def get_api_token(self):
    #     response = self.client.post('/api/tokens', auth=('susan', 'foo'))
    #     return response.json['token']

    def test_app(self):
        assert self.app is not None
        assert app == self.app

    def test_home_page_redirect(self):
        response = self.client.get('/', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/login'

    def test_registration_form(self):
        response = self.client.get('/register')
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # make sure all the fields are included
        assert 'name="username"' in html
        assert 'name="email_address"' in html
        assert 'name="password1"' in html
        assert 'name="password2"' in html
        assert 'name="submit"' in html

    def test_register_user(self):
        response = self.client.post('/register', data={
            'username': 'alice',
            'email_address': 'alice@example.com',
            'password1': 'sanawar',
            'password2': 'sanawar',
        }, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/login' # redirected to login

        # login with new user
        response = self.client.post('/login', data={
            'username': 'alice',
            'password': 'sanawar',
        }, follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'Hi, alice!' in html

    def test_register_user_mismatched_passwords(self):
        response = self.client.post('/register', data={
            'username': 'alice',
            'email_address': 'alice@example.com',
            'password1': 'sanawar',
            'password2': 'bar',
        })
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'Field must be equal to password.' in html

    # def test_write_post(self):
    #     self.login()
    #     response = self.client.post('/', data={'post': 'Hello, world!'},
    #                                 follow_redirects=True)
    #     assert response.status_code == 200
    #     html = response.get_data(as_text=True)
    #     assert 'Your post is now live!' in html
    #     assert 'Hello, world!' in html
    #     assert re.search(r'<span class="user_popup">\s*'
    #                      r'<a href="/user/susan">\s*'
    #                      r'susan\s*</a>\s*</span>\s*said', html) is not None

    # def test_api_register_user(self):
    #     response = self.client.post('/api/users', json={
    #         'username': 'bob',
    #         'email': 'bob@example.com',
    #         'password': 'bar'
    #     })
    #     assert response.status_code == 201

    #     # make sure the user is in the database
    #     user = User.query.filter_by(username='bob').first()
    #     assert user is not None
    #     assert user.email == 'bob@example.com'

    # def test_api_get_users(self):
    #     token = self.get_api_token()
    #     response = self.client.get(
    #         '/api/users', headers={'Authorization': f'Bearer {token}'})
    #     assert response.status_code == 200
    #     assert len(response.json['items']) == 1
    #     assert response.json['items'][0]['username'] == 'susan'