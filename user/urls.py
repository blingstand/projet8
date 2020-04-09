from django.urls import path

from . import views as v # import views so we can use them in urls.

urlpatterns = [
    path(r'connection', v.ConnectionView.as_view(), name="connection"),
    path(r'favorite/<str:prod_name>', v.FavoriteView.as_view(), name="favorite"),
    path(r'favorite', v.FavoriteView.as_view(), name="favorite"),
    path(r'logout', v.logoutUser, name="logout"),
    path(r'myAccount', v.MyAccountView.as_view(), name="myAccount"),
    path(r'myAccount/<int:my_option>', v.MyAccountView.as_view(), name="myAccount"),
    path(r'myAccount/<int:my_option>/<str:code>', v.MyAccountView.as_view(), name="myAccount"),
    path(r'register', v.RegisterView.as_view(), name="register"),

]


