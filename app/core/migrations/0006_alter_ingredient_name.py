# Generated by Django 3.2.25 on 2024-07-26 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_ingredient_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]