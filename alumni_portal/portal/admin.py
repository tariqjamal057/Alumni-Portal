from django.contrib import admin

from portal.models import Batch, Country, Department, District, ExperienceDetail, Tech_Help_Post, Tech_Help_PostResponse, Tech_Help_ResponseMessage, Post, PostEducationDetail, PostResponse, ResponseMessage, State, User,Finance_request,Finance

# Register your models here.

class AdminConfig(admin.ModelAdmin):
    list_display = ['username','email','registered_on']


admin.site.register(User,AdminConfig)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(District)
admin.site.register(Batch)
admin.site.register(Department)
admin.site.register(PostEducationDetail)
admin.site.register(ExperienceDetail)
admin.site.register(Post)
admin.site.register(PostResponse)
admin.site.register(ResponseMessage)
admin.site.register(Tech_Help_Post)
admin.site.register(Tech_Help_PostResponse)
admin.site.register(Tech_Help_ResponseMessage)
admin.site.register(Finance_request)
admin.site.register(Finance)