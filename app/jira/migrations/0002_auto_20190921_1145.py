# Generated by Django 2.2.5 on 2019-09-21 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
        ('jira', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jiraissue',
            name='project',
        ),
        migrations.AddField(
            model_name='jiraissue',
            name='jira_project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='jira.JiraProject'),
        ),
        migrations.AddField(
            model_name='jiraproject',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='dashboard.Project'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jiraissue',
            name='created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jiraissue',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='jiraissue',
            name='duedate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jiraissue',
            name='environment',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='jiraissue',
            name='summary',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]