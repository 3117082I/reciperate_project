from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    @property
    def like_count(self):
        return self.liked_by.count()

    def __str__(self):
        return self.name