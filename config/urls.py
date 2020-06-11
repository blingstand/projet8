"""pureBeurre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include
from django.contrib import admin

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path(r'p10/user/', include(('user.urls', 'user'), namespace='user')),
    path(r'p10/products/', include(('products.urls', 'products'), namespace='products')),
    path(r'p10/', include(('research.urls', ''))),
    path(r'p10/research/', include(('research.urls', 'research'), namespace='research')),
    path(r'p10/skeleton/', include(('skeleton.urls', 'skeleton'), namespace='skeleton')),
    path(r'p10/admin/', admin.site.urls),
    path('sentry-debug/', trigger_error),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path(r'__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
