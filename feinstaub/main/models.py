from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel


class UserProfile(TimeStampedModel):
    NOTIFICATION_TYPE_CHOICES = (('none', 'no notification'),
                                 ('email', 'email'),
                                 ('pushover', 'pushover'),
                                 ('notifymyandroid', 'notifymyandroid'),)

    user = models.OneToOneField(User, related_name='profile')
    notification_type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE_CHOICES)
    pushover_clientkey = models.CharField(max_length=100, default='', blank=True)
    notifymyandroid_apikey = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return str(self.user)
