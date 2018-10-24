from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='homepage'),
    url(r'^reisplanner/', views.reisplanner, name='reisplanner'),
]
