import os
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


FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

def create_user_object():
    user = User.objects.get_or_create(username='testuser')[0]
    user.set_password('testabc123')
    user.save()
    return user

class SignUpTests(TestCase):
    def test_sign_up_url_exists(self):
        url = ''
        try:
            url = reverse('reciperate:sign_up')
        except:
            pass

        self.assertEqual(url, '/reciperate/sign-up/',
                         f"{FAILURE_HEADER}Have you created the reciperate:sign_up URL mapping correctly? It should point to the sign_up() view, and have a URL of '/reciperate/sign-up/'.{FAILURE_FOOTER}")

    def test_sign_up_page_loads(self):
        response = self.client.get(reverse('reciperate:sign_up'))
        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}The sign up page did not load correctly. Check your sign_up() view and URL mapping.{FAILURE_FOOTER}")

    def test_sign_up_uses_template(self):
        response = self.client.get(reverse('reciperate:sign_up'))
        self.assertTemplateUsed(response, 'reciperate_app/sign_up.html',
                                f"{FAILURE_HEADER}The sign_up() view does not use the expected sign_up.html template.{FAILURE_FOOTER}")

    def test_sign_up_form_present(self):
        response = self.client.get(reverse('reciperate:sign_up'))
        content = response.content.decode()
        self.assertTrue('name="username"' in content,
                        f"{FAILURE_HEADER}We couldn't find the username field in the sign up form. Check your sign_up.html template.{FAILURE_FOOTER}")
        self.assertTrue('name="password"' in content,
                        f"{FAILURE_HEADER}We couldn't find the password field in the sign up form. Check your sign_up.html template.{FAILURE_FOOTER}")
        self.assertTrue('type="submit"' in content,
                        f"{FAILURE_HEADER}We couldn't find the submit button in the sign up form. Check your sign_up.html template.{FAILURE_FOOTER}")


    def test_sign_up_creates_user(self):
        self.client.post(reverse('reciperate:sign_up'), {
            'username': 'newuser',
            'password': 'newpassword123'
        })

        users = User.objects.filter(username='newuser')
        self.assertEqual(len(users), 1,
                         f"{FAILURE_HEADER}When signing up with valid credentials, a new User object was not created in the database. Check your sign_up() view.{FAILURE_FOOTER}")

    def test_sign_up_redirects_to_sign_in(self):
        response = self.client.post(reverse('reciperate:sign_up'), {
            'username': 'newuser',
            'password': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302,
                         f"{FAILURE_HEADER}After a successful sign up, we expected a redirect but did not get one. Check your sign_up() view.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('reciperate:sign_in'),
                         f"{FAILURE_HEADER}After a successful sign up, we were not redirected to the sign in page. Check your sign_up() view.{FAILURE_FOOTER}")

    def test_sign_up_bad_post_response(self):
        response = self.client.post(reverse('reciperate:sign_up'), {})
        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}When submitting a blank sign up form, we expected a HTTP 200 response (redisplaying the form with errors), but did not get one.{FAILURE_FOOTER}")

class SignInTests(TestCase):
    def test_sign_in_url_exists(self):
        url = ''
        try:
            url = reverse('reciperate:sign_in')
        except:
            pass
        self.assertEqual(url, '/reciperate/sign-in/',
                         f"{FAILURE_HEADER}Have you created the reciperate:sign_in URL mapping correctly? It should point to the sign_in() view, and have a URL of '/reciperate/sign-in/'.{FAILURE_FOOTER}")

    def test_sign_in_page_loads(self):
        response = self.client.get(reverse('reciperate:sign_in'))
        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}The sign in page did not load correctly. Check your sign_in() view and URL mapping.{FAILURE_FOOTER}")

    def test_sign_in_uses_template(self):
        response = self.client.get(reverse('reciperate:sign_in'))
        self.assertTemplateUsed(response, 'reciperate_app/sign_in.html',
                                f"{FAILURE_HEADER}The sign_in() view does not use the expected sign_in.html template.{FAILURE_FOOTER}")

    def test_sign_in_form_present(self):
        response = self.client.get(reverse('reciperate:sign_in'))
        content = response.content.decode()
        self.assertTrue('name="username"' in content,
                        f"{FAILURE_HEADER}We couldn't find the username field in the sign in form. Check your sign_in.html template.{FAILURE_FOOTER}")
        self.assertTrue('name="password"' in content,
                        f"{FAILURE_HEADER}We couldn't find the password field in the sign in form. Check your sign_in.html template.{FAILURE_FOOTER}")
        self.assertTrue('type="submit"' in content,
                        f"{FAILURE_HEADER}We couldn't find the submit button in the sign in form. Check your sign_in.html template.{FAILURE_FOOTER}")

    def test_sign_in_functionality(self):
        user_object = create_user_object()

        response = self.client.post(reverse('reciperate:sign_in'), {
            'username': 'testuser',
            'password': 'testabc123'
        })

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your sign_in() view.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log in with your sign_in() view, it didn't seem to log the user in. Please check your sign_in() view implementation, and try again.{FAILURE_FOOTER}")

        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Logging in was successful, but we expected a redirect. We got a status code of {response.status_code} instead. Check your sign_in() view.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('reciperate:home'), f"{FAILURE_HEADER}We were not redirected to the Reciperate homepage after signing in. Please check your sign_in() view.{FAILURE_FOOTER}")

    def test_sign_in_invalid_credentials(self):
        response = self.client.post(reverse('reciperate:sign_in'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })

        self.assertTrue('_auth_user_id' not in self.client.session,
                        f"{FAILURE_HEADER}When signing in with invalid credentials, a user was logged in when they should not have been. Check your sign_in() view.{FAILURE_FOOTER}")



