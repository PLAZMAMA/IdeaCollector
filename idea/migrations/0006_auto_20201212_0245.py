# Generated by Django 3.1.3 on 2020-12-12 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0005_auto_20201116_0234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ideamodel',
            name='description',
            field=models.TextField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='ideamodel',
            name='title',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
