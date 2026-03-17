from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm, SignUpForm
from .models import Recipe, Like
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

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
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('reciperate:sign_in')
    else:
        form = SignUpForm()
    return render(request, 'reciperate_app/sign_up.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('reciperate:home'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'reciperate_app/sign_in.html')

def sign_out(request):
    logout(request)
    return redirect(reverse('reciperate:home'))

def home(request):
    context_dict = {}
    return render(request, 'reciperate_app/home.html', context=context_dict)

@login_required
@require_http_methods(['POST', 'DELETE'])
def like_recipe(request, category, recipe_id):
    user = request.user
    print(user)
    if request.method == 'POST':
        Like.objects.create(user=request.user, recipe=recipe_id)
        liked = True
    else:
        Like.objects.filter(user=request.user, recipe=recipe_id).delete()
        liked = False

    like_count = Like.objects.filter(user=request.user, recipe_id=recipe_id).count()
    return JsonResponse({'liked': liked, 'like_count': like_count})