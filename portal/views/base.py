from portal.utils import is_alumni


class BasePublicContext:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_alumni"] = is_alumni(self.request.user)
        return context
