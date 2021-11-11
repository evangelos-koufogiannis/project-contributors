from rest_framework.serializers import ModelSerializer, CharField

from accounts.models import User, Skill


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'age', 'country', 'residence', 'username', 'password')


class UserProjectOwnerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class UserProjectCollaboratorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class SkillSerializer(ModelSerializer):

    programming_language = CharField(source='get_programming_language_display')
    level = CharField(source='get_level_display')

    class Meta:
        model = Skill
        fields = ('programming_language', 'level')

class SkillWithUserSerializer(SkillSerializer):

    email = CharField(source='user.email')

    class Meta:
        model = Skill
        fields = ('email', 'programming_language', 'level')