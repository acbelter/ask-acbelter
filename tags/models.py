from django.db import models


# Create your models here.
class Tag(models.Model):
    value = models.CharField(u'tag', unique=True, max_length=16)

    def __unicode__(self):
        return self.value
