from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import Contact
from .form import ContactForm


def register(request):
    form = ContactForm()

    if request.method = "POST":
        form = ContactForm(request.post)

    context = {"form" : form}
    return render(request, 'coach/register.html', context)

def login(request):
    form = ContactForm()
    context = {"form" : form}
    return render(request, 'coach/login.html', context)

def index(request):
    # message = "Bienvenu sur le site pureBeurre !"
    print("\n"*20)
    print("* * *  "* 20)
    context = {
    	'connected' : False}
    return render(request, 'coach/index.html', context)

def legalMentions(request):
	return render(request, 'coach/legalMentions.html')

def contacts(request):
	return render(request, 'coach/contacts.html')

def monCompte(request):
	return render(request, 'coach/monCompte.html')

def favoris(request):
    return render(request, 'coach/favoris.html')





