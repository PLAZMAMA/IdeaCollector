# Generated by Django 3.1.2 on 2020-11-04 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0003_auto_20201015_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='picture',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
