from django.shortcuts import render
from .models import Recipe, Like

def render_recipe(request, category, template_name):
    recipes = Recipe.objects.filter(category=category).order_by('-created_at')
    context_dict = {'recipes': recipes}

    if request.user.is_authenticated:
        context_dict["liked_posts"] = Like.objects.filter(
            user=request.user).values_list('recipe', flat=True)

    return render(request, template_name, context=context_dict)
