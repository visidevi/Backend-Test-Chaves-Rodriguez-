# Generated by Django 3.0.8 on 2022-02-19 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('channel', models.CharField(max_length=50, unique=True)),
                ('tz', models.CharField(max_length=50)),
                ('deleted', models.BooleanField(default=False)),
                ('ordered_menus', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]