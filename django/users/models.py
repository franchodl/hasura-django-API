from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Role(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


def get_user_role():
    return Role.objects.get_or_create(name="user")[0]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, default=get_user_role)

    def __str__(self):
        return f"{self.user} - {self.role}"


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
