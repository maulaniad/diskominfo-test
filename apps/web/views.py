from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from database.repositories import UserCourseRepository


class LoginView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.session.get('logged_in', None):
            return redirect("web:dashboard")

        return render(request, "pages/login.html")

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        username = request.POST.get('username', None)
        password = request.POST.get("password", None)

        if not username or not password:
            messages.error(request, "Harap masukkan username dan password")
            return redirect(to="web:login")

        valid_auth = authenticate(request, username=username, password=password)
        if not valid_auth:
            messages.error(request, "Username atau password salah")
            return redirect(to="web:login")

        if not valid_auth.id_role:
            role = None
        else:
            role = valid_auth.id_role.id

        request.session['logged_in'] = True
        request.session['is_admin'] = role == 1
        request.session['user_id'] = valid_auth.id
        return redirect(to="web:dashboard")


class LogoutView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        request.session.flush()
        storage = messages.get_messages(request)
        storage.used = True
        return redirect(to="web:login")


class DashboardView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.session.get('logged_in', None):
            messages.error(request, "Harap login terlebih dahulu")
            return redirect(to="web:login")

        return render(request, "pages/dashboard.html")


class UserCourseView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.session.get('is_admin', None):
            data = UserCourseRepository.get_user_course()
        else:
            data = []

        return render(request, "pages/usercourse/index.html", {'data': data})
