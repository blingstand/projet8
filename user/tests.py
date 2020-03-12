from django.test import TestCase, RequestFactory
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.urls import reverse

from django.shortcuts import render, redirect

from unittest import mock, skip
from .form import UserForm

class IndexViewTests(TestCase):
    def test_access_page(self):
        """
        user can access page
        """
        response = self.client.get(reverse('user:index'))
        self.assertEqual(response.status_code, 200)

class AuthenticationViewTests(TestCase):

    def setUp(self): 
        patcher = mock.patch("user.views.UserForm")
        self.addCleanup(patcher.stop) #called after teardown
        mock_form_class = patcher.start()
        self.mock_form = mock_form_class.return_value

        self.factory = RequestFactory()

    #registration page
    def test_regis_get_access_page(self):
        """
        user can access page
        """
        response = self.client.get(reverse("user:register"))

        self.assertEqual(response.status_code, 200)

    def test_regis_get_access_page_when_user_connected(self):
        """ Test redirection when a connected user try to get the register page"""
        #creates user
        user = User.objects.create(username='new_user')
        user.set_password('new_psw')
        user.save()
        #connectes user
        logged_in = self.client.login(username='new_user', password='new_psw')
        #loads page
        response = self.client.get(reverse("user:register"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("user:index"))
        self.assertTrue(logged_in)
        #cleans datas
        self.client.logout()
        user.delete()

    def test_regis_post_form_invalid(self):
        """ Tests reaction in case of invalid form """
        self.mock_form.is_valid.return_value = False 
        #mock qui imite le comportement form.is_valid = False
        response = self.client.post(reverse("user:register"), follow=True)
        messages = [message for message in response.context["messages"]]
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, 'Problème dans le formulaire !')

    def test_regis_post_add_new_user_ok(self):
        self.mock_form.is_valid.return_value = True
        self.mock_form.cleaned_data = {
            "username": "new_user",
            "password": "new_password"
        }
        response = self.client.post(reverse("user:register"), follow=True)
        users = User.objects.filter(username='new_user')[0]
        self.assertRedirects(response, reverse("user:connection"))
        self.assertEqual('new_user', users.username)

    def test_regis_post_add_new_user_integrity_error(self):
        self.mock_form.is_valid.return_value = True
        self.mock_form.cleaned_data = {
            "username": "new_user",
            "password": "new_password"
        }
        #response create a first new user
        response = self.client.post(reverse("user:register"), follow=True)
        #response2 tries to create another with same username, fails and is redirected
        response2 = self.client.post(reverse("user:register"), follow=True)
        
        self.assertRedirects(response, reverse("user:connection"))
        self.assertRedirects(response2, reverse("user:register"))

    #connection page
    def test_conn_get_access_page(self):
        """
        user can access page
        """
        response = self.client.get(reverse("user:connection"))

        self.assertEqual(response.status_code, 200)

    def test_conn_get_access_page_when_user_connected(self):
        """ Test redirection when a connected user try to get the register page"""
        #creates user
        user = User.objects.create(username='new_user')
        user.set_password('new_psw')
        user.save()
        #connectes user
        logged_in = self.client.login(username='new_user', password='new_psw')
        #loads page
        response = self.client.get(reverse("user:connection"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("user:index"))
        self.assertTrue(logged_in)
        #cleans datas
        self.client.logout()
        user.delete()

    def test_conn_post_form_invalid(self):
        self.mock_form.is_valid.return_value = False 
        response = self.client.post(reverse("user:connection"), follow=True)
        messages = [message for message in response.context["messages"]]
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, 'Problème dans le formulaire !')

    def test_conn_post_good_credentials(self):
        #user account
        user = User.objects.create(username='new_user')
        user.set_password('new_psw')
        user.save()
        #mock for user connection
        self.mock_form.is_valid.return_value = True
        self.mock_form.cleaned_data = {
            "username": "new_user",
            "password": "new_psw"
        }
        #tests connection is possible
        self.assertTrue(self.client.login(
            username="new_user",
            password="new_psw"))
        self.client.logout()
        response = self.client.post(reverse("user:connection"), follow=True)
        self.assertRedirects(response, reverse("user:index"))

    def test_conn_post_bad_credentials(self):
        #user account
        user = User.objects.create(username='new_user')
        user.set_password('new_psw')
        user.save()
        #mock for user connection
        self.mock_form.is_valid.return_value = True
        self.mock_form.cleaned_data = {
            "username": "bad username",
            "password": "bad password"
        }
        #tests connection is not possible
        self.assertFalse(self.client.login(
            username="bad username",
            password="bad new_password"))
        response = self.client.post(reverse("user:connection"), follow=True)
        messages = [message for message in response.context["messages"]]
        self.assertRedirects(response, reverse("user:connection"))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,'Pseudo ou mot de passe incorrect')
        

class ConnectionViewTests(TestCase):
    def test_access_page(self):
        """
        user can access page
        """
        response = self.client.get(reverse('user:connection'))
        self.assertEqual(response.status_code, 200)
