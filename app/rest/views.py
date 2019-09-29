from django.contrib.auth.models import User, Group
from todolist.models import TodoList, Todo
from dashboard.models import Customer, Project
from jira.models import (
    JiraStatus, JiraPriority, JiraIssueType, JiraUser,
    JiraProject, JiraIssue
)
from .serializers import (
    UserSerializer, GroupSerializer,
    CustomerSerializer, ProjectSerializer,
    JiraStatusSerializer, JiraPrioritySerializer, JiraIssueTypeSerializer,
    JiraUserSerializer, JiraProjectSerializer, JiraProjectFullSerializer,
    JiraIssueSerializer,
    TodoListFullSerializer, TodoSerializer
)
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import viewsets, mixins


''' django viewsets '''


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


''' todolist viewsets '''


class TodoListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TodoList to be viewed or edited.
    """
    queryset = TodoList.objects.all()
    serializer_class = TodoListFullSerializer


class TodoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Todo to be viewed or edited.
    """
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


''' dashboard viewsets '''


class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Customer to be viewed or edited.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Project to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


''' Jira viewsets '''


class JiraStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows JiraStatus to be viewed or edited.
    """
    queryset = JiraStatus.objects.all()
    serializer_class = JiraStatusSerializer


class JiraPriorityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows JiraPriority to be viewed or edited.
    """
    queryset = JiraPriority.objects.all()
    serializer_class = JiraPrioritySerializer


class JiraIssueTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows JiraIssueType to be viewed or edited.
    """
    queryset = JiraIssueType.objects.all()
    serializer_class = JiraIssueTypeSerializer


class JiraUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows JiraUser to be viewed or edited.
    """
    queryset = JiraUser.objects.all()
    serializer_class = JiraUserSerializer


class JiraProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows JiraProject to be viewed or edited.
    """
    queryset = JiraProject.objects.all()
    serializer_class = JiraProjectFullSerializer


class JiraIssueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows JiraIssue to be viewed or edited.
    """
    queryset = JiraIssue.objects.all()
    serializer_class = JiraIssueSerializer
