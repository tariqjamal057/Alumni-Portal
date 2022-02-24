from django.contrib import admin

from portal.models import Batch, Country, Department, District, Experience_Detail, Mentor_Post, Mentor_Post_Response, Mentor_Response_Message, Post, Post_Education_Detail, Post_Response, Response_Message, Sponser, State, Student_Support, Tag, User

# Register your models here.

admin.site.register(User)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(District)
admin.site.register(Batch)
admin.site.register(Department)
admin.site.register(Post_Education_Detail)
admin.site.register(Experience_Detail)
admin.site.register(Post)
admin.site.register(Post_Response)
admin.site.register(Response_Message)
admin.site.register(Mentor_Post)
admin.site.register(Mentor_Post_Response)
admin.site.register(Mentor_Response_Message)
admin.site.register(Student_Support)
admin.site.register(Sponser) 
admin.site.register(Tag) 