from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(District)
admin.site.register(Batch)
admin.site.register(Department)
admin.site.register(Post_Education_Detail)
admin.site.register(Experience_Detail)