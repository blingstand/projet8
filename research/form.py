from django import forms


class SearchForm(forms.Form):
    simple_search = forms.CharField(
    	label="Entrez le nom d'un produit", 
    	max_length=50,
    	widget=forms.TextInput(attrs={'id': 'simple_form_input'}) )