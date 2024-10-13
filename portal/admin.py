from django.contrib import admin
from django.contrib.auth.hashers import make_password
from import_export.admin import ImportExportModelAdmin

from portal.models import *

admin.site.site_header = "College of Engineering and Technology"
admin.site.site_title = "Admin"
admin.site.index_title = ""


class BaseAdminConfig(ImportExportModelAdmin, admin.ModelAdmin):
    """"""


class BaseAdminConfigWithListDisplay(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name"]


class BaseAdminConfigWithTitle(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "title"]


class AdminConfig(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "username", "email", "registered_on", "is_active"]

    def save_model(self, request, obj, form, change):
        if "password" in form.changed_data:
            obj.password = make_password(form.cleaned_data.get("password"))

        super().save_model(request, obj, form, change)


admin.site.register(User, AdminConfig)


class BatchConfig(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "entry_year", "passed_out"]


admin.site.register(Batch, BatchConfig)

admin.site.register(Degree, BaseAdminConfigWithListDisplay)

admin.site.register(DegreeSpecialization, BaseAdminConfigWithListDisplay)

admin.site.register(Department, BaseAdminConfigWithListDisplay)

admin.site.register(FinanceRequest, BaseAdminConfigWithTitle)

admin.site.register(FinanceRequestComment)

admin.site.register(FinanceRequestInterest)


admin.site.register(FinanceRequestInterestMessage)

admin.site.register(FinanceRequestSponser)

admin.site.register(GaleryCategory)

admin.site.register(GalleryImage)

admin.site.register(Image)

admin.site.register(PostType)

admin.site.register(HelpDesk, BaseAdminConfigWithTitle)

admin.site.register(HelpDeskComment)

admin.site.register(HelpDeskInterest)

admin.site.register(HelpDeskInterestMessage)

admin.site.register(Tag)

admin.site.register(TechHelpPost, BaseAdminConfigWithTitle)

admin.site.register(TechHelpPostComment)

admin.site.register(TechHelpPostInterest)

admin.site.register(TechHelpPostInterestMessage)

admin.site.register(Country, BaseAdminConfigWithListDisplay)

admin.site.register(State, BaseAdminConfigWithListDisplay)

admin.site.register(District, BaseAdminConfigWithListDisplay)

admin.site.register(PostEducationDetail)

admin.site.register(Experience)
