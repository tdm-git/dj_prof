# Generated by Django 3.2.7 on 2021-09-28 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lange',
            field=models.CharField(default='RUS', max_length=3),
        ),
    ]
