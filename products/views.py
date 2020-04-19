from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from products.models import Product

class InfosView(View):
    """ This class deals with login
        get > loads a connection page
        post > analyses datas in order to try to authenticate
    """
    def get(self, request, prod_name):
        """ manage the get request concerning the connection page """
        if request.user.is_authenticated:
            if prod_name:
                prod = Product.objects.get(name=prod_name)
                context={
                    'prod' : prod }
                return render(request, 'products/infos.html', context)
            return  redirect('research/index')
        return render(request, 'user/connection.html', context)