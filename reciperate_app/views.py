from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'reciperate_app/index.html',context=context_dict)

def breakfast(request):
    context_dict = {}
    return render(request, 'reciperate_app/breakfast.html',context=context_dict)

def lunch(request):
    context_dict = {}
    return render(request, 'reciperate_app/lunch.html', context=context_dict)

def dinner(request):
    context_dict = {}
    return render(request, 'reciperate_app/dinner.html', context=context_dict)

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
    return render(request, 'reciperate_app/add_recipe.html', {'form': form})

def signup(request):
    context_dict = {}
    return render(request, 'reciperate_app/sign_up.html', context=context_dict)

def signin(request):
    context_dict = {}
    return render(request, 'reciperate_app/sign_in.html', context=context_dict)