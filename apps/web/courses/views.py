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
        course_id = kwargs.get('id', None)
        course_data = CoursesRepository.get_course(course_id)

        if not course_data:
            return render(request, "pages/courses/form.html", {'action': "create"})

        return render(
            request,
            "pages/courses/form.html",
            {
                'id': course_id,
                'course': course_data.course,
                'mentor': course_data.mentor,
                'title': course_data.title,
                'action': "update"
            }
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        course = request.POST.get('course', None)
        mentor = request.POST.get('mentor', None)
        title = request.POST.get('title', None)
        action = request.GET.get('action', "create")

        if action == "create":
            valid_data = CoursesRepository.create_course({
                'course': course,
                'mentor': mentor,
                'title': title
            })
        else:
            course_id = kwargs.get('id', None)
            valid_data = CoursesRepository.update_course(course_id, {
                'course': course,
                'mentor': mentor,
                'title': title
            })

        if not valid_data:
            messages.error(request, ("Course gagal disimpan"))
            return redirect(to="web:courses:index")

        messages.success(request, ("Course berhasil disimpan"))
        return redirect(to="web:courses:index")


class CoursesDeleteView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        course_id = kwargs.get('id')
        CoursesRepository.delete_course(course_id)
        return redirect(to="web:courses:index")
