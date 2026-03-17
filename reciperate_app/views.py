from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm, SignUpForm
from .models import Recipe, Like
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .utils import render_recipe

def breakfast(request):
    return render_recipe(request, 'breakfast', 'reciperate_app/breakfast.html')

def lunch(request):
    return render_recipe(request, 'lunch', 'reciperate_app/lunch.html')

def dinner(request):
    return render_recipe(request, 'dinner', 'reciperate_app/dinner.html')

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
            return redirect('reciperate:sign_in')
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
            if user.is_active:
                login(request, user)
                return redirect(reverse('reciperate:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'reciperate_app/sign_in.html')

def sign_out(request):
    context_dict = {}
    return render(request, 'reciperate_app/sign_out.html', context=context_dict)

def home(request):
    context_dict = {}
    return render(request, 'reciperate_app/home.html', context=context_dict)

@login_required
@require_http_methods(['POST', 'DELETE'])
def like_recipe(request, category, recipe_id):
    user = request.user
    recipe = Recipe.objects.get(id=recipe_id)

    if request.method == 'POST':
        Like.objects.create(user=request.user, recipe=recipe)
        liked = True
    else:
        Like.objects.filter(user=request.user, recipe=recipe).delete()
        liked = False

    like_count = recipe.like_count
    return JsonResponse({'liked': liked, 'like_count': like_count})