from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from database.repositories import (CoursesRepository,
                                   UsersRepository,
                                   UserCourseRepository,
                                   RolesRepository)


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
        return redirect(to="web:login")


class DashboardView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.session.get('logged_in', None):
            messages.error(request, "Harap login terlebih dahulu")
            return redirect(to="web:login")

        return render(request, "pages/dashboard.html")


class CoursesView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.session.get('is_admin', None):
            data = CoursesRepository.get_courses()
        else:
            data = CoursesRepository.get_my_courses(request.session.get('user_id'))
        return render(request, "pages/courses/index.html", {'data': data})


class CoursesFormView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, "pages/courses/form.html")

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        course = request.POST.get('course', None)
        mentor = request.POST.get('mentor', None)
        title = request.POST.get('title', None)

        valid_data = CoursesRepository.create_course({
            'course': course,
            'mentor': mentor,
            'title': title
        })
        if not valid_data:
            messages.error(request, ("Course gagal disimpan"))
            return redirect(to="web:courses")
        
        messages.success(request, ("Course berhasil disimpan"))
        return redirect(to="web:courses")


class CoursesFormDetailView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        course_id = kwargs.get('id')
        user_data = CoursesRepository.get_course(course_id)
        return render(request, "pages/courses/form.html", {'user_data': user_data})


class CoursesDeleteView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        course_id = kwargs.get('id')
        CoursesRepository.delete_course(course_id)
        return redirect(to="web:courses")


class UsersView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.session.get('is_admin', None):
            data = UsersRepository.get_users()
        else:
            data = UsersRepository.get_my_user(request.session.get('user_id'))
        return render(request, "pages/users/index.html", {'data': data})


class UsersFormView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        roles = RolesRepository.get_roles()
        return render(request, "pages/users/form.html", {'roles': roles})


class UsersFormDetailView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user_id = kwargs.get('id')
        user_data = UsersRepository.get_my_user(user_id)
        return render(request, "pages/users/form.html", {'user_data': user_data})


class UsersDeleteView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user_id = kwargs.get('id')
        UsersRepository.delete_user(user_id)
        return redirect(to="web:users")


class UserCourseView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.session.get('is_admin', None):
            data = UserCourseRepository.get_user_course()
        else:
            data = []

        return render(request, "pages/usercourse/index.html", {'data': data})
