# Generated by Django 5.0.6 on 2024-11-29 01:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0013_remove_unitprogress_quiz_score_quizattempt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='knowledge.knowledgenode'),
        ),
    ]
