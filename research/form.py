from django import forms


class SearchForm(forms.Form):
    simple_search = forms.CharField(label="Entrez le nom d'un produit", max_length=50)