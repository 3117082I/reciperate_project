from django.test import TestCase
from django.urls import reverse
from .models import Recipe, Like, UserProfile
from .forms import RecipeForm
from django.contrib.auth.models import User
from django.conf import settings
import importlib
class ViewTests(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('reciperate_app.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('reciperate_app.urls')

    def test_home_exists(self):
        self.check_if_view_exists('home')

    def test_breakfast_exists(self):
        self.check_if_view_exists('breakfast')

    def test_lunch_exists(self):
        self.check_if_view_exists('lunch')

    def test_dinner_exists(self):
        self.check_if_view_exists('dinner')

    def test_sign_in_exists(self):
        self.check_if_view_exists('sign_in')

    def test_sign_up_exists(self):
        self.check_if_view_exists('sign_up')

    def test_add_recipe_exists(self):
        self.check_if_view_exists('add_recipe')

    def check_if_view_exists(self, view):
        name_exists = view in self.views_module_listing
        is_callable = callable(self.views_module.home)

        self.assertTrue(name_exists)
        self.assertTrue(is_callable)


class NavBarTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", password="test123"
        )

    def test_navbar_anonymous(self):
        response = self.client.get(reverse("reciperate:home"))
        self.check_common_links_on_nav_bar(response)
        self.assertContains(response, 'href = "/reciperate/sign-in/"')
        self.assertContains(response, 'href = "/reciperate/sign-up/"')

    def test_navbar_logged_in(self):
        self.client.login(username="test", password="test123")
        response = self.client.get(reverse("reciperate:home"))
        self.check_common_links_on_nav_bar(response)
        self.assertContains(response, 'href = "/reciperate/add-recipe/"')
        self.assertContains(response, 'href = "/reciperate/sign-out/"')

    def check_common_links_on_nav_bar(self, response):
        self.assertContains(response, 'href = "/reciperate/home/')
        self.assertContains(response, 'href = "/reciperate/breakfast/"')
        self.assertContains(response, 'href = "/reciperate/lunch/"')
        self.assertContains(response, 'href = "/reciperate/dinner/"')

class LikeButtonTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", password="test123"
        )

        self.secondUser = User.objects.create_user(
            username="secondtest", password="test321"
        )
        self.recipe = Recipe.objects.create(
            user=self.user,
            name="Pancakes",
            url="www.test.com",
            category="breakfast",
            image="recipe_images/default.jpg"
        )

        self.like_url = reverse(
            "reciperate:like_recipe",
            kwargs={"category": self.recipe.category, "recipe_id": self.recipe.id}
        )

    def test_like_button_unavailable_logged_out(self):
        #button should not show if not logged in
        response = self.client.get(reverse("reciperate:breakfast"))
        self.assertNotContains(response, 'Like</button>')

    def test_like_button_available_logged_in(self):
        #button should  show if not logged in
        self.client.login(username="test", password="test123")
        response = self.client.get(reverse("reciperate:breakfast"))

        self.assertContains(response, 'Like</button>')

    def test_like_button_text_changes_on_like(self):
        self.client.login(username="test", password="test123")
        response = self.client.get(reverse("reciperate:breakfast"))
        unpressed_like_button_text_check = 'Like</button>' in response.content.decode()

        self.client.post(self.like_url)
        response = self.client.get(reverse("reciperate:breakfast"))
        pressed_like_button_text_check = 'Liked</button>' in response.content.decode()

        self.assertTrue(unpressed_like_button_text_check and pressed_like_button_text_check)

    def test_like_post(self):
        #liking should create a new database record and return like as true
        self.client.login(username="test", password="test123")

        response = self.client.post(self.like_url)
        data = response.json()

        self.assertTrue(data["liked"])
        self.assertEqual(data["like_count"], 1)
        self.assertEqual(Like.objects.count(), 1)
        self.assertTrue(Like.objects.filter(user=self.user, recipe=self.recipe).exists())

    def test_dislike_post(self):
        #disliking should delete previous database record and return like as false
        self.client.login(username="test", password="test123")

        #like it
        self.client.post(self.like_url)

        #unlike it
        response = self.client.delete(self.like_url)
        data = response.json()

        self.assertFalse(data["liked"])
        self.assertEqual(data["like_count"], 0)
        self.assertEqual(Like.objects.count(), 0)
        self.assertFalse(Like.objects.filter(user=self.user, recipe=self.recipe).exists())

    def test_multiple_users_liking(self):
        self.client.login(username="test", password="test123")
        self.client.post(self.like_url)
        self.client.logout()

        self.client.login(username="secondtest", password="test321")
        self.client.post(self.like_url)

        self.assertEqual(Like.objects.count(), 2)
        self.assertTrue(Like.objects.filter(user=self.user, recipe=self.recipe).exists())
        self.assertTrue(Like.objects.filter(user=self.secondUser, recipe=self.recipe).exists())

    def test_one_user_like_one_user_dislike(self):
        self.client.login(username="test", password="test123")
        self.client.post(self.like_url)
        self.client.logout()

        self.client.login(username="secondtest", password="test321")
        self.client.post(self.like_url)
        self.client.delete(self.like_url)

        self.assertEqual(Like.objects.count(), 1)
        self.assertTrue(Like.objects.filter(user=self.user, recipe=self.recipe).exists())
        self.assertFalse(Like.objects.filter(user=self.secondUser, recipe=self.recipe).exists())

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

class TemplateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='username',
            password='password123'
        )
        self.recipe = Recipe.objects.create(
            user=self.user,
            name="Test Recipe",
            url="https://example.com",
            category="breakfast",
        )
        Like.objects.create(user=self.user, recipe=self.recipe)
    def test_navbar_logged_out_displays (self):
        response = self.client.get(reverse('reciperate:home'))
        self.assertContains(response, "Home")
        self.assertContains(response, "Breakfast")
        self.assertContains(response, "Lunch")
        self.assertContains(response, "Dinner")
        self.assertContains(response, "Sign in")
        self.assertContains(response, "Sign up")
        self.assertNotContains(response, "Add a recipe")
        self.assertNotContains(response, "Sign Out")
    def test_navbar_logged_in_displays(self):
        self.client.login(username='username', password='password123')
        response = self.client.get(reverse('reciperate:home'))

        self.assertContains(response, "Add a recipe")
        self.assertContains(response, "Sign Out")
        self.assertNotContains(response, "Sign in")
        self.assertNotContains(response, "Sign up")

    def test_category_template_used(self):
        response = self.client.get(reverse('reciperate:breakfast'))
        self.assertTemplateUsed(response, 'reciperate_app/category.html')

    def test_category_displays_recipe(self):
        response = self.client.get(reverse('reciperate:breakfast'))

        self.assertContains(response, "Test Recipe")
        self.assertContains(response, "https://example.com")
        self.assertContains(response, "1 Likes")

    def test_category_sort_dropdown_exists(self):
        response = self.client.get(reverse('reciperate:breakfast'))

        self.assertContains(response, "Popular")
        self.assertContains(response, "Newest")
        self.assertContains(response, "Oldest")
        self.assertContains(response, "A-Z")

    def test_like_button_hidden_when_logged_out(self):
        response = self.client.get(reverse('reciperate:breakfast'))
        self.assertNotContains(response, 'class="like_button"')

    def test_like_button_visible_when_logged_in(self):
        self.client.login(username='username', password='password123')
        response = self.client.get(reverse('reciperate:breakfast'))

        self.assertContains(response, 'class="like_button"')

    def test_breakfast_page_heading(self):
        response = self.client.get(reverse('reciperate:breakfast'))

        self.assertContains(response, "<h1>Breakfast</h1>", html=True)

    def test_breakfast_inherits_category(self):
        response = self.client.get(reverse('reciperate:breakfast'))

        # Content from category template
        self.assertContains(response, "Click below to sort")

    def test_lunch_page_heading(self):
        response = self.client.get(reverse('reciperate:lunch'))

        self.assertContains(response, "<h1>Lunch</h1>", html=True)

    def test_dinner_page_heading(self):
        response = self.client.get(reverse('reciperate:dinner'))

        self.assertContains(response, "<h1>Dinner</h1>", html=True)

    def test_add_recipe_link_hidden_logged_out(self):
        response = self.client.get(reverse('reciperate:home'))
        self.assertNotContains(response, "Add a recipe")

    def test_add_recipe_link_visible_logged_in(self):
        self.client.login(username='username', password='password123')
        response = self.client.get(reverse('reciperate:home'))
        self.assertContains(response, "Add a recipe")

    def test_sign_in_page_accessible(self):
        response = self.client.get(reverse('reciperate:sign_in'))
        self.assertEqual(response.status_code, 200)

    def test_sign_up_page_accessible(self):
        response = self.client.get(reverse('reciperate:sign_up'))
        self.assertEqual(response.status_code, 200)

class CSSTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='usernametest',
            password='password123'
        )
        self.recipe = Recipe.objects.create(
            user=self.user,
            name="Test Recipe",
            url="https://example.com",
            category="breakfast",
        )
        Like.objects.create(user=self.user, recipe=self.recipe)

    def test_css_file_loaded(self):
        response = self.client.get(reverse('reciperate:home'))

        self.assertContains(
            response,
            "css/styles.css"
        )
    def test_navbar_class_present(self):
        response = self.client.get(reverse('reciperate:home'))

        self.assertContains(response, 'class="navbar"')

    def test_nav_links_present(self):
        response = self.client.get(reverse('reciperate:home'))

        self.assertContains(response, "Home")
        self.assertContains(response, "Breakfast")
        self.assertContains(response, "Lunch")
        self.assertContains(response, "Dinner")

    def test_recipe_card_class_present(self):
        response = self.client.get(reverse('reciperate:breakfast'))

        self.assertContains(response, 'class="recipe_card"')

    def test_like_section_class_present(self):
        response = self.client.get(reverse('reciperate:breakfast'))

        self.assertContains(response, 'class="like_section"')

    def test_home_header_class(self):
        response = self.client.get(reverse('reciperate:home'))

        self.assertContains(response, "homeHeader")

    def test_category_header_class(self):
        response = self.client.get(reverse('reciperate:breakfast'))
        self.assertContains(response, "categoryHeader")

    def test_form_classes_present(self):
        response = self.client.get(reverse('reciperate:sign_in'))

        self.assertContains(response, "form_group")

    def test_select_wrapper_present(self):
        response = self.client.get(reverse('reciperate:breakfast'))

        self.assertContains(response, "select-wrapper")

    def test_select_element_present(self):
        response = self.client.get(reverse('reciperate:breakfast'))

        self.assertContains(response, "<select", html=False)

    def test_viewport_responsive_meta(self):
        response = self.client.get(reverse('reciperate:home'))

        self.assertContains(response, "viewport")