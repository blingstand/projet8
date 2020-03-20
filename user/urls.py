from django.urls import path

from . import views as v # import views so we can use them in urls.

urlpatterns = [
    path(r'legalMentions', v.legalMentions, name="legalMentions"),
    path(r'contacts', v.contacts, name="contacts"),
    path(r'favoris', v.favoris, name="favoris"),
    path(r'logout', v.logoutUser, name="logout"),
    path(r'myAccount', v.myAccountView.as_view(), name="myAccount"),
    path(r'myAccount/<int:my_option>', v.myAccountView.as_view(), name="myAccount"),
    path(r'myAccount/<int:my_option>/<str:my_chain>', v.myAccountView.as_view(), name="myAccount"),
    path(r'connection', v.ConnectionView.as_view(), name="connection"),
    path(r'register', v.RegisterView.as_view(), name="register"),

]


