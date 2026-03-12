from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
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
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            form = RecipeForm()
    else:
        form = RecipeForm()
    return render(request, 'add_recipe.html', {'form': form})

def signup(request):
    return HttpResponse("Create Account")

def signin(request):
    return HttpResponse("Sign in")