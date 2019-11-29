# Generated by Django 2.2.1 on 2019-11-29 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=60, null=True, verbose_name='图片名称')),
                ('image', models.ImageField(blank=True, null=True, upload_to='avatar/%Y%m%d/', verbose_name='图片')),
            ],
            options={
                'verbose_name': '图片列表',
                'verbose_name_plural': '图片列表',
            },
        ),
    ]
