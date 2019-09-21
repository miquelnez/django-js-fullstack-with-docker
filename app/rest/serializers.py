from django.contrib.auth.models import User, Group
from dashboard.models import Customer, Project
from jira.models import (
    JiraStatus, JiraPriority, JiraIssueType, JiraUser,
    JiraProject, JiraIssue
)
from rest_framework import serializers

''' django models '''


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


''' Dashboard models '''


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ['url', 'name', 'user']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['url', 'name', 'description', 'customer']


''' Jira models '''


class JiraStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JiraStatus
        fields = ['jira_id', 'name']


class JiraPrioritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JiraPriority
        fields = ['jira_id', 'name']


class JiraIssueTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JiraIssueType
        fields = ['jira_id', 'description', 'subtask']


class JiraUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JiraUser
        fields = ['url', 'displayName', 'emailAddress',
                  'key', 'name', 'active']


class JiraProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = JiraProject
        fields = ['url', 'name', 'description', 'customer', 'jira_id',
                  'jira_key', 'statuses', 'priorities', 'jira_users']


class JiraProjectSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = JiraProject
        fields = ['name', 'jira_id', 'jira_key']


class JiraIssueSerializer(serializers.ModelSerializer):

    status = JiraStatusSerializer(many=False)
    priority = JiraPrioritySerializer(many=False)
    issuetype = JiraIssueTypeSerializer(many=False)
    project = JiraProjectSmallSerializer(many=False)
    assignee = JiraUserSerializer(many=False)
    creator = JiraUserSerializer(many=False)

    class Meta:
        model = JiraIssue
        fields = ['url', 'jira_id', 'jira_key', 'summary', 'description',
                  'environment', 'duedate', 'created', 'assignee', 'creator',
                  'status', 'priority', 'issuetype', 'project']
