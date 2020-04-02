from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class MoreUserDataForm(forms.Form):

	mail = forms.EmailField(			label="Mon mail", 
										max_length=100, 
										widget=forms.TextInput(attrs={'class': 'account_i'}))

class AddFavorite(forms.form): 
	fav = forms.MultipleChoiceField(	
		required=False,
        label="ajouter aux favoris",
        widget=forms.CheckboxSelectMultiple)