import random

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    pass

    # def create_user(self, username, email, password):
    #     user = self.model (username=username, email=self.normaize_email(email))
    #     user.set_password(password)
    #     user.save()

    # def reset_user_password(self):
    #     return self.set_password(self.make_random_password(length=16))


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    age = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=100)
    residence = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'age', 'country', 'residence', 'username', 'password']

    objects = UserManager()

    def set_and_save_random_password(self):
        new_random_password = ''.join([random.choice('1234567890qwertyuiopasdfghjklzxcvbnm') for i in range(16)])
        self.set_password(new_random_password)
        self.save()
        return new_random_password

    def set_and_save_password(self, raw_password):
        self.set_password(raw_password)
        self.save()


class SkillManager(models.Manager):

    def can_add_skill(self, user):
        return True if self.model.objects.filter(user=user).count() < 3 else False


class Skill(models.Model):
    PROGRAMMING_LANGUAGE_CHOICES = [
        (0, 'C++'),
        (1, 'Javascript'),
        (2, 'Python'),
        (3, 'Java'),
        (4, 'Lua'),
        (5, 'Rust'),
        (6, 'Go'),
        (7, 'Julia'),
    ]
    LEVEL_CHOICES = [
        (0, 'beginner'),
        (1, 'experienced'),
        (2, 'expert'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
    )

    programming_language = models.PositiveSmallIntegerField(
        choices=PROGRAMMING_LANGUAGE_CHOICES,
        db_index=True,
    )
    level = models.PositiveSmallIntegerField(
        choices=LEVEL_CHOICES,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SkillManager()

    class Meta:
        unique_together = ("user", "programming_language")
