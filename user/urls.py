from django.urls import path

from . import views as v # import views so we can use them in urls.

urlpatterns = [
    path(r'', v.index, name="index"), # "/store" will call the method "index" in "views.py"
    path(r'index', v.index, name="index"),
    path(r'legalMentions', v.legalMentions, name="legalMentions"),
    path(r'contacts', v.contacts, name="contacts"),
    path(r'favoris', v.favoris, name="favoris"),
    path(r'logout', v.logoutUser, name="logout"),
    path(r'myAccount', v.myAccountView.as_view(), name="myAccount"),
    path(r'myAccount/<str:new_mail>', v.myAccountView.as_view(), name="myAccount"),
    path(r'myAccount/<int:mail_confirm>/<str:get_mail>', v.myAccountView.as_view(), name="myAccount"),
    path(r'connection', v.ConnectionView.as_view(), name="connection"),
    path(r'register', v.RegisterView.as_view(), name="register"),

]


