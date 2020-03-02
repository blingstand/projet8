from django.shortcuts import render

from django.http import HttpResponse

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
