from django.contrib import admin
from .models import JiraStatus, JiraPriority, JiraIssueType, JiraUser
from .models import JiraProject, JiraIssue

admin.site.register(JiraStatus)
admin.site.register(JiraPriority)
admin.site.register(JiraIssueType)
admin.site.register(JiraUser)
admin.site.register(JiraProject)
admin.site.register(JiraIssue)
