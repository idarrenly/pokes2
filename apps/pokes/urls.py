from django.conf.urls import url
from . import views  

urlpatterns = [
    url(r'^$', views.index),                 #http://localhost:8000 or http://localhost:8000/
    url('^main$', views.index),              #http://localhost:8000/main
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^pokes$', views.dashboard),
    url(r'^pokes/(?P<user_id>\d+)$', views.poked),
]



