from django.shortcuts import render
from .models import Recipe, Like

def render_recipe(request, category, template_name):
    sort = request.GET.get("sort", "popular")

    if sort == "newest":
        recipes = Recipe.objects.filter(category=category).order_by("-created_at")
    elif sort == "oldest":
        recipes = Recipe.objects.filter(category=category).order_by("created_at")
    elif sort == "az":
        recipes = Recipe.objects.filter(category=category).order_by("name")
    else:
        recipes = sorted(Recipe.objects.filter(category=category), key=lambda r: r.like_count, reverse=True)

    context_dict = {"recipes": recipes, "sort": sort}

    if request.user.is_authenticated:
        context_dict["liked_posts"] = Like.objects.filter(
            user=request.user).values_list('recipe', flat=True)

    return render(request, template_name, context=context_dict)
