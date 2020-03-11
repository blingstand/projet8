from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views import View

from .form import UserForm
from .models import Profile



class RegisterView(View):
    """ This class deals with registration
        get > loads a registration page
        post > analyses datas to try to create a new user and profile
    """
    def get(self, request): 
        """ display html page with form in order to register a new user"""
        if request.user.is_authenticated:
            return redirect('index') #if auth user comes to register page
        form = UserForm()
        context = {'form':form}
        return render(request, 'coach/register.html', context)
    
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
                messages.success(request, "Félicitation vous venez de créer : {} !".format(username))
                return redirect('connection')
            except IntegrityError:
                messages.error(request, "Cet utilisateur existe déjà !")
                return redirect('register')
        messages.error(request, "Problème dans le formulaire !")
        return redirect('register')
        
    

class ConnectionView(View):
    """ This class deals with login
        get > loads a connection page
        post > analyses datas in order to try to authenticate
    """
    def get(self, request):
        """ loads a connection page """
        if request.user.is_authenticated:
            return redirect('index')
        form = UserForm()
        context = {'form' : form}
        return render(request, 'coach/login.html', context)
    
    def post(self, request):
        """ analyses datas in order to try to authenticate """
        form = UserForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data.get('username')
            password =form.cleaned_data.get('password')
            new_user = authenticate(username=username, password=password)

            if new_user is not None:
                login(request, new_user)
                return redirect('index')
            else:
                messages.info(request, 'pseudo ou mot de passe incorrect')
                return redirect('connection')
        messages.error(request, "Problème dans le formulaire !")
        return redirect('connection')
                


def logoutUser(request):
    logout(request)
    return redirect('index')



def index(request):
    # message = "Bienvenu sur le site pureBeurre !"

    return render(request, 'coach/index.html')

def legalMentions(request):
	return render(request, 'coach/legalMentions.html')

def contacts(request):
	return render(request, 'coach/contacts.html')

@login_required(login_url='login')
def monCompte(request):
	return render(request, 'coach/monCompte.html')

@login_required(login_url='login')
def favoris(request):
    return render(request, 'coach/favoris.html')





