from unittest import mock, skip

#from django
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.test import TestCase
from django.urls import reverse

#from app import
from user.form import UserForm, MailForm
from user.models import Profile

#from other app import
from products.models import Product, Category

import user.views as v
print("test_user\n", "_ "*20)


#-- unit test --

class UnitTest(TestCase):
    def setUp(self):
        self.user = User(username="test")
        self.profile = Profile(user=self.user)
        self.user.set_password("test")
        self.user.pk = 1
        self.user.save()
        self.profile.save()
        self.logged_in = self.client.login(username="test", password="test")
        self.category = Category(name="jus de fruits")
        self.category.save()
        self.product1 = Product(
            name="Pur jus d'orange sans pulpe", 
            image_url="https://static.openfoodfacts.org/images/products/350/211/000/9449/front_fr.80.400.jpg",
            url="https://world.openfoodfacts.org/product/3502110009449/pur-jus-d-orange-sans-pulpe-tropicana", 
            nutriscore=3, packaging="carton")
        self.product1.save()
        self.rv = v.RegisterView()
        self.mav = v.MyAccountView()
        self.fav = v.FavoriteView()
    
    def test_get_user_and_profile(self):
        """ tests wethers function returns user and profile """
        #create a mock request
        my_mock = mock.Mock()
        my_mock.user = self.user
        u, p = v.get_user_and_profile(my_mock)
        self.assertTrue(u, self.user)
        self.assertTrue(p, self.profile)
        my_mock = None
    
    def test_add_new_user_False(self):
        """ checks wether function returns False when user ever exists"""
        new_user = self.rv.add_new_user("test", "test")
        self.assertFalse(new_user[0]) #because it ever exists
       
    def test_add_new_user_True(self):   
        """ checks whether function  returns True when user does not ever exists"""
        new_user2 = self.rv.add_new_user("test2", "test")
        self.assertTrue(new_user2[0])
    
    # def test_mav_notify_db(self):
    #     """ tests whether function notifies the db that a code in a confirm mail has been send """
    #     #params user, profile, code, mail
    #     self.mav.notify_db(self.user, self.profile, code=123, mail="mail")
    #     self.assertEqual(self.profile.code, 123)
    #     self.assertEqual(self.user.email, "mail")
    #     self.assertTrue(self.profile.mail_confirm_sent)
    
    def test_fav_notify_db(self):
        """ tests wether function adds a given prod to the profile fav list"""
        before = self.profile.favlist.all()
        self.fav.notify_db(self.profile, self.product1.name)
        after = self.profile.favlist.all()
        self.assertTrue(len(before), len(after)-1)

    def test_logout(self):
        """ Tests whether the function logouts the user """
        response = self.client.get(reverse("user:logout"), follow=True)
        self.assertTrue(self.user.is_authenticated)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse("research:index"))

#-- integration test -- 

