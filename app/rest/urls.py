from django.urls import include, path
from rest_framework import routers
from .views import (
    UserViewSet, GroupViewSet,
    CustomerViewSet, ProjectViewSet,
    JiraStatusViewSet, JiraPriorityViewSet, JiraIssueTypeViewSet,
    JiraUserViewSet, JiraProjectViewSet, JiraIssueViewSet
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'projects', ProjectViewSet)


jira_router = routers.DefaultRouter()
jira_router.register(r'statuses', JiraStatusViewSet)
jira_router.register(r'priorities', JiraPriorityViewSet)
jira_router.register(r'issuetypes', JiraIssueTypeViewSet)
jira_router.register(r'users', JiraUserViewSet)
jira_router.register(r'projects', JiraProjectViewSet)
jira_router.register(r'issues', JiraIssueViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('jira/', include(jira_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
