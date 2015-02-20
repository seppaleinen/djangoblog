# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('git_branch', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'database_branch',
                'verbose_name_plural': 'branch_list',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('git_directory', models.CharField(max_length=100)),
                ('git_shortname', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'database_directory',
                'verbose_name_plural': 'directory_list',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'user_info',
                'verbose_name_plural': 'user_info_list',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('workspace', models.CharField(max_length=100)),
                ('user_info', models.ForeignKey(to='blog.UserInfo')),
            ],
            options={
                'db_table': 'workspace',
                'verbose_name_plural': 'workspace_list',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='directory',
            name='workspace',
            field=models.ForeignKey(to='blog.Workspace'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='branch',
            name='directory',
            field=models.ForeignKey(to='blog.Directory'),
            preserve_default=True,
        ),
    ]
