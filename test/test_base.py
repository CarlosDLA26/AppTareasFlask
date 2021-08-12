from main import app
from flask_testing import TestCase
from flask import current_app, url_for

class Main(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_app_exist(self):
        self.assertIsNotNone(current_app)
    
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_index_redirect(self):
        response = self.client.get(url_for('index'))
        print("Response:",response)
        self.assertRedirects(response, url_for('hello_world'))

    def test_auth_login_template(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')
    
    def test_auth_login(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake-password'
        }
        response = self.client.post(url_for('auth.login'), data=fake_form)

        self.assert200(response)
        