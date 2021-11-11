from django.urls import path

from accounts.api.views import *

app = 'accounts'

urlpatterns = [
    path('new-user/', CreateUserAPIView.as_view(), name="create-user-api-view"),
    path('user/password-reset/', ResetUserPasswordAPIView.as_view(), name="reset-user-password-api-view"),
    path('user/statistics/', UserStatisticsAPIView.as_view(), name="user-statistics-api-view"),
    path('user/list-open-projects/', OpenProjectsListAPIView.as_view(), name="user-list-open-projects-api-view"),
    path('user/look-for-collaborators/', LookForProjectCollaboratorsAPIView.as_view(), name="user-look-for-collaborators-api-view"),
    path('user/skill/list/', CandidateSkillsListAPIView.as_view(), name="add-user-skill-list-api-view"),  # Endpoint NOT required by the assignment
    path('user/skill/add/', AddUserSkillAPIView.as_view(), name="add-user-skill-api-view"),
    path('user/skill/remove/', RemoveUserSkillAPIView.as_view(), name="remove-user-skill-api-view"),
    path('user/project/create/', CreateProjectAPIView.as_view(), name="user-project-create-api-view"),
    path('user/project/complete/', CompleteProjectAPIView.as_view(), name="user-project-complete-api-view"),
    path('user/project/delete/', DeleteProjectAPIView.as_view(), name="user-project-delete-api-view"),
    path('user/project/collaborator/accept/', AcceptCollaboratorAPIView.as_view(), name="user-project-accept-colaborator-api-view"),
    path('user/project/collaborator/decline/', DeclineCollaboratorAPIView.as_view(), name="user-project-decline-colaborator-api-view"),
    path('user/project/candidates/', ProjectCandidatesAPIView.as_view(), name="project-candidates-api-view"),
    path('user/project/express-interest/', ExpressInterestToProjectAPIView.as_view(), name="project-express-interest-api-view"),
]