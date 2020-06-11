""" this script manages the views """
# global
import random, string

#django
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

#from app import
from .form import UserForm, MailForm
from .models import Profile
from .utils import MailAgent, notify_db_fv, get_user_and_profile, add_new_user


mail_agent = MailAgent()

class RegisterView(View):
    """ This class deals with registration
        get > loads a registration page
        post > analyses datas to try to create a new user and profile
    """

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
            success, message = add_new_user(name, password)
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

    def get(self, request, my_option = 0, code = ""):
        """ manages the get request for myAccount page """
        if request.user.is_authenticated:
            user, profile_found = get_user_and_profile(request)
            profile_found.wait_confirmation = True
            try:
                user_mail = user.email

            except:
                user_mail = None
            if my_option == 1: #comparison code
                profile_found.wait_confirmation = False
                if profile_found.code == code:
                    print("sit code bon")
                    profile_found.mail_confirmed = True
                else:
                    print("sit code mauvais")
                    profile_found.mail_confirmed = False

                
            elif my_option == 2: #new mail
                print("sit change mail")
                profile_found.wait_confirmation = True
                user_mail = None
            else:
                print("sit check mail")
            profile_found.save()
            mail_form = MailForm()
            print({
                    'wait_confirmation' : profile_found.wait_confirmation,
                    'mail_confirmed' : profile_found.mail_confirmed,
                    'user_mail' : user_mail,
                })
            context = {
                'mail_form' : mail_form,
                'wait_confirmation' : profile_found.wait_confirmation,
                'mail_confirmed' : profile_found.mail_confirmed,
                'user_mail' : user_mail,
            }
            return render(request, "user/myAccount.html", context)
        return redirect('user:connection')

    def post(self, request, my_option = 0, code = ""):
        """ manages post request for mail form concerning the myAccount page """
        mail_form = MailForm(request.POST)
        if mail_form.is_valid():
            code = "".join([random.choice(string.digits) for _ in range(24)])
            print(f'le code est {code}')
            mail = mail_form.cleaned_data['mail'] #gets the mail
            mail_agent.send_confirm_mail(mail, code)
            # notify base that mail has been sent
            user_found, profile_found = get_user_and_profile(request)
            user_found.email = mail
            profile_found.mail_confirmed = False
            profile_found.wait_confirmation = True
            user_found.save()
            mail_agent.notify_db_mav(user_found, profile_found, code, mail)
            context = {
                'mail_form' : mail_form,
                'wait_confirmation' : profile_found.wait_confirmation,
                'mail_confirmed' : profile_found.mail_confirmed,
                'user_mail' : user_found.email,
            }
            return render(request, "user/myAccount.html", context)
        return HttpResponse("Le formulaire n'est pas valide")

class FavoriteView(View):
    """ manages the favorite page"""

    def get(self, request, prod_name=None):
        """ manage the get request for fav page"""
        if request.user.is_authenticated:
            profile_found = get_user_and_profile(request)[1]
            if prod_name is not None:
                notify_db_fv(profile_found, prod_name)
            fav_list = [fav for fav in profile_found.favlist.all()]
            print(fav_list)
            context = {"fav_list" : fav_list}
            return render(request, 'user/favorite.html', context)
        return redirect('user:connection')

class LogoutUser(View):
    """ manages the sign out function"""
    def get(self, request):
        """ manages the get request for the logout page"""
        logout(request)
        return redirect('research:index')
        