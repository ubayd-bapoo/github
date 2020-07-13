from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

class HomePageTests(TestCase):
    # --------------------------------------------------------------------------
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        self.user = User.objects.get(username=self.credentials['username'])

    # --------------------------------------------------------------------------
    def test_login_page_status_code(self):
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)

    # --------------------------------------------------------------------------
    def test_view_uses_correct_template(self):
        response = self.client.get('/accounts/login/')
        self.assertTemplateUsed(response, 'account/login.html')

    # --------------------------------------------------------------------------
    def test_login_page_contains_correct_html(self):
        response = self.client.get('/')
        self.assertContains(response, '<h1 class="h4 text-gray-900 mb-4">Welcome and Login with Github!</h1>')

    # --------------------------------------------------------------------------
    def test_login_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/accounts/login/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

    # --------------------------------------------------------------------------
    def test_redirect_when_authenticated(self):
        self.client.force_login(self.user)
        resp = self.client.get('/')
        self.assertContains(resp, 'Title: <input type="text" class="form-control form-control-user" id="title" name="title" placeholder="Enter Title">')
