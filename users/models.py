from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Member(AbstractUser):
    nick = models.CharField(u'nick', max_length=32)
    avatar = models.ImageField(u'avatar', upload_to='uploads/', blank=True, null=True, max_length=1000)
    rating = models.IntegerField(u'rating', default=0)

    def get_full_name(self):
        pass

    def get_short_name(self):
        pass
