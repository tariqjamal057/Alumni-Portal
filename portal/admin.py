from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from portal.models import *
from django.contrib.auth.hashers import make_password

admin.site.site_header = 'Karpagam Institute of Technology'
admin.site.site_title = 'Admin'
admin.site.index_title = ''


class AdminConfig(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','username','email','registered_on']

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(form.cleaned_data.get('password'))
            # obj.car.confirm =_('approved')
            # obj.car.save()
        super().save_model(request, obj, form, change) 
      
admin.site.register(User,AdminConfig)

class CountryConfig(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','name']

admin.site.register(Country,CountryConfig)

class StateConfig(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','name']

admin.site.register(State,StateConfig)

class DistrictConfig(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','name','state']

admin.site.register(District,DistrictConfig)

class BatchConfig(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','entry_year','passed_out']
admin.site.register(Batch,BatchConfig)

class DepartmentConfig(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','short_name','name']

admin.site.register(Department,DepartmentConfig)

class PostEducationDetailConfig(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','user','degree','institute_or_university','currently_pursing']

admin.site.register(PostEducationDetail,PostEducationDetailConfig)

class ExperienceDetailConfig(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','user','designation','organization','currently_working_here']

admin.site.register(ExperienceDetail,ExperienceDetailConfig)

class PostConfig(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','title','posted_by','date']
admin.site.register(Post,PostConfig)

class PostResponseConfig(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','user','post']

admin.site.register(PostResponse,PostResponseConfig)

class ResponseMessageConfig(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','user','post_response','message','date']

admin.site.register(ResponseMessage,ResponseMessageConfig)

class Tech_Help_PostConfig(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','title','stack','posted_by','date']

admin.site.register(Tech_Help_Post,Tech_Help_PostConfig)

class Tech_Help_PostResponseConfig(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','user','post']

admin.site.register(Tech_Help_PostResponse,Tech_Help_PostResponseConfig)

class Tech_Help_ResponseMessageConfig(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','user','post_response','message','date']

admin.site.register(Tech_Help_ResponseMessage,Tech_Help_ResponseMessageConfig)

admin.site.register(Featured_Mentor)

class Finance_request_Config(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','title','name','year','department','posted_by']
admin.site.register(Finance_request,Finance_request_Config)

class Finance_request_Post_Response_Config(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','post','user']
admin.site.register(Finance_request_Post_Response,Finance_request_Post_Response_Config)

class Finance_request_Response_Message_Config(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','user','post_response','message','date']
admin.site.register(Finance_request_Response_Message,Finance_request_Response_Message_Config)

# class Featured_Sponser_config(ImportExportModelAdmin,admin.ModelAdmin):
#     list_display = ['id','student_name','user','amount','date']

admin.site.register(Featured_Sponser)
