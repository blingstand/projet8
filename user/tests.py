from django.test import TestCase
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.urls import reverse

from django.shortcuts import render, redirect

from unittest import mock, skip
from .form import UserForm, MoreUserDataForm
from .models import Profile

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
        

class myAccountViewTests(TestCase):

    def setUp(self): 
        patcher = mock.patch("user.views.myAccountView")
        self.addCleanup(patcher.stop) #called after teardown
        mock_acc_view_class = patcher.start()
        self.mock_acc_view = mock_acc_view_class.return_value

        patcher2 = mock.patch("user.views.MoreUserDataForm")
        self.addCleanup(patcher2.stop) #called after teardown
        mock_form_class = patcher2.start()
        self.mock_form = mock_form_class.return_value


        self.user = User(username="test")
        self.profile = Profile(user=self.user)
        self.user.set_password("test")
        self.user.pk = 1
        self.user.save()
        self.profile.save()
        self.logged_in = self.client.login(username="test", password="test")
        

    def tearDown(self):
        self.client.logout()
    
    def test_myacc_can_not_get_access_page(self):
        """ user connected can access myAccount page"""
        self.client.logout()
        response = self.client.get(reverse('user:myAccount'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("user:connection"))
    
    def test_myacc_get_access_page(self):
        """ user connected can access myAccount page"""
        response = self.client.get("/user/myAccount", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.build_absolute_uri(), \
            "http://testserver/user/myAccount")
        
    def test_myacc_get_access_page_option1_and_mail(self):
        """ user can access myAcount with url : ".../user/myAccount/1/test@mail.fr" """
        self.user.email, self.profile.mail_confirm_sent = "test@mail.fr", True
        self.user.save()
        self.profile.save()
        self.mock_acc_view.get_user_and_profile = self.user, self.profile
        #send a .../myAccount/1/test@mail.fr
        response = self.client.get(reverse("user:myAccount", args=[1, str("test@mail.fr")]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tu m'as communiqué ce mail : test@mail.fr")
        

    
    def test_myacc_get_access_page_option2(self):
        """ user can access myAcount with url : ".../user/myAccount/2
            that means user has given a first mail and can change it because a new email form appears
        """ 
        self.user.email, self.profile.mail_confirm_sent = "test@mail.fr", True
        self.user.save()
        self.profile.save()
        response = self.client.get(reverse("user:myAccount", args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Il semblerait que je n'ai pas ton mail ...")

    
    def test_myacc_post_form_is_not_valid(self):
        """
            user gets an error page if form is not valid 
        """
        self.mock_form.is_valid.return_value = False
        response = self.client.post(reverse("user:myAccount"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Le formulaire n'est pas valide")

    def test_myacc_post_form_is_valid(self):
        """ 
            user can give a mail adress and this will actualise :
            1/ user.email,
            2/ profile.mail_confirm_sent 
        """
        self.mock_acc_view.get_user_and_profile = self.user, self.profile
        self.mock_form.is_valid.return_value = True
        self.mock_form.cleaned_data = {"mail": "a new mail"}  #le pb ne vient pas de là 
        response = self.client.post(reverse("user:myAccount"))
        self.assertEqual(response.status_code, 200)
        session_profile = Profile.objects.filter(user = self.user)[0]
        self.assertTrue(response.wsgi_request.user.email == "a new mail")
        self.assertTrue(session_profile.mail_confirm_sent)

        

        


     