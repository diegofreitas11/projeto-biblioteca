# Generated by Django 2.1.5 on 2019-03-19 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0004_emprestimo'),
    ]

    operations = [
        migrations.AddField(
            model_name='emprestimo',
            name='status',
            field=models.CharField(default=34, max_length=11),
            preserve_default=False,
        ),
    ]