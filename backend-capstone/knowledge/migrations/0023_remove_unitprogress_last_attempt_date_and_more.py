# Generated by Django 5.0.6 on 2024-11-29 02:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0022_remove_quizresponse_quiz_attempt_and_more'),
        ('users', '0004_remove_student_email_remove_student_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unitprogress',
            name='last_attempt_date',
        ),
        migrations.RemoveField(
            model_name='unitprogress',
            name='quiz_attempts',
        ),
        migrations.RemoveField(
            model_name='unitprogress',
            name='quiz_score',
        ),
        migrations.CreateModel(
            name='QuizAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('passed', models.BooleanField()),
                ('attempt_date', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_attempts', to='users.student')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_attempts', to='knowledge.unit')),
            ],
        ),
        migrations.CreateModel(
            name='QuizResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_answer', models.TextField()),
                ('is_correct', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='knowledge.question')),
                ('quiz_attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='knowledge.quizattempt')),
            ],
        ),
    ]