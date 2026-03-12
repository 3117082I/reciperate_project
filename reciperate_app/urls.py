from django.urls import path
from reciperate_app import views

app_name = 'reciperate'

urlpatterns = [
    path('', views.index, name='index'),
    path('breakfast/', views.breakfast, name='breakfast'),
    path('lunch/', views.lunch, name='lunch'),
    path('dinner/', views.dinner, name='dinner'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('sign-up/', views.signup, name='signup'),
    path('sign-in/', views.signin, name='signin')
]
