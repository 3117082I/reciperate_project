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
            'image': image if image else 'recipe_images/default.jpg',
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
    hugh = create_user('hugh', 'Password456!')
    nadia = create_user('nadia', 'Password789!')
    hafsa = create_user('hafsa', 'Password1234!')
    zach = create_user('zach', 'Password1234!')

    #recipes
    pancakes = create_recipe(
        user=jack,
        name='Pancakes',
        url='https://www.bbcgoodfood.com/recipes/easy-pancakes',
        image='recipe_images/pancakes.jpg',
        category='Breakfast'
    )

    french_toast = create_recipe(
        user=zach,
        name='French Toast',
        url='https://www.bbcgoodfood.com/recipes/french-toast',
        image='recipe_images/french_toast.jpg',
        category='Breakfast'
    )

    pain_au_chocolat = create_recipe(
        user=nadia,
        name='Pain Au Chocolat',
        url='https://www.bbcgoodfood.com/recipes/pain-au-chocolat',
        image='recipe_images/pain_au_chocolat.jpg',
        category='Breakfast'
    )

    cheese_omelet = create_recipe(
        user=hugh,
        name='Cheese Omelette',
        url='https://www.bbcgoodfood.com/recipes/cheese-omelette',
        image='recipe_images/cheese_omelette.jpg',
        category='Breakfast'
    )

    falafel_burgers = create_recipe(
        user=hafsa,
        name='Falafel Burgers',
        url='https://www.bbcgoodfood.com/recipes/falafel-burgers-0',
        image='recipe_images/falafel_burgers.jpg',
        category='Lunch'
    )

    chicken_avocado_wrap = create_recipe(
        user=nadia,
        name='Spicy Chicken & Avocado Wraps',
        url='https://www.bbcgoodfood.com/recipes/spicy-chicken-avocado-wraps',
        image='recipe_images/chicken_avocado_wraps.jpg',
        category='Lunch'
    )

    ham_cheese_egg_bagel = create_recipe(
        user=hafsa,
        name='Air Fryer Ham, Cheese & Egg Bagel',
        url='https://www.bbcgoodfood.com/recipes/air-fryer-ham-cheese-egg-bagel',
        image='recipe_images/ham_cheese_egg_bagel.jpg',
        category='Lunch'
    )

    ultimate_chorizo_ciabatta = create_recipe(
        user=zach,
        name='Ultimate Chorizo Ciabatta',
        url='https://www.bbcgoodfood.com/recipes/ultimate-chorizo-ciabatta',
        image='recipe_images/ultimate_chorizo_ciabatta.jpg',
        category='Lunch'
    )

    chicken_pasta_bake = create_recipe(
        user=hugh,
        name='Chicken Pasta Bake',
        url='https://www.bbcgoodfood.com/recipes/chicken-pasta-bake',
        image='recipe_images/chicken_pasta_bake.jpg',
        category='Dinner'
    )

    creamy_chicken_pasta = create_recipe(
        user=jack,
        name='Creamy Chicken Pasta',
        url='https://www.bbcgoodfood.com/recipes/creamy-chicken-pasta',
        image='recipe_images/creamy_chicken_pasta.jpg',
        category='Dinner'
    )

    easy_chicken_curry = create_recipe(
        user=zach,
        name='Easy Chicken Curry',
        url='https://www.bbcgoodfood.com/recipes/easy-chicken-curry',
        image='recipe_images/easy_chicken_curry.jpg',
        category='Dinner'
    )

    crispy_chilli_beef = create_recipe(
        user=jack,
        name='Air Fryer Crispy Chilli Beef',
        url='https://www.bbcgoodfood.com/recipes/air-fryer-crispy-chilli-beef',
        image='recipe_images/crispy_chilli_beef.jpg',
        category='Dinner'
    )

    #likes
    create_like(jack, pancakes)
    create_like(hugh, pancakes)
    create_like(hafsa, pancakes)
    create_like(zach, pancakes)
    create_like(nadia, pancakes)
    create_like(hafsa, french_toast)
    create_like(hugh, french_toast)
    create_like(hugh, chicken_pasta_bake)
    create_like(jack, chicken_pasta_bake)
    create_like(jack, easy_chicken_curry)
    create_like(hugh, easy_chicken_curry)
    create_like(nadia, easy_chicken_curry)


if __name__ == '__main__':
    print("Populating database...")
    populate()