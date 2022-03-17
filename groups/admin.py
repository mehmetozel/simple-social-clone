from django.contrib import admin
from . import models


# Register your models here.

class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember




admin.site.register(models.Group)

# tabular inline class allows us to utilize the admin interface
# and our django website with the ability to edit models
# on the same page as the parent model


