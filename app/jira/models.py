from django.db import models
from app.dashboard.models import Customer
from django.contrib.auth.models import User
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE


class JiraStatus(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    jira_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)


class JiraPriority(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    jira_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)


class JiraIssueType(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    jira_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    subtask = models.BooleanField(default=False)


class JiraUser(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    displayName = models.CharField(max_length=200)
    emailAddress = models.CharField(max_length=200)
    key = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class JiraProject(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=200)
    description = models.TextField(
        max_length=512, verbose_name="Description", blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    jira_id = models.CharField(max_length=200)
    jira_key = models.CharField(max_length=200, unique=True)
    statuses = models.ManyToManyField(JiraStatus)
    priorities = models.ManyToManyField(JiraPriority)
    jira_users = models.ManyToManyField(JiraUser)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.name, self.customer)


class JiraIssue(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    jira_id = models.CharField(max_length=200)
    jira_key = models.CharField(max_length=200, unique=True)
    summary = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    environment = models.CharField(max_length=200, null=True)
    duedate = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True)
    created = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True)
    assignee = models.ForeignKey(JiraUser, on_delete=models.PROTECT)
    creator = models.ForeignKey(JiraUser, on_delete=models.PROTECT)
    status = models.ForeignKey(JiraStatus, on_delete=models.PROTECT)
    priority = models.ForeignKey(JiraPriority, on_delete=models.PROTECT)
    issuetype = models.ForeignKey(JiraIssueType, on_delete=models.PROTECT)
    project = models.ForeignKey(JiraProject, on_delete=models.PROTECT)

    def __str__(self):
        return '%s - %s' % (self.key, self.project.name)