class AuthenticationViewTests(TestCase):

    def setUp(self): 
        patcher = mock.patch("user.views.UserForm")
        self.addCleanup(patcher.stop) #called after teardown
        mock_form_class = patcher.start()
        self.mock_form = mock_form_class.return_value

        #creates user
        self.user = User.objects.create(username='new_user')
        self.user.set_password('new_psw')
        self.user.save()
        #connectes user
        self.logged_in = self.client.login(username='new_user', password='new_psw')

    #registration page
  
    def test_regis_get_access_page_when_user_connected(self):
        """
        Tests whether function redirects authenticated user if they want to access register page 
        """
        
        response = self.client.get(reverse("user:register"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('research:index'))
  
    def test_regis_get_access_page_(self):
        """ Test redirection when a connected user try to get the register page"""
        #creates user
        self.client.logout()
        #loads page
        response = self.client.get(reverse("user:register"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.build_absolute_uri(), 'http://testserver/user/register')

  
    def test_regis_post_form_invalid(self):
        """ Tests reaction in case of invalid form """
        self.mock_form.is_valid.return_value = False 
        #mock qui imite le comportement form.is_valid = False
        response = self.client.post(reverse("user:register"), follow=True)
        self.assertContains(response, "Problème dans le formulaire !")

  
    def test_regis_post_add_new_user_ok(self):
        self.mock_form.is_valid.return_value = True
        self.mock_form.cleaned_data = {
            "username": "123",
            "password": "new_password"
        }
        self.client.logout()
        response = self.client.post(reverse("user:register"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("user:connection"))

    
    def test_regis_post_add_new_user_integrity_error(self):
        self.client.logout()
        self.mock_form.is_valid.return_value = True
        self.mock_form.cleaned_data = {
            "username": "new_user",
            "password": "new_password"
        }
        #response create a new user but this ever exists
        response = self.client.post(reverse("user:register"), follow=True)
        self.assertRedirects(response, reverse("user:register"))

    #connection page
  
    def test_conn_get_access_page_when_user_not_connected(self):
        """
        user can access page
        """
        self.client.logout()
        response = self.client.get(reverse("user:connection"))
        self.assertEqual(response.status_code, 200)

  
    def test_conn_get_access_page_when_user_connected(self):
        """ Test redirection when a connected user try to get the register page"""
        response = self.client.get(reverse("user:connection"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("research:index"))

  
    def test_conn_post_us_form_invalid(self):
        self.mock_form.is_valid.return_value = False 
        response = self.client.post(reverse("user:connection"), follow=True)
        self.assertContains(response, 'Problème dans le formulaire !')
        self.assertEqual(response.status_code, 200)
    
    def test_conn_post_us_form_valid(self):
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
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("research:index"))

    
    def test_conn_post_bad_credentials(self):
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
        self.client.logout()
        response = self.client.post(reverse("user:connection"), follow=True)
        messages = [message for message in response.context["messages"]]
        self.assertRedirects(response, reverse("user:connection"))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,'Pseudo ou mot de passe incorrect')    

class MyAccountViewTests(TestCase):

    def setUp(self): 
        # patcher = mock.patch("user.views.MyAccountView")
        # self.addCleanup(patcher.stop) #called after teardown
        # mock_acc_view_class = patcher.start()
        # self.mock_acc_view = mock_acc_view_class.return_value

        patcher2 = mock.patch("user.views.MailForm")
        self.addCleanup(patcher2.stop) #called after teardown
        mock_form_class = patcher2.start()
        self.mock_form = mock_form_class.return_value  
        self.mav = v.MyAccountView()

        self.user = User(username="test")
        self.profile = Profile(user=self.user)
        self.user.set_password("test")
        self.user.pk = 1
        self.user.save()
        self.profile.save()
        self.logged_in = self.client.login(username="test", password="test")
        
        self.my_mock = mock.Mock()
        self.my_mock.user = self.user
   
    def test_myacc_get_access_page_when_user_not_authenticated(self):
        """ user connected can not access myAccount page"""
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
    
    # def test_myacc_get_access_page_option1_wrong_code(self):
    #     """ Tests whether the function will display an error message if code is not correct 111 != 123"""
        
    #     self.user.email, self.profile.mail_confirm_sent = "test@mail.fr", True
    #     self.profile.code = "123"
    #     self.user.save()
    #     self.profile.save()
    #     response = self.client.get(reverse("user:myAccount", args=[1, "111"]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(
    #         response.wsgi_request.build_absolute_uri(), "http://testserver/user/myAccount/1/111")
    #     self.assertContains(response, "Il semblerait que je n'ai pas encore reçu ta confirmation")
    
    # def test_myacc_get_access_page_option1_good_code(self): 
    #     """ Tests whether the function will display confirmation message if code is correct 123 = 123"""
    #     self.user.email, self.profile.mail_confirm_sent = "test@mail.fr", True
    #     self.profile.code = "123"
    #     self.user.save()
    #     self.profile.save()
    #     response = self.client.get(reverse("user:myAccount", args=[1, "123"]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(
    #         response.wsgi_request.build_absolute_uri(), "http://testserver/user/myAccount/1/123")
    #     self.assertContains(response, "Tu m'as communiqué ce mail : test@mail.fr")

    
    # def test_myacc_get_access_page_option2(self):
    #     """ user can access myAcount with url : ".../user/myAccount/2
    #         that means user has given a first mail and can change it because a new email form appears
    #     """ 
    #     self.user.email, self.profile.mail_confirm_sent = "test@mail.fr", True
    #     self.user.save()
    #     self.profile.save()
    #     response = self.client.get(reverse("user:myAccount", args=[2]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Il semblerait que je n'ai pas ton mail ...")

    
    def test_myacc_post_form_is_not_valid(self):
        """ Tests whether the function displays an error msg if form is not valid """
        self.mock_form.is_valid.return_value = False
        response = self.client.post(reverse("user:myAccount"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Le formulaire n'est pas valide")
    
    
    def test_myacc_post_form_is_valid(self):
        """ Tests whether the function displays an"""
        self.mock_form.is_valid.return_value = True
        mail = "a new mail"
        self.mock_form.cleaned_data = {"mail": mail}  #le pb ne vient pas de là 
        response = self.client.post(reverse("user:myAccount"), follow=True)
        self.assertRedirects(response, reverse("user:myAccount"))
        # self.assertContains(response, f"Mail de confirmation envoyé à cette adresse {mail}, j'attends ta réponse")
        self.assertEqual(response.wsgi_request.user.email, "a new mail")

class FavoriteTests(TestCase):

    def setUp(self): 
        self.user = User(username="test")
        self.profile = Profile(user=self.user)
        self.user.set_password("test")
        self.user.pk = 1
        self.user.save()
        self.profile.save()
        self.logged_in = self.client.login(username="test", password="test")
        
        self.category = Category(name="jus de fruits")
        self.category.save()
        self.product1 = Product(
            name="Pur jus d'orange sans pulpe", 
            image_url="https://static.openfoodfacts.org/images/products/350/211/000/9449/front_fr.80.400.jpg",
            url="https://world.openfoodfacts.org/product/3502110009449/pur-jus-d-orange-sans-pulpe-tropicana", 
            nutriscore=3, packaging="carton")
        self.product2 = Product(
            name="orange bio", 
            image_url="fake url",
            url="fake url", 
            nutriscore=5, packaging="bouteille plastique")
        self.product1.save()
        self.product2.save()
        self.product1.category.add(self.category)
        self.product2.category.add(self.category)
        self.product1.save()
        self.product2.save()
    
    def test_favorite_get_access_no_param_no_connected(self):
        self.client.logout()
        response = self.client.get(reverse("user:favorite"))
        self.assertRedirects(response, reverse("user:connection"))

    def test_favorite_get_access_no_param(self):
        """ test wehter user can acces user/favorite """
        response = self.client.get(reverse("user:favorite"))
        self.assertTrue(response.status_code, 200)

    def test_favorite_get_access_with_param(self):
        """ test wehter user can acces user/favorite/orange bio"""
        before = len(self.profile.favlist.all())

        response = self.client.get("/user/favorite/orange bio")
        after = len(self.profile.favlist.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(before, after-1)

        self.assertTrue(response.status_code, 200)

    def test_favorite_add_db(self):
        """ test wether a product can be add user favorite page"""
        before = len(self.profile.favlist.all())
        response = self.client.get("user/favorite/orange bio")
        after = len(self.profile.favlist.all())
        self.assertTrue(before + 1, after)



        