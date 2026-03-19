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
        category='breakfast'
    )

    french_toast = create_recipe(
        user=zach,
        name='French Toast',
        url='https://www.bbcgoodfood.com/recipes/french-toast',
        image='recipe_images/french_toast.jpg',
        category='breakfast'
    )

    pain_au_chocolat = create_recipe(
        user=nadia,
        name='Pain Au Chocolat',
        url='https://www.bbcgoodfood.com/recipes/pain-au-chocolat',
        image='recipe_images/pain_au_chocolat.jpg',
        category='breakfast'
    )

    cheese_omelet = create_recipe(
        user=hugh,
        name='Cheese Omelette',
        url='https://www.bbcgoodfood.com/recipes/cheese-omelette',
        image='recipe_images/cheese_omelette.jpg',
        category='breakfast'
    )

    porridge = create_recipe(
        user=zach,
        name='Creamy Oat Porridge',
        url='https://www.allrecipes.com/recipe/245498/overnight-oats/',
        image='recipe_images/porridge.jpg',
        category='breakfast'
    )

    egg_muffins = create_recipe(
        user=hafsa,
        name='Breakfast Egg Muffins',
        url='https://www.allrecipes.com/recipe/222586/egg-muffins/',
        image='recipe_images/egg_muffins.jpg',
        category='breakfast'
    )

    waffles = create_recipe(
        user=jack,
        name='Golden Belgian Waffles',
        url='https://www.allrecipes.com/recipe/20513/classic-waffles/',
        image='recipe_images/waffles.jpg',
        category='breakfast'
    )

    fruit_yogurt = create_recipe(
        user=nadia,
        name='Fruit & Yogurt Bowl',
        url='https://www.simplyrecipes.com/yogurt-parfait-recipe-5180007',
        image='recipe_images/fruit_yogurt.jpg',
        category='breakfast'
    )

    falafel_burgers = create_recipe(
        user=hafsa,
        name='Falafel Burgers',
        url='https://www.bbcgoodfood.com/recipes/falafel-burgers-0',
        image='recipe_images/falafel_burgers.jpg',
        category='lunch'
    )

    chicken_avocado_wrap = create_recipe(
        user=nadia,
        name='Spicy Chicken & Avocado Wraps',
        url='https://www.bbcgoodfood.com/recipes/spicy-chicken-avocado-wraps',
        image='recipe_images/chicken_avocado_wraps.jpg',
        category='lunch'
    )

    ham_cheese_egg_bagel = create_recipe(
        user=hafsa,
        name='Air Fryer Ham, Cheese & Egg Bagel',
        url='https://www.bbcgoodfood.com/recipes/air-fryer-ham-cheese-egg-bagel',
        image='recipe_images/ham_cheese_egg_bagel.jpg',
        category='lunch'
    )

    ultimate_chorizo_ciabatta = create_recipe(
        user=zach,
        name='Ultimate Chorizo Ciabatta',
        url='https://www.bbcgoodfood.com/recipes/ultimate-chorizo-ciabatta',
        image='recipe_images/ultimate_chorizo_ciabatta.jpg',
        category='lunch'
    )

    grilled_cheese = create_recipe(
        user=hugh,
        name='Classic Grilled Cheese Sandwich',
        url='https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/',
        image='recipe_images/grilled_cheese.jpg',
        category='lunch'
    )

    chicken_wrap = create_recipe(
        user=zach,
        name='Grilled Chicken Wrap',
        url='https://www.bbcgoodfood.com/recipes/grilled-chicken-wrap',
        image='recipe_images/chicken_wrap.jpg',
        category='lunch'
    )

    pasta_salad = create_recipe(
        user=hafsa,
        name='Mediterranean Pasta Salad',
        url='https://www.allrecipes.com/recipe/14385/pasta-salad/',
        image='recipe_images/pasta_salad.jpg',
        category='lunch'
    )

    quesadilla = create_recipe(
        user=nadia,
        name='Cheesy Chicken Quesadilla',
        url='https://www.simplyrecipes.com/recipes/chicken_quesadilla/',
        image='recipe_images/quesadilla.jpg',
        category='lunch'
    )

    chicken_pasta_bake = create_recipe(
        user=hugh,
        name='Chicken Pasta Bake',
        url='https://www.bbcgoodfood.com/recipes/chicken-pasta-bake',
        image='recipe_images/chicken_pasta_bake.jpg',
        category='dinner'
    )

    creamy_chicken_pasta = create_recipe(
        user=jack,
        name='Creamy Chicken Pasta',
        url='https://www.bbcgoodfood.com/recipes/creamy-chicken-pasta',
        image='recipe_images/creamy_chicken_pasta.jpg',
        category='dinner'
    )

    easy_chicken_curry = create_recipe(
        user=zach,
        name='Easy Chicken Curry',
        url='https://www.bbcgoodfood.com/recipes/easy-chicken-curry',
        image='recipe_images/easy_chicken_curry.jpg',
        category='dinner'
    )

    crispy_chilli_beef = create_recipe(
        user=jack,
        name='Air Fryer Crispy Chilli Beef',
        url='https://www.bbcgoodfood.com/recipes/air-fryer-crispy-chilli-beef',
        image='recipe_images/crispy_chilli_beef.jpg',
        category='dinner'
    )

    lasagna = create_recipe(
        user=jack,
        name='Homemade Lasagna',
        url='https://www.allrecipes.com/recipe/23600/worlds-best-lasagna/',
        image='recipe_images/lasagna.jpg',
        category='dinner'
    )

    roast_chicken = create_recipe(
        user=hugh,
        name='Roast Chicken with Herbs',
        url='https://www.bbcgoodfood.com/recipes/roast-chicken',
        image='recipe_images/roast_chicken.jpg',
        category='dinner'
    )

    beef_tacos = create_recipe(
        user=zach,
        name='Spicy Beef Tacos',
        url='https://www.simplyrecipes.com/recipes/beef_tacos/',
        image='recipe_images/beef_tacos.jpg',
        category='dinner'
    )

    veg_curry = create_recipe(
        user=hafsa,
        name='Vegetable Coconut Curry',
        url='https://www.bbcgoodfood.com/recipes/vegetable-curry',
        image='recipe_images/veg_curry.jpg',
        category='dinner'
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