from django.views.generic import TemplateView


class PageNotFoundView(TemplateView):
    template_name = "not_found_page.html"


class InternalServerError(TemplateView):
    template_name = 'internal_error_page.html'
