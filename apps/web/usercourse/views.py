from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from database.repositories import UserCourseRepository, CoursesRepository, UsersRepository


class UserCourseView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.session.get('is_admin', None):
            data = UserCourseRepository.get_user_course()
        else:
            data = []

        return render(request, "pages/usercourse/index.html", {'data': data})


class UserCourseFormView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        users = UsersRepository.get_users()
        courses = CoursesRepository.get_courses()
        return render(request, "pages/usercourse/form.html", {'users': users, 'courses': courses})

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user_id = request.POST.get('user', None)
        course_id = request.POST.get('course', None)
        valid_data = UserCourseRepository.create_usercourse(
            {'id_user_id': user_id, 'id_course_id': course_id}
        )
        if not valid_data:
            messages.error(request, "Data gagal disimpan")
            return redirect(to="web:usercourse:index")

        return redirect(to="web:usercourse:index")


class UserCourseDeleteView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        course_id = request.GET.get('id_course', None)
        user_id = request.GET.get('id_user', None)
        UserCourseRepository.delete_usercourse(user_id, course_id)
        return redirect(to="web:usercourse:index")
