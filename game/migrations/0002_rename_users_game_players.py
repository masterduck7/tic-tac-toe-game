# Generated by Django 4.2.7 on 2023-11-09 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='users',
            new_name='players',
        ),
    ]
