from django.urls import path
from reciperate_app import views

app_name = 'reciperate'
urlpatterns = [
    path('', views.index, name='index'),
    path('breakfast/', views.breakfast, name='breakfast'),
    path('lunch/', views.lunch, name='lunch'),
    path('dinner/', views.dinner, name='dinner'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='about')
]
