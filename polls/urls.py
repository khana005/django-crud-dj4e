from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('owner', views.owner, name='owner'),
    path('owner/', views.owner, name='owner_slash'),
]
