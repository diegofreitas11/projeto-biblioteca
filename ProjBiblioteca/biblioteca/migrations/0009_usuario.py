# Generated by Django 2.1.5 on 2019-04-18 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0008_aluno_valor_debito'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=30)),
                ('login', models.CharField(max_length=10)),
                ('senha', models.CharField(max_length=10)),
            ],
        ),
    ]