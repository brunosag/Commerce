# Generated by Django 4.0.5 on 2022-07-13 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_category_icon_alter_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='url_name',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]
