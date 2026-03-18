from django.test import TestCase
from django.urls import reverse
from .models import Recipe, Like, UserProfile
from django.contrib.auth.models import User

class NavBarTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", password="test123"
        )

    def test_navbar_anonymous(self):
        response = self.client.get(reverse("reciperate:home"))
        self.assertContains(response, 'href = "/reciperate/home/')
        self.assertContains(response, 'href = "/reciperate/breakfast/"')
        self.assertContains(response, 'href = "/reciperate/lunch/"')
        self.assertContains(response, 'href = "/reciperate/dinner/"')
        self.assertContains(response, 'href = "/reciperate/sign-in/"')
        self.assertContains(response, 'href = "/reciperate/sign-up/"')


    def test_navbar_logged_in(self):
        self.client.login(username="test", password="test123")
        response = self.client.get(reverse("reciperate:home"))
        self.assertContains(response, 'href = "/reciperate/home/')
        self.assertContains(response, 'href = "/reciperate/breakfast/"')
        self.assertContains(response, 'href = "/reciperate/lunch/"')
        self.assertContains(response, 'href = "/reciperate/dinner/"')
        self.assertContains(response, 'href = "/reciperate/add-recipe/"')
        self.assertContains(response, 'href = "/reciperate/sign-out/"')


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
