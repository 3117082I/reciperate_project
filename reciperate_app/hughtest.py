import os
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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