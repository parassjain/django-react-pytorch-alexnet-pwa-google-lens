# Generated by Django 3.2.4 on 2021-06-11 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_post_pytorch_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image_url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]