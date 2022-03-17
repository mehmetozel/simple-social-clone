from django.db import models
from django.utils.text import slugify #slugify allows us to remove any characters that alphanumaric or underscores or hyphens.
                                      # If you have a string that has spaces in it and you want to use that as part of the URL , it is gonna be avle to lowercase and add dashes instead of spaces.
from django.urls import reverse
from django.conf import settings
# Create your models here.

from django.contrib.auth import get_user_model # returns the user model that's currently active in this project
User = get_user_model()

import misaka
#???? that allows us to do link and bedding


from django import template
register = template.Library()  #this is how we can user custom template tags in the future

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True) #allow_unicode means that SlugField, now accepts unicode characters instead of just ASCII characters.
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)   #group form doldurulup save edildiginde name ne girildiyse onun arasına "-"ler koyup slug olarak kaydeder.
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']     #When the objects of this model are retrieved, they will be present in this ordering.



class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models. CASCADE)
    user = models.ForeignKey(User, related_name='user_groups',on_delete=models. CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')


