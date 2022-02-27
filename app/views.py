from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from helpers.Mixins import AuthenticateMixin, UserContextMixin
from helpers.services import connect_user_registration, error_handler, connect_get_user, connect_login_api, \
    connect_create_room_api, connect_room_api, connect_room_messages, connect_update_chat
from .forms import *


class RegisterView(generic.FormView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm

    def get_success_url(self):
        return reverse('login')

    def form_valid(self, form):
        params = {
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'email': form.cleaned_data['email'],
            'username': form.cleaned_data['username'],
            'password': form.cleaned_data['password'],
        }

        conn = connect_user_registration(self.request, params)

        if not conn['success']:
            # API return false then return form_invalid
            error_handler(self.request, conn['data'])
            return super().form_invalid(form)

        else:
            messages.success(self.request, "Account Created Successfully.")

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LoginView(generic.FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        """ Intercept dispatch to check if there is active session"""
        try:
            """ Check if there is an active session """
            conn = connect_get_user(self.request)

            if conn['success']:
                return redirect('dashboard')

            else:
                raise Exception('Please, login to continue')

        except Exception as err:
            try:
                del request.session['session_token']
                messages.error(request, '%s' % err)

            except KeyError:
                pass

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        params = {
            'username': form.cleaned_data['username'],
            'password': form.cleaned_data['password']
        }
        conn = connect_login_api(self.request, params)

        if conn['success']:

            self.request.session['session_token'] = conn['data']['access']

        else:
            error_handler(self.request, conn['data'])

            return super().form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dashboard')


class DashboardView(AuthenticateMixin, UserContextMixin, generic.FormView):
    template_name = 'accounts/dashboard.html'
    form_class = ChatRoomForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['rooms'] = connect_room_api(self.request, context['user'][0]['id'])
        return context

    def form_valid(self, form):
        params = {
            'title': form.cleaned_data['title'],
        }
        conn = connect_create_room_api(self.request, params)

        if not conn['success']:
            error_handler(self.request, conn['data'])
            return super().form_invalid(form)
        messages.success(self.request, "Chat Room created successfully")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dashboard')


class ChatRoomView(AuthenticateMixin, UserContextMixin, TemplateView):
    template_name = 'app/chat.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['room_name'] = self.kwargs.get('title')
        context['chats'] = connect_room_messages(self.request, context['room_name'])
        return context

@csrf_exempt
def update_chat(request, message_id):
    if request.method == 'POST':
        response = connect_update_chat(request, message_id)
        if response['success']:
            return JsonResponse(data={"msg":"Chat updated successfully"}, status=200)
        else:
            return JsonResponse(data={"error": "Chat not updated successfully"}, status=400)
    else:
        return JsonResponse(data={"error": "Method not allowed"}, status=405)


def logout(request):
    session_keys = list(request.session.keys())

    for key in session_keys:
        del request.session[key]

    return redirect(reverse('login'))


def error_404(request, exception):
    return render(request, 'error_pages/404.html')


def error_500(request):
    return render(request, 'error_pages/500.html')


def error_403(request, exception):
    return render(request, 'error_pages/403.html')
