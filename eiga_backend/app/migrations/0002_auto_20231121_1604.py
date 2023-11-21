# Generated by Django 3.2 on 2023-11-21 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='user_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.CharField(blank=True, default='default', max_length=60, null=True, verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='bangumi',
            name='bangumi_score',
            field=models.FloatField(blank=True, null=True, verbose_name='评分'),
        ),
        migrations.AlterField(
            model_name='bangumi',
            name='rank',
            field=models.IntegerField(blank=True, null=True, verbose_name='排名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='permission',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='权限'),
        ),
    ]