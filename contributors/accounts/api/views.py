from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE, HTTP_409_CONFLICT
)

from accounts.api.serializers import UserSerializer, SkillSerializer, SkillWithUserSerializer
from projects.api.serializers import ProjectSerializer
from accounts.models import User, Skill
from projects.models import Project


# # # USER RELATED APIVIEWS # # #
class UserAuthenticationMixIn(object):

    def get_object(self):
        user = authenticate(email=self.request.POST.get('email'), password=self.request.POST.get('password'))
        if not user:
            raise PermissionDenied
        else:
            return user


class CreateUserAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=HTTP_201_CREATED)


class ResetUserPasswordAPIView(GenericAPIView):
    queryset = User
    lookup = 'email'

    def post(self, request):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        new_password = request.POST.get('new_password', None)

        if password and new_password:
            user = authenticate(email=email, password=str(password))
            if user:
                user.set_and_save_password(str(new_password))
            else:
                raise PermissionDenied
        else:
            new_password = get_object_or_404(self.get_queryset(), **{self.lookup: email}).set_and_save_random_password()
            send_mail(
                'Contributors: Forgotten password reset',
                'You new automaticaly generated password is: {}. Please change it asap!'.format(new_password),
                'contributors@cp.com',
                [email],
                fail_silently=False,
            )

        return Response(status=HTTP_202_ACCEPTED)


class AddUserSkillAPIView(UserAuthenticationMixIn, CreateAPIView):
    serializer_class = SkillSerializer

    def post(self, request):
        user = self.get_object()
        if Skill.objects.can_add_skill(user):
            try:
                Skill.objects.create(user=user,
                                     programming_language=self.request.POST.get('programming_language'),
                                     level=self.request.POST.get('level'),
                                     )
                status = HTTP_201_CREATED
                data = None
            except IntegrityError:
                status = HTTP_409_CONFLICT
                data = {"error": "You have already registered this skill (programming language)."}
        else:
            status = HTTP_400_BAD_REQUEST
            data = {"error": "User can not add more than 3 skills (programming language)."}
        return Response(data=data, status=status)


class RemoveUserSkillAPIView(UserAuthenticationMixIn, DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        try:
            Skill.objects.filter(user=self.get_object(),
                                 programming_language=self.request.POST.get('programming_language')).delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except Skill.DoesNotExist:
            return Response(data={"error": "User skill not found."}, status=HTTP_404_NOT_FOUND)


# # # PROJECT RELATED APIVIEWS # # #
class CreateProjectAPIView(UserAuthenticationMixIn, CreateAPIView):

    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        # Handle cace where user defines mode collaborators that the max_collaborators parameter by removing extra ones
        collaborators = User.objects.filter(email__in=self.request.POST.get('collaborator_emails', '').replace(" ", "").split(","))
        maximum_collaborators = int(self.request.POST.get('maximum_collaborators'))
        instance = serializer.save(created_by=self.get_object(), collaborators=collaborators[:maximum_collaborators])
        # Mark the project as closed in case collaborators.count reached maximum_collaborators from project definition
        if instance.collaborators.count() == instance.maximum_collaborators:
            instance.is_open = False
            instance.save()

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=HTTP_201_CREATED)


class CompleteProjectAPIView(UserAuthenticationMixIn, CreateAPIView):

    def post(self, request):
        user = self.get_object()
        try:
            Project.objects.mark_as_completed(name=request.POST.get('name'),
                                              creator=user,
                                              )
            return Response(status=HTTP_201_CREATED)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)


class DeleteProjectAPIView(UserAuthenticationMixIn, CreateAPIView):

    def post(self, request):
        user = self.get_object()
        try:
            Project.objects.mark_as_deleted(name=request.POST.get('name'),
                                            creator=user,
                                            )
            return Response(status=HTTP_201_CREATED)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)


class AcceptCollaboratorAPIView(UserAuthenticationMixIn, CreateAPIView):

    def post(self, request):
        user = self.get_object()
        try:
            accept_status = Project.objects.accept_candidate_collaborator({'created_by': user, 'name': request.POST.get('project_name')},
                                                request.POST.get('candidate_collaborator_email'),
                                                )
            if accept_status:
                return Response(status=HTTP_201_CREATED)
            else:
                return JsonResponse(data={"error": "Project is not open. Can't accept user as collaborator."},
                                    status=HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)


class DeclineCollaboratorAPIView(UserAuthenticationMixIn, CreateAPIView):

    def post(self, request):
        user = self.get_object()
        try:
            Project.objects.decline_candidate_collaborator({'created_by': user, 'name': request.POST.get('project_name')},
                                                request.POST.get('candidate_collaborator_email'),
                                                )
            return Response(status=HTTP_201_CREATED)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)


class LookForProjectCollaboratorsAPIView(UserAuthenticationMixIn, ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillWithUserSerializer

    def post(self, request):
        # self.queryset = self.queryset.filter(programming_language__in=[0,1,2,3], level__in=[1]) ### Needs numbers in order to implement filtering on choice field
        return self.get(self, request) # ListApiView Provides only a get method but we need a post for user authentication security reasons


class CandidateSkillsListAPIView(UserAuthenticationMixIn, ListAPIView):

    def post(self, request):
        return Response(SkillSerializer(Skill.objects.filter(user=self.get_object()), many=True).data)


class CandidateSkillsListAPIView(UserAuthenticationMixIn, ListAPIView):

    def post(self, request):
        return Response(SkillSerializer(Skill.objects.filter(user=self.get_object()), many=True).data)


class ProjectCandidatesAPIView(UserAuthenticationMixIn, CreateAPIView):
    project_lookup = 'project_name'

    def post(self, request):
        user = self.get_object()
        candidates = {}
        for candidate in Project.objects.list_candidate_collaborators({'created_by': user, 'name': request.POST.get(self.project_lookup)}):
            candidates.update({candidate.username: {'email': candidate.email,
                               'skills': SkillSerializer(Skill.objects.filter(user=candidate), many=True).data,
                               }})

        return JsonResponse(data=candidates, status=HTTP_200_OK)


class OpenProjectsListAPIView(UserAuthenticationMixIn, ListAPIView):
    queryset = Project.objects.filter(is_open=True, status=Project.ACTIVE_STATUS_CODE)
    serializer_class = ProjectSerializer

    def post(self, request):
        return self.get(self, request) # ListApiView Provides only a get method but we need a post for user authentication security reasons


class ExpressInterestToProjectAPIView(UserAuthenticationMixIn, CreateAPIView):
    project_lookup = 'project_name'

    def post(self, request):
        user = self.get_object()
        project_of_interest = Project.objects.get(name=request.POST.get(self.project_lookup))
        if project_of_interest.is_open and user.pk != project_of_interest.created_by.pk:
            project_of_interest.candidate_collaborators.add(user)
            return Response(status=HTTP_202_ACCEPTED)
        elif project_of_interest.is_open:
            return Response(data={'error': "Project creator can not be the same with the one that expresses interest."},
                            status=HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(data={'error': "Project of interest is closed. It does not accept requests of interest."},
                            status=HTTP_406_NOT_ACCEPTABLE)


class UserStatisticsAPIView(UserAuthenticationMixIn, CreateAPIView):

    def post(self, request):
        user = self.get_object()
        return JsonResponse(data={
            'statistics': {
                'skills_count': Skill.objects.filter(user=user).count(),
                'projects_created': Project.objects.created_by_user_count(user),
                'projects_contributed': Project.objects.collaborators_count(user)
            }
        },
            status=HTTP_200_OK)
