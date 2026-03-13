from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from.models import Recipe
# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'reciperate_app/index.html',context=context_dict)

def breakfast(request):
    recipes = Recipe.objects.filter(category='breakfast').order_by('-created_at')
    context_dict = {'recipes': recipes}
    return render(request, 'reciperate_app/breakfast.html',context=context_dict)

def lunch(request):
    context_dict = {}
    return render(request, 'reciperate_app/lunch.html', context=context_dict)

def dinner(request):
    context_dict = {}
    return render(request, 'reciperate_app/dinner.html', context=context_dict)

@login_required
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

def sign_up(request):
    context_dict = {}
    return render(request, 'reciperate_app/sign_up.html', context=context_dict)

def sign_in(request):
    context_dict = {}
    return render(request, 'reciperate_app/sign_in.html', context=context_dict)

def sign_out(request):
    context_dict = {}
    return render(request, 'reciperate_app/sign_out.html', context=context_dict)