from django.urls import path
from reciperate_app import views

app_name = 'reciperate'
urlpatterns = [
    path('', views.index, name='index'),
]
