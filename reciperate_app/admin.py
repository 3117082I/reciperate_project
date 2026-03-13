from django.contrib import admin
from .models import Recipe
from .models import UserProfile
from .models import Like
# Register your models here.

admin.site.register(Recipe)
admin.site.register(UserProfile)
admin.site.register(Like)