class SignOutTests(TestCase):
    def test_sign_out_url_exists(self):
        url = ''
        try:
            url = reverse('reciperate:sign_out')
        except:
            pass
        self.assertEqual(url, '/reciperate/sign-out/',
                         f"{FAILURE_HEADER}Have you created the reciperate:sign_out URL mapping correctly? It should point to the sign_out() view, and have a URL of '/reciperate/sign-out/'.{FAILURE_FOOTER}")

    def test_sign_out_when_not_logged_in(self):
        response = self.client.get(reverse('reciperate:sign_out'))
        self.assertEqual(response.status_code, 302,
                         f"{FAILURE_HEADER}When attempting to sign out without being logged in, we expected a redirect but did not get one. Check your sign_out() view.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('reciperate:home'),
                         f"{FAILURE_HEADER}When signing out without being logged in, we were not redirected to the homepage. Check your sign_out() view.{FAILURE_FOOTER}")

    def test_sign_out_when_logged_in(self):
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']),
                             f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your sign_out() view.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False,
                            f"{FAILURE_HEADER}When attempting to log a user in to test sign out, it failed. Please check your sign_in() view and try again.{FAILURE_FOOTER}")

        response = self.client.get(reverse('reciperate:sign_out'))
        self.assertEqual(response.status_code, 302,
                         f"{FAILURE_HEADER}Signing out should cause a redirect, but this failed to happen. Please check your sign_out() view.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('reciperate:home'),
                         f"{FAILURE_HEADER}When signing out, we were not redirected to the Reciperate homepage. Please check your sign_out() view.{FAILURE_FOOTER}")
        self.assertTrue('_auth_user_id' not in self.client.session,
                        f"{FAILURE_HEADER}Signing out with your sign_out() view didn't actually log the user out! Please check your sign_out() view.{FAILURE_FOOTER}")


class NavbarAuthTests(TestCase):
    def test_logged_out_links(self):
        content = self.client.get(reverse('reciperate:home')).content.decode()

        self.assertTrue('reciperate/sign-in/' in content,
                        f"{FAILURE_HEADER}The Sign In link was not present in the navbar when the user was not logged in. Check your base.html template.{FAILURE_FOOTER}")
        self.assertTrue('reciperate/sign-up/' in content,
                        f"{FAILURE_HEADER}The Sign Up link was not present in the navbar when the user was not logged in. Check your base.html template.{FAILURE_FOOTER}")
        self.assertTrue('reciperate/sign-out/' not in content,
                        f"{FAILURE_HEADER}The Sign Out link was present in the navbar when the user was not logged in. It should not be. Check your base.html template.{FAILURE_FOOTER}")

    def test_logged_in_links(self):
        create_user_object()
        self.client.login(username='testuser', password='testabc123')
        content = self.client.get(reverse('reciperate:home')).content.decode()

        self.assertTrue('reciperate/sign-out/' in content,
                        f"{FAILURE_HEADER}The Sign Out link was not present in the navbar when the user was logged in. Check your base.html template.{FAILURE_FOOTER}")
        self.assertTrue('reciperate/sign-in/' not in content,
                        f"{FAILURE_HEADER}The Sign In link was present in the navbar when the user was logged in. It should not be. Check your base.html template.{FAILURE_FOOTER}")
        self.assertTrue('reciperate/sign-up/' not in content,
                        f"{FAILURE_HEADER}The Sign Up link was present in the navbar when the user was logged in. It should not be. Check your base.html template.{FAILURE_FOOTER}")