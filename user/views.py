""" this script manages the views """
# global
import random, string

#django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

#from other app import

from products.models import Product

#from app import
from .form import UserForm, MailForm
from .models import Profile


#usefull function for myAccount and Favorite class
def get_user_and_profile(request):
    """ return the session user and the profile he belongs """
    user_found = request.user
    ufpk = user_found.pk #user_found_primary_key = ufpk
    profile_found = Profile.objects.filter(user=ufpk)[0]
    return user_found, profile_found


class RegisterView(View):
    """ This class deals with registration
        get > loads a registration page
        post > analyses datas to try to create a new user and profile
    """

    def add_new_user(self, name, password):
        """
        Tries to add a new user in base and return Boolean and message
            True = Success / False = Fail
        """
        try:
            new_user = User(username=name)
            new_user.set_password(password)
            new_user.save()

            new_profile = Profile(user=new_user)
            new_profile.save()
            return True, f"Félicitation vous venez de créer : {name} !"
        except IntegrityError:
            return False, "Cet utilisateur existe déjà !"

    def get(self, request):
        """ manages the get request for the register page """
        if request.user.is_authenticated:
            return redirect('research:index') #if auth user comes to register page
        us_form = UserForm()
        context = {'us_form': us_form}
        return render(request, 'user/register.html', context)

    def post(self, request):
        """
        manages the post request for the register page :
            get datas in order to try to create a new user

        """
        us_form = UserForm(request.POST)
        if us_form.is_valid():
            name, password = us_form.cleaned_data['username'], us_form.cleaned_data['password']
            success, message = self.add_new_user(name, password)
            messages.info(request, message)
            if success:
                return redirect('user:connection')
            return redirect('user:register')
        return HttpResponse("Problème dans le formulaire !")

class ConnectionView(View):
    """ This class deals with login
        get > loads a connection page
        post > analyses datas in order to try to authenticate
    """
    def get(self, request):
        """ manage the get request concerning the connection page """
        if request.user.is_authenticated:
            return redirect('research:index')
        us_form = UserForm()
        context = {'us_form' : us_form}
        return render(request, 'user/connection.html', context)

    def post(self, request):
        """
        manages the post request for connection page,  use given datas
        in order to try to authenticate
        """
        us_form = UserForm(request.POST)
        if us_form.is_valid():
            username = us_form.cleaned_data['username']
            password = us_form.cleaned_data['password']
            new_user = authenticate(username=username, password=password)

            if new_user is not None:
                login(request, new_user)
                return redirect('research:index')
            messages.info(request, 'Pseudo ou mot de passe incorrect')
            return redirect('user:connection')
        return HttpResponse("Problème dans le formulaire !")

class MyAccountView(View):
    """ this class handles with myAccount view to display the myAccount.html

        get() can load the same page but this one can change according to the context
        context will depend on parameters in the request
    """
    def _send_confirm_mail(self, mail, code):
        """ sends a code by mail to confirm mail adress before adding in base """
        subject = "Confirmation de votre mail "
        message = f"Cliquez sur ce lien http://127.0.0.1:8000/user/myAccount/1/{code}"\
        " pour confirmer votre mail"
        from_email = settings.EMAIL_HOST_USER
        to_list = [mail]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


    def notify_db(self, user, profile, code, mail):
        """ notifies the db that a code in a confirm mail has been send """
        profile.mail_confirm_sent = True
        profile.code = code
        profile.save()
        user.email = mail
        user.save()

    def get(self, request, my_option = 0, code = ""):
        """ manages the get request for myAccount page """
        if request.user.is_authenticated:
            user, profile_found = get_user_and_profile(request)
            try:
                user_mail = user.email

            except:
                user_mail = None
            if my_option == 1: #comparison code
                if profile_found.code == code:
                    profile_found.mail_confirmed = True
                    profile_found.save()
                else:
                    print({
                        'mail_confirm_sent' : profile_found.mail_confirm_sent,
                        'mail_confirmed' : profile_found.mail_confirmed,
                        'user_mail' : user_mail,
                    })
                    messages.error(request, "la confirmation de l'adresse mail a échoué !")
            elif my_option == 2: #new mail
                print("changeons le mail")
                profile_found.mail_confirm_sent = False
                user_mail = None
                profile_found.save()
            mail_form = MailForm()
            context = {
                'mail_form' : mail_form,
                'mail_confirm_sent' : profile_found.mail_confirm_sent,
                'mail_confirmed' : profile_found.mail_confirmed,
                'user_mail' : user_mail,
            }
            return render(request, "user/myAccount.html", context)
        return redirect('user:connection')

    def post(self, request, my_option = 0, code = ""):
        """ manages post request for mail form concerning the myAccount page """
        mail_form = MailForm(request.POST)
        if mail_form.is_valid():
            mail = mail_form.cleaned_data['mail'] #gets the mail
            code = "".join([random.choice(string.digits) for _ in range(24)])
            self._send_confirm_mail(mail, code)
            # notify base that mail has been sent
            user_found, profile_found = get_user_and_profile(request)
            user_found.email = mail
            user_found.save()
            self.notify_db(user_found, profile_found, code, mail)
            return redirect("user:myAccount")
        return HttpResponse("Le formulaire n'est pas valide")

class FavoriteView(View):
    """ manages the favorite page"""
    def notify_db(self, profile, prod_name):
        """ adds a given prod to the profile fav list"""
        product = Product.objects.get(name=prod_name) #it always exists, so don't need : try/except
        profile.favlist.add(product)
        profile.save()

    def get(self, request, prod_name=None):
        """ manage the get request for fav page"""
        if request.user.is_authenticated:
            profile_found = get_user_and_profile(request)[1]
            if prod_name is not None:
                self.notify_db(profile_found, prod_name)
            fav_list = [fav for fav in profile_found.favlist.all()]
            context = {"fav_list" : fav_list}
            return render(request, 'user/favorite.html', context)
        return redirect('user:connection')

class LogoutUser(View):
    """ manages the sign out function"""
    def get(self, request):
        """ manages the get request for the logout page"""
        logout(request)
        return redirect('research:index')
        