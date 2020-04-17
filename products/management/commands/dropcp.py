""" this script drop datas from tables Category and Product"""
from django.core.management.base import BaseCommand
from products.models import Category as c , Product as p


class Command(BaseCommand):
    """ this class manages the parameters you can pass to python manage.py"""
    help = "this command drops the products.Category and products.Product tables"

    def _drop_db(self):
        """drops the datas"""
        print("\n","Cette commande vide les tables Category et Product.")
        cat = c.objects.all()
        prod = p.objects.all()
        print("\n", "avant : ")
        print(" cat / prod > ", len(cat)," / ", len(prod))

        cat.delete()
        prod.delete()
        print("\n", "après : ")
        print(" cat / prod > ", len(cat)," / ", len(prod))
    def handle(self, *args, **options):
        """throws the drop_db function"""
        print("\n", "* "*30)
        self._drop_db() 
        print("\n", "* "*30, "\n")