# Generated by Django 5.0.6 on 2024-11-25 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0006_alter_glossary_node_alter_question_node'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossary',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
