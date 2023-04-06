# Generated by Django 4.0.9 on 2023-02-14 07:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_person_alter_publisher_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='age',
        ),
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.EmailField(default='', max_length=254, verbose_name='邮箱'),
        ),
        migrations.AddField(
            model_name='person',
            name='login_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='登录时间'),
        ),
        migrations.AddField(
            model_name='person',
            name='text',
            field=models.TextField(default='', verbose_name='内容'),
        ),
        migrations.AddField(
            model_name='person',
            name='url',
            field=models.URLField(blank=True, verbose_name='个人地址'),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=50, verbose_name='姓名'),
        ),
    ]
