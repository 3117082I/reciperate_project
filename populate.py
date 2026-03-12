import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'reciperate_project.settings')

import django
django.setup()
from django.contrib.auth.models import User
from reciperate_app.models import Recipe, UserProfile, Like

def create_user(username, password):
    user, created = User.objects.get_or_create(username=username)

    if created:
        user.set_password(password)
        user.save()

    UserProfile.objects.get_or_create(user=user)
    return user

def create_recipe(user, name, url, category, image=None):
    recipe, created = Recipe.objects.get_or_create(
        user=user,
        name=name,
        defaults={
            'url': url,
            'category': category,
            'image': image,
        }
    )
    return recipe

def create_like(user, recipe):
    like, created = Like.objects.get_or_create(
        user=user,
        recipe=recipe
    )
    return like

def populate():
    #users
    jack = create_user('jack', 'Password123!')
    phil = create_user('phil', 'mypassword')

    #recipes
    pancakes = create_recipe(
        user=jack,
        name='Pancakes',
        url='https://www.bbcgoodfood.com/recipes/easy-pancakes',
        category='Breakfast'
    )

    chicken_pasta_bake = create_recipe(
        user=phil,
        name='Chicken Pasta Bake',
        url='https://www.bbcgoodfood.com/recipes/chicken-pasta-bake',
        category='Dinner'
    )

    #likes
    create_like(jack, pancakes)
    create_like(phil, chicken_pasta_bake)
    create_like(jack, chicken_pasta_bake)

if __name__ == '__main__':
    print("Populating database...")
    populate()