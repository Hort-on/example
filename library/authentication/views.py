from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from authentication.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
from django.views.generic import ListView, DetailView

from django.core.validators import validate_email
from django.core.exceptions import ValidationError, PermissionDenied

from django.contrib.auth.password_validation import validate_password

from .forms import LoginForm, RegistrationForm, UpdateYourselfForm, UpdateUserForm


class IndexView(TemplateView):
    template_name = "authentication/index.html"


def auth_user(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, "authentication/login.html", {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Incorrect Login or Password')
        return render(request, 'authentication/login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            middle_name = form.cleaned_data['middle_name']
            last_name = form.cleaned_data['last_name']

            # Checking email and password for validation
            try:
                validate_email(email)
                validate_password(password)
            except ValidationError as error_message:
                form.add_error(None, error_message)
                return render(request, 'authentication/registration.html', {'form': form})

            # if email and password valid then trying to create the new User
            try:
                user = CustomUser.create(email=email, password=password,
                                         first_name=first_name, middle_name=middle_name, last_name=last_name)
                user.save()

            # if email not unique then return 'error_message': 'USER IS ALREADY EXIST'
            except IntegrityError:
                form.add_error(None, 'User with that email is already exist, please Log In')
                return render(request, 'authentication/registration.html', {'form': form})

            # if everything is good then redirect to login page
            return redirect('authentication:login')

    # if request.method != 'POST', just render template
    else:
        form = RegistrationForm()
        return render(request, 'authentication/registration.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


class AccountDetails(DetailView):
    model = CustomUser
    template_name = 'authentication/user_account.html'
    context_object_name = 'user_account'

    # Deny to access to another user
    def dispatch(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


@login_required
def update_yourself(request, pk):
    if request.method == 'POST' and request.user.id == pk:
        form = UpdateYourselfForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            middle_name = form.cleaned_data['middle_name']
            last_name = form.cleaned_data['last_name']

            try:
                user = CustomUser.get_by_id(pk)
            except CustomUser.DoesNotExist:
                return HttpResponse('User does not exists')

            user.update(first_name=first_name,
                        last_name=last_name,
                        middle_name=middle_name)
            return redirect('authentication:account', pk)
        else:
            return render(request, 'authentication/update_yourself.html', {'form': form})


class ListOfUsers(ListView):
    model = CustomUser
    template_name = 'authentication/users.html'
    context_object_name = 'users'
    ordering = 'created_at'

    # Get list without current admin
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(is_superuser=True).exclude(id=self.request.user.id)


class DetailsOfUser(DetailView):
    model = CustomUser
    template_name = 'authentication/details_user.html'
    context_object_name = 'user'


def update_user(request, pk):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            admin = CustomUser.objects.get(id=request.user.id)

            if admin.role == 1 or admin.is_superuser:
                user_to_update = CustomUser.objects.get(id=pk)
                user_to_update.is_active = form.cleaned_data.get('is_active')
                user_to_update.role = form.cleaned_data['role']
                user_to_update.save()
                return redirect('authentication:users_list')
            else:
                return HttpResponse('You are not allowed to update this user.')
        else:
            return render(request, 'authentication/details_user.html', {'form': form})
    else:
        form = UpdateUserForm()
        return render(request, 'authentication/details_user.html', {'form': form})

