# Generated by Django 2.2.1 on 2019-12-16 00:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kpi', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpiinput',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='input_user', to=settings.AUTH_USER_MODEL, verbose_name='录入人'),
        ),
        migrations.AddField(
            model_name='groupkpi',
            name='dep',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Organization', verbose_name='所属部门'),
        ),
        migrations.AddField(
            model_name='groupkpi',
            name='kpi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_kpi', to='kpi.KPI', verbose_name='KPI'),
        ),
    ]
