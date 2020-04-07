from django.urls import path

from . import views as v # import views so we can use them in urls.

urlpatterns = [
	path(r'legalNotice', v.LegalNoticeView.as_view(), name="legalNotice"),
]