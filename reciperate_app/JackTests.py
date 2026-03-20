from django.test import TestCase
from django.contrib.auth.models import User
from reciperate_app.models import Recipe, UserProfile, Like
from population_script import create_user, create_recipe, create_like
from django.urls import reverse

# Create your tests here.
