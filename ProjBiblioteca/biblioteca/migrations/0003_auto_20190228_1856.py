# Generated by Django 2.1.5 on 2019-02-28 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0002_auto_20190225_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aluno',
            name='id',
        ),
        migrations.AlterField(
            model_name='aluno',
            name='matricula',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
