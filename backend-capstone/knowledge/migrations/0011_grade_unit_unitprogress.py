# Generated by Django 5.0.6 on 2024-11-28 21:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0010_glossary_sentence_alter_glossary_gloss'),
        ('users', '0004_remove_student_email_remove_student_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='knowledge.grade')),
            ],
        ),
        migrations.CreateModel(
            name='UnitProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unlocked', models.BooleanField(default=False)),
                ('quiz_score', models.FloatField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_progress', to='users.student')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='knowledge.unit')),
            ],
        ),
    ]
