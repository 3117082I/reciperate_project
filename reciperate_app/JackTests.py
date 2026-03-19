from django.test import TestCase
from django.contrib.auth.models import User
from reciperate_app.models import Recipe, UserProfile, Like
from population_script import create_user, create_recipe, create_like
from django.urls import reverse

# Create your tests here.
# DATABASE + POPULATE SCRIPT TESTS

class UserProfileModelTest(TestCase):
    def test_userprofile_str_returns_username(self):
        user = User.objects.create_user(username='jack', password='testpass123')
        profile = UserProfile.objects.create(user=user)

        self.assertEqual(str(profile), 'jack')


class RecipeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jack', password='testpass123')

    def test_recipe_creation(self):
        recipe = Recipe.objects.create(
            user=self.user,
            name='Pancakes',
            url='https://example.com/pancakes',
            category='breakfast'
        )

        self.assertEqual(recipe.name, 'Pancakes')
        self.assertEqual(recipe.user.username, 'jack')
        self.assertEqual(recipe.category, 'breakfast')

    def test_recipe_str_returns_name(self):
        recipe = Recipe.objects.create(
            user=self.user,
            name='French Toast',
            url='https://example.com/french-toast',
            category='breakfast'
        )

        self.assertEqual(str(recipe), 'French Toast')

    def test_like_count_starts_at_zero(self):
        recipe = Recipe.objects.create(
            user=self.user,
            name='Omelette',
            url='https://example.com/omelette',
            category='breakfast'
        )

        self.assertEqual(recipe.like_count, 0)

    def test_like_count_increases_when_recipe_is_liked(self):
        recipe = Recipe.objects.create(
            user=self.user,
            name='Pasta',
            url='https://example.com/pasta',
            category='dinner'
        )

        other_user = User.objects.create_user(username='hugh', password='testpass123')
        Like.objects.create(user=other_user, recipe=recipe)

        self.assertEqual(recipe.like_count, 1)


class LikeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jack', password='testpass123')
        self.other_user = User.objects.create_user(username='nadia', password='testpass123')
        self.recipe = Recipe.objects.create(
            user=self.user,
            name='Curry',
            url='https://example.com/curry',
            category='dinner'
        )

    def test_like_creation(self):
        like = Like.objects.create(user=self.other_user, recipe=self.recipe)

        self.assertEqual(like.user.username, 'nadia')
        self.assertEqual(like.recipe.name, 'Curry')

    def test_like_str(self):
        like = Like.objects.create(user=self.other_user, recipe=self.recipe)

        self.assertEqual(str(like), 'nadia likes Curry')

    def test_user_can_only_like_recipe_once(self):
        Like.objects.create(user=self.other_user, recipe=self.recipe)

        with self.assertRaises(Exception):
            Like.objects.create(user=self.other_user, recipe=self.recipe)


class PopulationScriptTest(TestCase):
    def test_create_user_creates_user_and_profile(self):
        user = create_user('zach', 'Password123!')

        self.assertTrue(User.objects.filter(username='zach').exists())
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_create_recipe_creates_recipe(self):
        user = User.objects.create_user(username='hafsa', password='testpass123')

        recipe = create_recipe(
            user=user,
            name='Bagel',
            url='https://example.com/bagel',
            category='lunch',
            image='recipe_images/bagel.jpg'
        )

        self.assertEqual(recipe.name, 'Bagel')
        self.assertEqual(recipe.category, 'lunch')
        self.assertEqual(recipe.user.username, 'hafsa')

    def test_create_like_creates_like(self):
        user1 = User.objects.create_user(username='jack', password='testpass123')
        user2 = User.objects.create_user(username='hugh', password='testpass123')

        recipe = Recipe.objects.create(
            user=user1,
            name='Pancakes',
            url='https://example.com/pancakes',
            category='breakfast'
        )

        like = create_like(user2, recipe)

        self.assertEqual(like.user.username, 'hugh')
        self.assertEqual(like.recipe.name, 'Pancakes')
        self.assertEqual(recipe.like_count, 1)

# HOME PAGE TESTS
class HomePageFeatureTest(TestCase):

    def test_homepage_contains_hero_image(self):
        response = self.client.get(reverse('reciperate:home'))

        # Check image path is in HTML
        self.assertContains(response, 'images/hero-food.jpg')

    def test_homepage_image_tag_exists(self):
        response = self.client.get(reverse('reciperate:home'))

        # Check actual <img> tag exists
        self.assertContains(response, '<img')

    def test_get_started_button_links_to_signup(self):
        response = self.client.get(reverse('reciperate:home'))

        signup_url = reverse('reciperate:sign_up')

        # Check button contains correct link
        self.assertContains(response, f'href="{signup_url}"')

    def test_get_started_button_text_exists(self):
        response = self.client.get(reverse('reciperate:home'))

        self.assertContains(response, 'Get Started')

    def test_get_started_button_redirects_correctly(self):
        signup_url = reverse('reciperate:sign_up')

        response = self.client.get(signup_url)

        # Just checks the page loads (status 200)
        self.assertEqual(response.status_code, 200)
