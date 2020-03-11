from django.test import TestCase
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.urls import reverse

from unittest import mock
from .form import UserForm

class IndexViewTests(TestCase):
    def test_access_page(self):
        """
        user can access page
        """
        response = self.client.get(reverse('coach:index'))
        self.assertEqual(response.status_code, 200)

class RegisterViewTests(TestCase):

    def test_access_page(self):
        """
        user can access page
        """
        response = self.client.get(reverse('coach:register'))

        self.assertEqual(response.status_code, 200)


    def test_add_new_user_ok(self):

        patcher = mock.patch("coach.views.UserForm")
        self.addCleanup(patcher.stop) #called after teardown
        mock_form_class = patcher.start()
        self.mock_form = mock_form_class.return_value

        users1 = User.objects.all()
        self.mock_form.is_valid.return_value = True
        self.mock_form.cleaned_data = {
            "username": "new_user",
            "password": "new_password"
        }

        response = self.client.post(reverse("coach:register"), follow=True)
        users2 = User.objects.filter(username='new_user')[0]
        self.assertRedirects(response, reverse("connection"))
        self.assertEqual('new_user', users2.username)


class ConnectionViewTests(TestCase):
    def test_access_page(self):
        """
        user can access page
        """
        response = self.client.get(reverse('coach:connection'))
        self.assertEqual(response.status_code, 200)
