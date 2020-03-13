from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .form import UserForm, MoreUserDataForm
from .models import Profile



class RegisterView(View):
    """ This class deals with registration
        get > loads a registration page
        post > analyses datas to try to create a new user and profile
    """
    def get(self, request): 
        """ display html page with form in order to register a new user"""
        if request.user.is_authenticated:
            return redirect('user:index') #if auth user comes to register page
        form = UserForm()
        context = {'form':form}
        return render(request, 'user/register.html', context)
    
    def post(self, request):
        """ get the outcome from register's form and try to create a new user and profile"""
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                new_user = User.objects.create_user(username=username, password=password)
                new_user.save()
                new_profile = Profile(user=new_user)
                new_profile.save()
                # big brother is watching you 
                # œœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœ
                subject = "Création d'un nouveau compte"
                message = "Un utilisateur vient de créer un compte, \n" \
                    "pseudo = {} et mot de passe = {}".format(username, password)
                from_email = settings.EMAIL_HOST_USER
                to_list = [settings.EMAIL_HOST_USER]
                send_mail(subject, message, from_email, to_list, fail_silently=True)
                # œœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœ
                messages.success(request, "Félicitation vous venez de créer : {} !".format(username))
                return redirect('user:connection')
            except IntegrityError:
                messages.error(request, "Cet utilisateur existe déjà !")
                return redirect('user:register')
        messages.error(request, "Problème dans le formulaire !")
        return redirect('user:register')
        

class ConnectionView(View):
    """ This class deals with login
        get > loads a connection page
        post > analyses datas in order to try to authenticate
    """
    def get(self, request):
        """ loads a connection page """
        if request.user.is_authenticated:
            return redirect('user:index')
        form = UserForm()
        context = {'form' : form}
        return render(request, 'user/connection.html', context)
    
    def post(self, request):
        """ analyses datas in order to try to authenticate """
        form = UserForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            new_user = authenticate(username=username, password=password)

            if new_user is not None:
                login(request, new_user)
                return redirect('user:index')
            else:
                messages.info(request, 'Pseudo ou mot de passe incorrect')
                return redirect('user:connection')
        messages.error(request, "Problème dans le formulaire !")
        return redirect('user:connection')
                


class myAccountView(View):
    
    def get_user_and_profile(self, user):
        user_found = user
        ufpk = user_found.pk #user_found_primary_key = ufpk
        profile_found = Profile.objects.filter(user=ufpk)[0]
        print(profile_found.mail_confirmed, profile_found.mail_confirm_sent)
        return user, profile_found

    def get(self, request, mail_confirm=0, get_mail=""):
        if request.user.is_authenticated:
            user, profile_found = self.get_user_and_profile(request.user)
            try:
                user_mail = user.email
            except Exception as e:
                HttpResponse(user.username, user.password, user.email)
            user.email = None #to avoid error
            if mail_confirm == 1:
                user.email = get_mail
                user.save()
                profile_found.mail_confirmed = True
                profile_found.save()
            form = MoreUserDataForm()
            context={
                'form' : form, 
                'mail_confirm_sent' : profile_found.mail_confirm_sent,
                'mail_confirmed' : profile_found.mail_confirmed, 
                'user_mail' : user_mail
            }
            return render(request, "user/myAccount.html", context)

    def post(self, request, email_confirm=0):
        if request.user.is_authenticated:
            form = MoreUserDataForm(request.POST)
            if form.is_valid(): 
                mail = form.cleaned_data['mail'] #gets the mail
                #sends a mail to confirm mail adress before adding in base
                subject = "Confirmation de votre mail "
                message = "Clickez sur ce lien http://127.0.0.1:8000/myAccount/1/{} pour confirmer votre mail"\
                .format(mail)
                from_email = settings.EMAIL_HOST_USER
                to_list = [mail]
                # send_mail(subject, message, from_email, to_list, fail_silently=True)
                # notify base that mail has been sent
                user, profile_found = self.get_user_and_profile(request.user)
                profile_found.mail_confirm_sent = True
                profile_found.save()
                user.email = mail
                user.save()
                return HttpResponse(user.email)

            context={
                'form' : form
            }
            return render(request, "user/myAccount.html", context)




def logoutUser(request):
    logout(request)
    return redirect('user:index')



def index(request):
    # message = "Bienvenu sur le site pureBeurre !"

    return render(request, 'user/index.html')

def legalMentions(request):
	return render(request, 'user/legalMentions.html')

def contacts(request):
	return render(request, 'user/contacts.html')

@login_required(login_url='connection')
def favoris(request):
    return render(request, 'user/favoris.html')





