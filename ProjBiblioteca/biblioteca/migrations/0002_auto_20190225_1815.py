# Generated by Django 2.1.5 on 2019-02-25 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Usuarios',
            new_name='Aluno',
        ),
    ]