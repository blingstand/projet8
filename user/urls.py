from django.urls import path

from . import views as v # import views so we can use them in urls.

urlpatterns = [
    path(r'legalMentions', v.legalMentions, name="legalMentions"),
    path(r'contacts', v.contacts, name="contacts"),
    path(r'logout', v.logoutUser, name="logout"),
    path(r'myAccount', v.MyAccountView.as_view(), name="myAccount"),
    path(r'myAccount/<int:my_option>', v.MyAccountView.as_view(), name="myAccount"),
    path(r'myAccount/<int:my_option>/<str:my_chain>', v.MyAccountView.as_view(), name="myAccount"),
    path(r'connection', v.ConnectionView.as_view(), name="connection"),
    path(r'register', v.RegisterView.as_view(), name="register"),
    path(r'favorite/<str:prod_name>', v.FavoriteView.as_view(), name="favorite"),
    path(r'favorite', v.FavoriteView.as_view(), name="favorite"),

]


