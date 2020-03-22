from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .form import SearchForm, AdvancedSearchForm

from products.models import Category, Product
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

    def get(self, request):
        """ manage the HttpResponse for the SearchFormView with get method request """
        return render(request, "research/results.html")

class IndexView(View):
    
    def get(self, request):
        # message = "Bienvenu sur le site pureBeurre !"
        form = SearchForm()
        context = { 'form' : form }
        return render(request, 'research/index.html', context)
    
    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid(): 
            #I throw a search 
            get_from_input = form.cleaned_data["simple_search"] 
            #I write result in context
            try:
                print("je cherche")
                cat_found = Category.objects.filter(name__contains=get_from_input)
                prod_found = Product.objects.filter(category=cat_found[0])
                good_prods_nutriscore = [prod.nutriscore for prod in prod_found]
                prods = Product.objects.filter(
                    category=cat_found[0], 
                    nutriscore=min(good_prods_nutriscore))
                best = prods[0]
                good_prods = prods[1:]
                print(best, good_prods)
                context = { 
                "name" : cat_found[0].name, 
                "best" : best, 
                "good_prods" : good_prods}
                return render(request, "research/results.html", context)
            except Exception as e:
                raise e #for debug
                messages.error(request, "Pas de résultats dans la base actuellement pour"\
                    " la recherche - {}.".format(get_from_input))
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