from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .users import UserForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Python, Django


class UserFormView(View):
    form_class = UserForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            if user.email:
                user.save()
                user = authenticate(username=username, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
        return render(request, 'registration.html', {'form': form})


def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
        return render(request, 'index.html', {'logged': 1})
    return render(request, 'index.html', {'logged': 2})


def home(request):
    if request.user.is_authenticated():
        python_list = Python.objects.all()
        django_list = Django.objects.all()
        return render(request, 'home.html', {'username': request.user.get_username(),
                                             'python_list': python_list, 'django_list': django_list})
    python = Python.objects.all()[0]
    django = Django.objects.all()[0]
    return render(request, 'index.html', {'registration': 1, 'python_lesson': python,
                                          'django_lesson': django})


def index(request):
    python = Python.objects.all()[0]
    django = Django.objects.all()[0]
    return render(request, 'index.html', {'python_lesson': python, 'django_lesson': django})


class LogUser(View):
    form_class = UserForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, email=email, password=password)
        if user is not None:
            if email == user.email:
                login(request, user)
                return HttpResponseRedirect(reverse(home))
            return render(request, 'login.html', {'email': 1, 'form': form})
        return render(request, 'login.html', {'form': form})
