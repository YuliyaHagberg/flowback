# Generated by Django 4.0.8 on 2023-01-26 15:28

from django.db import migrations, models
import django.db.models.deletion

import flowback.comment.models
import flowback.comment.services


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
        ('poll', '0005_poll_comment_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='comment_section',
            field=models.ForeignKey(default=flowback.comment.models.comment_section_create, on_delete=django.db.models.deletion.DO_NOTHING, to='comment.commentsection'),
        ),
    ]
