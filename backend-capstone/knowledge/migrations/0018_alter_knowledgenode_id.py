# Generated by Django 5.0.6 on 2024-11-29 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0017_alter_question_node'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knowledgenode',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
