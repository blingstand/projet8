from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .form import SearchForm, AdvancedSearchForm

from products.models import Category, Product
from .searcher import find_subs
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
            find_prod, product, substitutes = find_subs(get_from_input, category)
            context = { "name" : category, "good_prods" : substitutes, "no_prod" : True}
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
            try:
                find_prod, product, substitutes = find_subs(get_from_input)
                if find_prod:
                    print("Résultats : le produit recherché était", product,\
                        "et voici les substituts trouvés :\n", substitutes)
                    print("* * * "*10)
                    many = len(substitutes) >= 1 
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>many", many)
                    context = { 
                    "name" : product.name, 
                    "good_prods" : substitutes,
                    "many" : many }
                    return render(request, "research/results.html", context)
                else:
                    messages.error(request, "Pas de résultats dans la base actuellement pour"\
                    " la recherche : '{}'.".format(get_from_input))
                    context = { 
                        'form' : form, "categories" : substitutes.keys,
                        'however' : " Cependant j'ai des résultats en rapport avec ta recherche ...", 
                        'get_from_input' : get_from_input}
                    return render(request, 'research/index.html', context)
            except Exception as e:
                print(e) #for debug
                messages.error(request, "Pas de résultats dans la base actuellement pour"\
                    " la recherche : {}.".format(get_from_input))
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