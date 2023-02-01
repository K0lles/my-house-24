from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.views.generic.base import ContextMixin, TemplateResponseMixin

from administrator_panel.functions import owner_context_data
from configuration.models import User


class DirectorUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_anonymous:
            return False

        string_permission = getattr(self, 'string_permission', None)
        if not string_permission:
            raise AttributeError(f"String permission is not defined in {self.__class__.__name__}")

        return getattr(self.request.user.role, string_permission, False)


class BasePermissionView(DirectorUserPassesTestMixin, View):

    def forbidden_page(self):
        self.template_name = 'forbidden_page.html'
        self.object = None
        self.object_list = None
        context = self.get_context_data()
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):

        # if in cookies there is session_key of management user, we set self.request.user to it
        try:
            if self.request.COOKIES.get('management_session_key'):
                # get the Session model with saved in cookies session_key
                session_object_model = Session.objects.get(session_key=self.request.COOKIES.get('management_session_key'))

                # if Session object is valid and has data
                if session_object_model.get_decoded():
                    session = SessionStore(self.request.COOKIES.get('management_session_key'))

                    # get User's id for further getting it from database and setting to request data
                    user_id = session_object_model.get_decoded().get('_auth_user_id')
                    if user_id:
                        self.request.session = session
                        self.request.user = User.objects.get(pk=user_id)
        except (Session.DoesNotExist, KeyError, User.DoesNotExist):
            pass

        if not self.test_func():
            if self.request.user.is_anonymous \
                    or (self.request.user.is_authenticated and self.request.user.role.role == 'owner' \
                        and self.request.COOKIES.get('management_session_key') == 'None'):
                return redirect('user-staff-login')
            return self.forbidden_page()

        return super().dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response.set_cookie('sessionid', self.request.session.session_key, max_age=self.request.session.get_expiry_age())
        return response


class PermissionListView(BasePermissionView, ListView):
    pass


class PermissionCreateView(BasePermissionView, CreateView):
    pass


class PermissionDetailView(BasePermissionView, DetailView):
    pass


class PermissionUpdateView(BasePermissionView, UpdateView):
    pass


class PermissionDeleteView(BasePermissionView, DeleteView):
    pass


class PermissionView(BasePermissionView, View):

    def forbidden_page(self):
        self.object = None
        self.name = getattr(self, 'name_view')
        if not self.name:
            raise AttributeError('Define name of view')
        return JsonResponse({'answer': f'Ви не маєте доступу до {self.name}'})

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return self.forbidden_page()
        return super().dispatch(request, *args, **kwargs)


class OwnerBasePermissionView(TemplateResponseMixin, ContextMixin, View):
    """Base view class for classes which will work with owner-side part of website"""

    def forbidden_page(self):
        self.template_name = 'forbidden_page.html'
        self.object = None
        context = super().get_context_data()
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        # if in cookies there is session_key of management user, we set self.request.user to it
        try:
            if self.request.COOKIES.get('owner_session_key'):
                # get the Session model with saved in cookies session_key
                session_object_model = Session.objects.get(
                    session_key=self.request.COOKIES.get('owner_session_key'))

                # if Session object is valid and has data
                if session_object_model.get_decoded():
                    session = SessionStore(self.request.COOKIES.get('owner_session_key'))

                    # get User's id for further getting it from database and setting to request data
                    user_id = session_object_model.get_decoded().get('_auth_user_id')
                    if user_id:
                        self.request.session = session
                        self.request.user = User.objects.get(pk=user_id)
        except (Session.DoesNotExist, KeyError, User.DoesNotExist):
            pass

        if self.request.user.is_anonymous \
                or (self.request.user.is_authenticated and self.request.user.role != 'owner' \
                        and self.request.COOKIES.get('owner_session_key') == 'None'):
            return redirect('user-login')
        if self.request.user.role.role != 'owner':
            return self.forbidden_page()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(owner_context_data(self.request.user))
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response.set_cookie('sessionid', self.request.session.session_key,
                            max_age=self.request.session.get_expiry_age())
        return response


class OwnerPermissionDetailView(OwnerBasePermissionView, DetailView):
    pass


class OwnerPermissionListView(OwnerBasePermissionView, ListView):
    pass


class OwnerPermissionCreateView(OwnerBasePermissionView, CreateView):
    pass


class OwnerPermissionUpdateView(OwnerBasePermissionView, UpdateView):
    pass


class OwnerPermissionDeleteView(OwnerBasePermissionView, DeleteView):
    pass
