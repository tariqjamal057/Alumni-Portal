from django.contrib import admin

from portal.models import Batch, Country, Department, District, ExperienceDetail, MentorPost, MentorPostResponse, MentorResponseMessage, Post, Post_Education_Detail, PostResponse, ResponseMessage, State, Tag, User,Authentication

# Register your models here.

admin.site.register(User)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(District)
admin.site.register(Batch)
admin.site.register(Department)
admin.site.register(Post_Education_Detail)
admin.site.register(ExperienceDetail)
admin.site.register(Post)
admin.site.register(PostResponse)
admin.site.register(ResponseMessage)
admin.site.register(MentorPost)
admin.site.register(MentorPostResponse)
admin.site.register(MentorResponseMessage)
admin.site.register(Tag) 
admin.site.register(Authentication)