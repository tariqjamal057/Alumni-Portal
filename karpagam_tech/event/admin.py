from django.contrib import admin

from event.models import Event, Faq, Feedback, Media, Partner, Prize, Speaker, Student, Theme


admin.site.site_header = 'Karpagam Institute of Technology'
admin.site.site_title  = 'Admin Panel'
admin.site.index_title = ''



class StudentModel(admin.ModelAdmin):
    list_display = (
        'name' , 'rollno' , 'regno' , 'degree'  , 'specialization', 'phoneno')
class EventModel(admin.ModelAdmin):
    list_display = ('id' , 'name' , 'poster' , 'venue' , 'fees'  , 'description', )
class SpeakerModel(admin.ModelAdmin):
    list_display = ('id' , 'name', 'image' , 'designation' , 'about')
class PartnerModel(admin.ModelAdmin):
    list_display = ('id', 'image')
class MediaModel(admin.ModelAdmin):
    list_display = ('id', 'gallery')

admin.site.register(Student , StudentModel)
admin.site.register(Event,EventModel)
admin.site.register(Speaker , SpeakerModel)
admin.site.register(Partner , PartnerModel)
admin.site.register(Media , MediaModel)
admin.site.register(Theme )
admin.site.register(Prize )
admin.site.register(Faq )
admin.site.register(Feedback )
