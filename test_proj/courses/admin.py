
# Register your models here.
from django.contrib import admin

from .models import Node,Course,Person

admin.site.register(Person)
admin.site.register(Course)
admin.site.register(Node)

