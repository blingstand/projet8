from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .form import UserForm
from .models import Profile
from .backend import MyBackend


def register(request):
    """ display html page with form in order to register a new user"""
    if request.user.is_authenticated:
        return redirect('index') #if auth user comes to register page
    form = UserForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password =form.cleaned_data.get('password')
        new_user = User.objects.create_user(username=username, password=password)
        new_profile = Profile(user=new_user)

        return HttpResponse('inscription réussie pour {}'.format(new_profile))
    context = {'form':form}
    return render(request, 'coach/register.html', context)

def connection(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = UserForm(request.POST or None)
    if form.is_valid(): 
        username = form.cleaned_data.get('username')
        password =form.cleaned_data.get('password')
        new_user = authenticate(username=username, password=password)

        if new_user is not None:
            login(request, new_user)
            return redirect('index')
        else:
            msg = Profile.objects.filter(username="adrien")[0]
            return HttpResponse(msg.password)
            messages.info(request, 'pseudo ou mot de passe incorrect')

    context = {'form' : form}
    return render(request, 'coach/login.html', context)


def logout(request):
    logout(request)
    return redirect('index')



def index(request):
    # message = "Bienvenu sur le site pureBeurre !"
    context = {
    	'connected' : False
        }
    return render(request, 'coach/index.html', context)

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





