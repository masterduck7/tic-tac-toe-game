from django.contrib import admin

from .models import Game, User, UserGame

admin.site.register(User)
admin.site.register(Game)
admin.site.register(UserGame)
