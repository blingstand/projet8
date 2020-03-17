from django import forms


class SearchForm(forms.Form):
    simple_search = forms.CharField(
        label="Entrez le nom d'un produit", 
        max_length=50,
        widget=forms.TextInput(attrs={'id': 'simple_form_input'}) )




class AdvancedSearchForm(forms.Form):
    FAV_PACKAGINGS = [
    (1, "plastique"), (2, "sachet"), (3, "cartons"),
    (4, "verre"), (5, "métal"), (6, "aluminium")]
    name = forms.CharField(
        label="nom",
        required=True)
    category = forms.CharField(
        label="catégorie",
        required=False)
    nutriscore = forms.MultipleChoiceField(
        label="nutriscore",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[(1,"A"),(2,"B"),(3,"C"),(4, "D"),(5, "E")])
    packaging = forms.MultipleChoiceField(
        label="conditionnement",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=FAV_PACKAGINGS)