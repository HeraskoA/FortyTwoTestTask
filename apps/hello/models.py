from django.db import models
from PIL import Image
import StringIO
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile
from apps.hello.validators import (valid_name, valid_skype,
                                   valid_jabber, valid_birthday)


class UserData(models.Model):
    first_name = models.CharField(
        max_length=256,
        blank=False,
        validators=[valid_name]
    )
    last_name = models.CharField(
        max_length=256,
        blank=False,
        validators=[valid_name]
    )
    date_of_birth = models.DateField(
        blank=False,
        null=True,
        validators=[valid_birthday]
    )
    bio = models.TextField(max_length=256, blank=False)
    email = models.EmailField(max_length=40, blank=False)
    jabber = models.CharField(
        max_length=40,
        blank=False,
        validators=[valid_jabber]
    )
    skype = models.CharField(
        max_length=40,
        blank=False,
        validators=[valid_skype]
    )
    other_contacts = models.TextField(max_length=256, blank=False)
    photo = models.ImageField(upload_to='photos', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.photo:
            image = Image.open(StringIO.StringIO(self.photo.read()))
            image.thumbnail((200, 200), Image.ANTIALIAS)
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.photo = InMemoryUploadedFile(
                output,
                'ImageField',
                "%s.jpg" % self.photo.name.split('.')[0],
                'image/jpeg',
                output.len,
                None
            )
        super(UserData, self).save(*args, **kwargs)


class Request(models.Model):
    path = models.CharField(max_length=60, blank=True)
    method = models.CharField(max_length=60, blank=True)
    time = models.TimeField(blank=True, auto_now=True)
    priority = models.PositiveSmallIntegerField(default=1)


class ActionHistory(models.Model):
    object_type = models.CharField(max_length=256)
    object_id = models.IntegerField()
    action = models.CharField(max_length=10)


@receiver(post_save)
def save(sender, instance=None, created=None, **kwargs):
    if sender.__name__ not in ['ActionHistory',
                               'Session',
                               'ContentType',
                               'MigrationHistory']:
        if not created:
            action = 'update'
        else:
            action = 'created'
        objects_id = instance.id
        ActionHistory.objects.create(object_type=sender.__name__,
                                     object_id=objects_id,
                                     action=action
                                     )
    return


@receiver(pre_delete)
def deleted(sender, instance=None, **kwargs):
    if sender.__name__ not in ['ActionHistory',
                               'Session',
                               'ContentType',
                               'MigrationHistory']:
        objects_id = instance.id
        ActionHistory.objects.create(object_type=sender.__name__,
                                     object_id=objects_id,
                                     action='deleted'
                                     )
    return
