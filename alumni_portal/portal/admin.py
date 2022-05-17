from django.contrib import admin
from portal.models import *

admin.site.site_header = 'Karpagam Institute of Technology'
admin.site.site_title = 'Admin'
admin.site.index_title = ''

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

class Finance_request_Config(admin.ModelAdmin):
    list_display = ['title','student_name','year','department','posted_by']
admin.site.register(Finance_request,Finance_request_Config)

class Finance_request_Post_Response_Config(admin.ModelAdmin):
    list_display = ['post','user']
admin.site.register(Finance_request_Post_Response,Finance_request_Post_Response_Config)

class Finance_request_Response_Message_Config(admin.ModelAdmin):
    list_display = ['user','post_response','message','date']
admin.site.register(Finance_request_Response_Message,Finance_request_Response_Message_Config)

# class featured_Sponser_config(admin.ModelAdmin):
#     list_display = ['student_name','user','amount','date']

admin.site.register(featured_Sponser)
