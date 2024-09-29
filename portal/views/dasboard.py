from django.shortcuts import redirect
from django.views import View

from portal.utils import is_alumni, is_faculty, is_student


class DashboardView(View):
    def get(self, request):
        if is_faculty(request.user):
            return redirect("faculty-dashboard")
        elif is_alumni(request.user):
            return redirect("dashboard.alumni")
        elif is_student(request.user):
            return redirect("student-dashboard")
        else:
            return redirect("page404")
