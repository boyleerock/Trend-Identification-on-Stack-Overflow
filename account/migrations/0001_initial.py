# Generated by Django 2.2.20 on 2021-06-02 04:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dir', models.CharField(max_length=255, verbose_name='文件地址')),
                ('status', models.CharField(default=1, max_length=1, verbose_name='status')),
                ('tag', models.CharField(default=1, max_length=1, verbose_name='tag')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户文件',
                'verbose_name_plural': '用户文件',
                'ordering': ('-create_at',),
            },
        ),
    ]