from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from database.repositories import CoursesRepository


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
