# global
import random, string

#django
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db import IntegrityError

#from current app
from .models import Profile

#from other app import
from products.models import Product

def notify_db_fv(profile, prod_name):
    """ adds a given prod to the profile fav list"""
    product = Product.objects.get(name=prod_name) 
    profile.favlist.add(product)
    profile.save()

def add_new_user(name, password):
    """
    Tries to add a new user in base and return Boolean and message
        True = Success / False = Fail
    """
    try:
        new_user = User(username=name)
        new_user.set_password(password)
        new_user.save()
        new_profile = Profile(user=new_user)
        new_profile.save()
        return True, f"Félicitation vous venez de créer : {name} !"
    except IntegrityError:
        return False, "Cet utilisateur existe déjà !"
#usefull function for myAccount and Favorite class
def get_user_and_profile(request):
    """ return the session user and the profile he belongs """
    user_found = request.user
    ufpk = user_found.pk #user_found_primary_key = ufpk
    profile_found = Profile.objects.filter(user=ufpk)[0]
    return user_found, profile_found

class MailAgent():

    def send_confirm_mail(self, mail, code, request):
        """ sends a code by mail to confirm mail adress before adding in base """
        subject = "Confirmation de votre mail "
        url = request.build_absolute_uri()
        print(type(url))
        print(f'{url}/1/{code}')
        print(f'{url[:-2]}/1/{code}')
        
        message = f"Cliquez sur ce lien {url[:-2]}/1/{code}"\
        " pour confirmer votre mail"
        from_email = settings.EMAIL_HOST_USER
        to_list = [mail]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


    def notify_db_mav(self, user, profile, code, mail):
        """ notifies the db that a code in a confirm mail has been send """
        profile.mail_confirm_sent = True
        profile.code = code
        profile.save()
        user.email = mail
        user.save()