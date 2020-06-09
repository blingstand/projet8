from django.conf import settings
from django.core.mail import send_mail

def notify_db_fv(self, profile, prod_name):
        """ adds a given prod to the profile fav list"""
        product = Product.objects.get(name=prod_name) #it always exists, so don't need : try/except
        profile.favlist.add(product)
        profile.save()

class MailAgent():

    def send_confirm_mail(self, mail, code):
        """ sends a code by mail to confirm mail adress before adding in base """
        subject = "Confirmation de votre mail "
        message = f"Cliquez sur ce lien http://127.0.0.1:8000/user/myAccount/1/{code}"\
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