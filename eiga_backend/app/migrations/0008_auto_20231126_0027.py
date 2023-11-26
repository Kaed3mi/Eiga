# Generated by Django 3.2 on 2023-11-25 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20231126_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bangumi',
            name='bangumi_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='blog_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='character',
            name='character_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='id'),
        ),
    ]