from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Reciperate Home Page")

def breakfast(request):
    #recipes = Recipe.objects.filter(category="breakfast").order_by('-likes')
    # this commented code should work once the models are sorted out. For now, I'm just using dummy data - Hafsa

    recipes = [
        {
            "image": "",
            "url": "#",
            "likes": 0,
        },
        {
            "image": "",
            "url": "#",
            "likes": 0,
        },
        {
            "image": "",
            "url": "#",
            "likes": 0,
        },
        {
            "image": "",
            "url": "#",
            "likes": 0,
        },
    ]


    return render(request, "breakfast.html", {"recipes:recipes"})

def lunch(request):
    return HttpResponse("Lunch")

def dinner(request):
    return HttpResponse("Dinner")

def add_recipe(request):
    return HttpResponse("Add Recipe")

def signup(request):
    return HttpResponse("Create Account")

def signin(request):
    return HttpResponse("Sign in")