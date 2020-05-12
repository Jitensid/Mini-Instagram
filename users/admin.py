from django.contrib import admin
from .models import Profile
from .models import Following
from .models import Follower
# Register your models here.

admin.site.register(Profile)
admin.site.register(Following)
admin.site.register(Follower)
