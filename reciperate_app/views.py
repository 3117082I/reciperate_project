from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from.models import Recipe
from django.contrib.auth import authenticate, login

# Create your views here.
def breakfast(request):
    recipes = Recipe.objects.filter(category='breakfast').order_by('-created_at')
    context_dict = {'recipes': recipes}
    return render(request, 'reciperate_app/breakfast.html',context=context_dict)

def lunch(request):
    recipes = Recipe.objects.filter(category='lunch').order_by('-created_at')
    context_dict = {'recipes': recipes}
    return render(request, 'reciperate_app/lunch.html',context=context_dict)

def dinner(request):
    recipes = Recipe.objects.filter(category='dinner').order_by('-created_at')
    context_dict = {'recipes': recipes}
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
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign_in')
    else:
        form = SignUpForm()
    context_dict = {'form': form}
    return render(request, 'reciperate_app/sign_up.html', context=context_dict)

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user_is_active:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'reciperate_app/sign_in.html')

    return render(request, 'reciperate_app/sign_in.html')

def sign_out(request):
    context_dict = {}
    return render(request, 'reciperate_app/sign_out.html', context=context_dict)

def home(request):
    context_dict = {}
    return render(request, 'reciperate_app/home.html', context=context_dict)