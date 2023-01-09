from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from administrator_panel.functions import owner_context_data


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
            if self.request.user.is_anonymous:
                return redirect('user-login')
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
            if self.request.user.is_anonymous:
                return redirect('user-login')
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
            if self.request.user.is_anonymous:
                return redirect('user-login')
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
            if self.request.user.is_anonymous:
                return redirect('user-login')
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
            if self.request.user.is_anonymous:
                return redirect('user-login')
            return self.forbidden_page()
        return super().dispatch(request, *args, **kwargs)


class PermissionView(DirectorUserPassesTestMixin, View):

    def forbidden_page(self):
        self.object = None
        self.name = getattr(self, 'name_view')
        if not self.name:
            raise AttributeError('Indicate name of view')
        return JsonResponse({'answer': f'Ви не маєте доступу до {self.name}'})

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return self.forbidden_page()
        return super().dispatch(request, *args, **kwargs)


class OwnerPermissionDetailView(DetailView):

    def forbidden_page(self):
        self.template_name = 'forbidden_page.html'
        self.object = None
        context = super().get_context_data()
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect('user-login')
        if not self.request.user.role.role == 'owner':
            return self.forbidden_page()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(owner_context_data(self.request.user))
        return context


class OwnerPermissionListView(ListView):

    def forbidden_page(self):
        self.template_name = 'forbidden_page.html'
        self.object = None
        context = super().get_context_data()
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect('user-login')
        if not self.request.user.role.role == 'owner':
            return self.forbidden_page()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update(owner_context_data(self.request.user))
        return context


class OwnerPermissionCreateView(CreateView):

    def forbidden_page(self):
        self.template_name = 'forbidden_page.html'
        self.object = None
        context = super().get_context_data()
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect('user-login')
        if not self.request.user.role.role == 'owner':
            return self.forbidden_page()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(owner_context_data(self.request.user))
        return context


class OwnerPermissionUpdateView(UpdateView):

    def forbidden_page(self):
        self.template_name = 'forbidden_page.html'
        self.object = None
        context = super().get_context_data()
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect('user-login')
        if not self.request.user.role.role == 'owner':
            return self.forbidden_page()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(owner_context_data(self.request.user))
        return context


class OwnerPermissionDeleteView(DeleteView):

    def forbidden_page(self):
        self.template_name = 'forbidden_page.html'
        self.object = None
        context = super().get_context_data()
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect('user-login')
        if not self.request.user.role.role == 'owner':
            return self.forbidden_page()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(owner_context_data(self.request.user))
        return context
