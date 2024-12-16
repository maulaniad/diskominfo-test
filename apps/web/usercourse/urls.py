from django.urls import path

from apps.web.usercourse.views import UserCourseView, UserCourseFormView, UserCourseDeleteView


app_name = "usercourse"

urlpatterns = [
    path('', UserCourseView.as_view(), name="index"),
    path('create', UserCourseFormView.as_view(), name="form-create"),
    path('delete', UserCourseDeleteView.as_view(), name="delete"),
]
