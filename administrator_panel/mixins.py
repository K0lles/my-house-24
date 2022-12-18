from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView


class DirectorUserPassesTestMixin(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_anonymous:
            return False

        string_permission = getattr(self, 'string_permission', None)
        if not string_permission:
            raise AttributeError(f"String permission is not indicated in {self.__class__.__name__}")

        return getattr(self.request.user.role, string_permission, False)


class PermissionListView(DirectorUserPassesTestMixin, ListView):

    def forbidden_page(self):
        self.template_name = 'forbidden_page.html'
        self.object_list = None
        context = super().get_context_data()
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return self.forbidden_page()
        return super().dispatch(request, *args, **kwargs)


class PermissionCreateView(DirectorUserPassesTestMixin, CreateView):

    def forbidden_page(self):
        self.template_name = 'forbidden_page.html'
        self.object = None
        context = super().get_context_data()
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return self.forbidden_page()
        return super().dispatch(request, *args, **kwargs)


class PermissionDetailView(DirectorUserPassesTestMixin, DetailView):

    def forbidden_page(self):
        self.template_name = 'forbidden_page.html'
        self.object = None
        context = super().get_context_data()
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return self.forbidden_page()
        return super().dispatch(request, *args, **kwargs)


class PermissionUpdateView(DirectorUserPassesTestMixin, UpdateView):

    def forbidden_page(self):
        self.template_name = 'forbidden_page.html'
        self.object = None
        context = super().get_context_data()
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return self.forbidden_page()
        return super().dispatch(request, *args, **kwargs)


class PermissionDeleteView(DirectorUserPassesTestMixin, DeleteView):

    def forbidden_page(self):
        self.template_name = 'forbidden_page.html'
        self.object = None
        context = super().get_context_data()
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return self.forbidden_page()
        return super().dispatch(request, *args, **kwargs)
