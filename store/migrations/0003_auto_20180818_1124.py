# Generated by Django 2.1 on 2018-08-18 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20180817_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='logo',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]