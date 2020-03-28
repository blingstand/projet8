from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .form import SearchForm, AdvancedSearchForm

from products.models import Category, Product
from .searcher import Search
# Create your views here.

class AdvancedSearchView(View):
    """ manage a HttpResponse in case of get or post method 
    request for this url research/advancedSearch"""

    def get(self, request):
        """ manage the HttpResponse for the SearchFormView with get method request """
        form = AdvancedSearchForm()
        context={'form' : form}
        return render(request, "research/advancedSearch.html", context)

    def post(self, request):
        form = AdvancedSearchForm(request.POST)
        results=(1,2,3)
        if form.is_valid():
            results = [r for r in range(10)]
            context = { "results" : results}
            return render(request, "research/results.html", context)
        return HttpResponse("Pb dans le form")

class ResultsView(View):
    """ manage a HttpResponse in case of get or post method 
    request for this url research/advancedSearch"""

    def get(self, request, category=None, get_from_input=None):
        """ manage the HttpResponse for the SearchFormView with get method request """
        if category is not None:
            search = Search(get_from_input, category)
            print(f"Je cherche des substituts avec {get_from_input} et {category}")
            substitutes = search.list_sub
            context = { "name" : category, "substitutes" : substitutes, "no_prod" : True}
        return render(request, "research/results.html", context)

    def post(self, request, category=None, get_from_input=None):
        pass

class IndexView(View):
    """ gère les index """
    def get(self, request):
        form = SearchForm()
        context = {'form' : form}
        return render(request, 'research/index.html', context)
    
    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid(): 
            #I throw a search 
            get_from_input = form.cleaned_data["simple_search"] 
            #I write result in context
            search = Search(get_from_input)
            print("* * * "*10)
            print("je cherche dans la base pour le mot : {}".format(get_from_input))
            prod = search.prod
            substitutes = search.list_sub
            if prod:
                print("Résultats : le produit recherché était", prod,\
                    "et voici les substituts trouvés :\n", substitutes)
                print("* * * "*10)
                context = { 
                "product" : prod, 
                "nutriscore" : prod.nutriscore.upper(), 
                "substitutes" : substitutes }
                return render(request, "research/results.html", context)
            elif search.cat_to_choose is not None:
                messages.error(request, "Pas de résultats parfaitement identiques "\
                    f"dans la base actuellement pour la recherche : {get_from_input}.")
                context = { 
                    'form' : form, "categories" : search.cat_to_choose,
                    'however' : " Cependant j'ai des résultats en rapport avec ta recherche ...", 
                    'get_from_input' : get_from_input, "few_cat" : len(search.cat_to_choose) <= 3}
                return render(request, 'research/index.html', context)
            else:
                messages.error(request, "Pas de résultats dans la base actuellement pour"\
                    f" la recherche : {get_from_input}.")
                return redirect("research:index")
                

                # alert me 
                # œœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœ
                # subject = "catégorie à ajouter"
                # message = "une nouvelle catégorie à ajouter : {}".format(get_from_input)
                # from_email = settings.EMAIL_HOST_USER
                # to_list = [settings.EMAIL_HOST_USER]
                # send_mail(subject, message, from_email, to_list, fail_silently=True)
                # œœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœœ
                # prepare work
            context = {"form": form}
            return render(request, "research/index.html", context)
            
        return HttpResponse ("Problème dans le formulaire")