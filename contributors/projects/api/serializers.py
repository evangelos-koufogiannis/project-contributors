from rest_framework.serializers import ModelSerializer, RelatedField

from accounts.api.serializers import UserSerializer, UserProjectOwnerSerializer, UserProjectCollaboratorSerializer
from projects.models import Project


class ProjectSerializer(ModelSerializer):
    # created_by = UserProjectOwnerSerializer(read_only=True)
    created_by = RelatedField(source='email', read_only=True)
    collaborators = UserProjectCollaboratorSerializer(source='email', read_only=True, many=True)

    class Meta:
        model = Project
        # fields = ('name', 'description', 'created_by', 'maximum_collaborators')
        fields = ('name', 'description', 'created_by', 'collaborators', 'maximum_collaborators')
