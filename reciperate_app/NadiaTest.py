from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from reciperate_app.models import Recipe, Like
from reciperate_app.forms import RecipeForm


class RecipeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='nadia',
            password='testpass123'
        )

    def test_recipe_str(self):
        recipe = Recipe.objects.create(
            user=self.user,
            name='Pancakes',
            url='www.bbcgoodfood.com/pancakes',
            category='breakfast'
        )
        self.assertEqual(str(recipe), 'Pancakes')

    def test_like_count_default(self):
        recipe = Recipe.objects.create(
            user=self.user,
            name='Pancakes',
            url='www.bbcgoodfood.com/pancakes',
            category='breakfast'
        )
        self.assertEqual(recipe.like_count, 0)

    def test_like_count_increases(self):
        recipe = Recipe.objects.create(
            user=self.user,
            name='Pancakes',
            url='www.bbcgoodfood.com/pancakes',
            category='breakfast'
        )
        Like.objects.create(user=self.user, recipe=recipe)
        self.assertEqual(recipe.like_count, 1)

    def test_recipe_saves_correct_category(self):
        recipe = Recipe.objects.create(
            user=self.user,
            name='Pancakes',
            url='www.bbcgoodfood.com/pancakes',
            category='breakfast'
        )
        self.assertEqual(recipe.category, 'breakfast')


class RecipeFormTests(TestCase):

    def test_valid_form(self):
        form = RecipeForm(data={
            'name': 'Pancakes',
            'url': 'www.bbcgoodfood.com/pancakes',
            'category': 'breakfast',
        })
        self.assertTrue(form.is_valid())

    def test_form_missing_name(self):
        form = RecipeForm(data={
            'url': 'www.bbcgoodfood.com/pancakes',
            'category': 'breakfast',
        })
        self.assertFalse(form.is_valid())

    def test_form_missing_category(self):
        form = RecipeForm(data={
            'name': 'Pancakes',
            'url': 'www.bbcgoodfood.com/pancakes',
        })
        self.assertFalse(form.is_valid())


class AddRecipeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='nadia',
            password='testpass123'
        )

    def test_add_recipe_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('reciperate:add_recipe'))
        self.assertEqual(response.status_code, 302) # redirect status code
        self.assertTrue(response.url.startswith('/reciperate/sign-in/'))

    def test_add_recipe_loads_when_logged_in(self):
        self.client.login(username='nadia', password='testpass123')
        response = self.client.get(reverse('reciperate:add_recipe'))
        self.assertEqual(response.status_code, 200) # success status code

    def test_add_recipe_form_on_page(self):
        self.client.login(username='nadia', password='testpass123')
        response = self.client.get(reverse('reciperate:add_recipe'))
        self.assertContains(response, 'enctype="multipart/form-data"')

    def test_valid_post_saves_recipe(self):
        self.client.login(username='nadia', password='testpass123')
        self.client.post(reverse('reciperate:add_recipe'), {
            'name': 'Pancakes',
            'url': 'www.bbcgoodfood.com/pancakes',
            'category': 'breakfast',
        })
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.first().name, 'Pancakes')

    def test_invalid_post_does_not_save(self):
        self.client.login(username='nadia', password='testpass123')
        self.client.post(reverse('reciperate:add_recipe'), {})
        self.assertEqual(Recipe.objects.count(), 0)


class SortingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='nadia',
            password='testpass123'
        )
        Recipe.objects.create(user=self.user, name='Avocado Toast', url='www.test.com', category='breakfast')
        Recipe.objects.create(user=self.user, name='Pancakes', url='www.test.com', category='breakfast')
        Recipe.objects.create(user=self.user, name='Omelette', url='www.test.com', category='breakfast')

    def test_breakfast_page_loads(self):
        response = self.client.get(reverse('reciperate:breakfast'))
        self.assertEqual(response.status_code, 200)

    def test_breakfast_shows_recipes(self):
        response = self.client.get(reverse('reciperate:breakfast'))
        self.assertIn('recipes', response.context)
        self.assertEqual(len(response.context['recipes']), 3)

    def test_lunch_page_loads(self):
        response = self.client.get(reverse('reciperate:lunch'))
        self.assertEqual(response.status_code, 200)

    def test_dinner_page_loads(self):
        response = self.client.get(reverse('reciperate:dinner'))
        self.assertEqual(response.status_code, 200)

    def test_lunch_shows_recipes(self):
        Recipe.objects.create(user=self.user, name='Chicken Wrap', url='www.test.com', category='lunch')
        response = self.client.get(reverse('reciperate:lunch'))
        self.assertIn('recipes', response.context)

    def test_dinner_shows_recipes(self):
        Recipe.objects.create(user=self.user, name='Chicken Curry', url='www.test.com', category='dinner')
        response = self.client.get(reverse('reciperate:dinner'))
        self.assertIn('recipes', response.context)

    def test_sort_by_newest(self):
        response = self.client.get(reverse('reciperate:breakfast') + '?sort=newest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['sort'], 'newest')

    def test_sort_by_az(self):
        response = self.client.get(reverse('reciperate:breakfast') + '?sort=az')
        recipes = list(response.context['recipes'])
        self.assertEqual(recipes[0].name, 'Avocado Toast')

    def test_sort_by_oldest(self):
        response = self.client.get(reverse('reciperate:breakfast') + '?sort=oldest')
        self.assertEqual(response.context['sort'], 'oldest')

    def test_sort_dropdown_on_page(self):
        response = self.client.get(reverse('reciperate:breakfast'))
        self.assertContains(response, 'Popular')
        self.assertContains(response, 'Newest')
        self.assertContains(response, 'Oldest')
        self.assertContains(response, 'A-Z')