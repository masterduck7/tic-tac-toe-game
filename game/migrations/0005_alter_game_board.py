# Generated by Django 4.2.7 on 2023-11-10 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_alter_game_board_alter_usergame_character_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='board',
            field=models.TextField(blank=None, default='[["","",""],["","",""],["","",""]]'),
        ),
    ]