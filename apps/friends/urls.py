from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^main$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^friends$', views.friends),
	url(r'^add_friend/(?P<user_id>\d+)$', views.add_friend),
	url(r'^user/(?P<user_id>\d+)$', views.user_profile),
	url(r'^remove_friend/(?P<user_id>\d+)$', views.remove_friend),
	url(r'^logout$', views.logout)
]