from django.urls import path

from apps.web.courses.views import CoursesView, CoursesFormView, CoursesDeleteView


app_name = "courses"

urlpatterns = [
    path('', CoursesView.as_view(), name="index"),
    path('create', CoursesFormView.as_view(), name="form-create"),
    path('<int:id>', CoursesFormView.as_view(), name="form-detail"),
    path('<int:id>/delete', CoursesDeleteView.as_view(), name="delete"),
]
