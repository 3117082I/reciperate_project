from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe, Like, UserProfile

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


   # def test_recipe_grid_class_present(self):
        #response = self.client.get(reverse('reciperate:breakfast'))

        #self.assertContains(response, 'class="recipe_grid"')

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

    #def test_like_button_class_present_when_logged_in(self):
        #self.client.login(username='username', password='password123')

        #response = self.client.get(reverse('reciperate:breakfast'))

        #self.assertContains(response, 'class="like_button"')

    def test_viewport_responsive_meta(self):
        response = self.client.get(reverse('reciperate:home'))

        self.assertContains(response, "viewport")



