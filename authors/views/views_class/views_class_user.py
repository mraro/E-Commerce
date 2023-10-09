from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.edit import BaseCreateView, ProcessFormView
from django.utils.translation import gettext_lazy as _  # TRANSLATE as _

from authors.forms import RegisterForm, LoginForm
from base_class.view_base import Base_Global_Objects


class Register_View(FormView, Base_Global_Objects):
    form_class = RegisterForm
    template_name = 'pages/register_view.html'

    def get_context_data(self, **kwargs):
        session_data = self.request.session.get('register_form_data')
        # self.form_class = RegisterForm(session_data)
        context = super().get_context_data(**kwargs)
        context.update({
            'form': RegisterForm(session_data),
            'form_action': reverse('authors:register_create'),
            'form_button': _('Register'),
            'nameSite': self.store_name,
            'current_cart': self.get_full_cart(request=self.request),

        })
        return context


class Register_Create(BaseCreateView, Base_Global_Objects):
    def get(self, *args):
        raise Http404()

    def post(self, request, *args, **kwargs):
        POST = request.POST  # Receive data by POST
        request.session['register_form_data'] = POST  # Give data from POST to SESSION
        form = RegisterForm(POST)

        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(user.password)
                user.save()
                messages.success(request, _("User registered successfully!!!"))
                del (request.session['register_form_data'])  # kill session
                return redirect('store:home')
            except ValueError:
                messages.error(request, _("Fail in create user"))
                return redirect('authors:register')

        return redirect('authors:register')


class Login_View(FormView, Base_Global_Objects):
    form_class = LoginForm
    template_name = 'pages/login_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_action': reverse('authors:authenticate'),
            'form_button': 'Login',
            'nameSite': self.store_name,
            'current_cart': self.get_full_cart(request=self.request),

        })
        return context


class Login_Authenticate(ProcessFormView):

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        POST = request.POST  # Recive data by POST
        # print("\n ", POST, "\n")
        form = LoginForm(POST)

        if form.is_valid():
            user_authenticate = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
            )

            if user_authenticate is not None:
                login(request, user_authenticate)
                messages.success(request, _("Success on Login!"))
                return redirect(reverse('store:home'))

            else:
                messages.error(request, _('User and/or password wrong'))
                return redirect(reverse('authors:login'))

        messages.error(request, _('fill the fields properly'))
        return redirect(reverse('authors:login'))


class Logout_Backend(LogoutView):
    http_method_names = ['post', ]
    get = Http404

    def post(self, request, *args, **kwargs):
        if request.POST.get('username') != request.user.username:
            return redirect(reverse('authors:login'))
        see_you = _('See you')
        logout(request)
        if request.POST.get('first_name'):
            messages.success(request, f"{see_you} {request.POST.get('first_name')}")
        else:
            messages.success(request, f"{see_you} {request.POST.get('username')}")

        return redirect(reverse('store:home'))
