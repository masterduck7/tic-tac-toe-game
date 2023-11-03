from django.contrib import admin

from .models import Game, User

admin.site.register(User)
admin.site.register(Game)
