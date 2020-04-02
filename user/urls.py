from django.urls import path

from . import views as v # import views so we can use them in urls.

urlpatterns = [
    path(r'legalMentions', v.legalMentions, name="legalMentions"),
    path(r'contacts', v.contacts, name="contacts"),
    path(r'logout', v.logoutUser, name="logout"),
    path(r'MyAccount', v.MyAccountView.as_view(), name="MyAccount"),
    path(r'MyAccount/<int:my_option>', v.MyAccountView.as_view(), name="MyAccount"),
    path(r'MyAccount/<int:my_option>/<str:my_chain>', v.MyAccountView.as_view(), name="MyAccount"),
    path(r'connection', v.ConnectionView.as_view(), name="connection"),
    path(r'register', v.RegisterView.as_view(), name="register"),
    path(r'favorite/<str:prod_name>', v.FavoriteView.as_view(), name="favorite"),
    path(r'favorite', v.FavoriteView.as_view(), name="favorite"),

]


