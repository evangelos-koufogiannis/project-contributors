from django.db import models

from accounts.models import User


class ProjectManager(models.Manager):

    def create_project(self,
                       name: str,
                       description: str,
                       creator: User,
                       maximum_collaborators: int,
                       collaborators=None):
        new_project = self.model(name=name,
                                 description=description,
                                 created_by=creator,
                                 maximum_collaborators=maximum_collaborators)
        new_project.save()
        if collaborators: new_project.collaborators.add(*collaborators)

    def mark_as_completed(self, filter_dict):
        # Use filter_dict in order to give the option to filter with pk or name field
        self.model.objects.filter(**filter_dict).update(status=self.model.COMPLETED_STATUS_CODE)

    def mark_as_deleted(self, filter_dict):
        self.model.objects.filter(**filter_dict).update(status=self.model.DELETED_STATUS_CODE)

    def accept_candidate_collaborator(self, filter_dict, user):
        accept_status = False
        project = self.model.objects.filter(**filter_dict)
        if project.is_open:
            project.candidate_collaborators.remove(user)
            project.collaborators.add(user)
            accept_status = True
            if project.collaborators.count() == project.maximum_collaborators:
                project.is_open = False  # Flag the project as closed when collaborators.count reached maximum_collaborators
        return accept_status

    def decline_candidate_collaborator(self, filter_dict, user):
        self.model.objects.filter(**filter_dict).candidate_collaborators.remove(user)

    def list_candidate_collaborators(self, filter_dict):
        return self.model.objects.get(**filter_dict).candidate_collaborators.all()

    def created_by_user_count(self, creator):
        return self.model.objects.filter(created_by=creator).count()

    def collaborators_count(self, creator):
        return self.model.objects.filter(collaborators=creator).count()


class Project(models.Model):
    DELETED_STATUS_CODE = 0
    ACTIVE_STATUS_CODE = 1
    COMPLETED_STATUS_CODE = 2
    STATUS_CHOICES = [
        (DELETED_STATUS_CODE, 'deleted'),
        (ACTIVE_STATUS_CODE, 'active'),
        (COMPLETED_STATUS_CODE, 'completed'),
    ]
    name = models.CharField(max_length=150, unique=True, db_index=True)
    description = models.TextField()
    # programing_languages_in_use =
    maximum_collaborators = models.PositiveSmallIntegerField()
    collaborators = models.ManyToManyField(User, blank=True, related_name='collaborators')  # The ones accepted by the project creator for collaboration
    candidate_collaborators = models.ManyToManyField(User, blank=True, related_name='candidate_collaborators')  # The ones awaiting acceptance or declaration by the collaborator
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_by',
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=ACTIVE_STATUS_CODE,
        db_index=True,
    )
    is_open = models.BooleanField(default=True) # Flag to define if project is open (Project is consider closer when collaborators.count = max_collaborators)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProjectManager()
