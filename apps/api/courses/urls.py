from django.urls import path

from .views import CoursesView


urlpatterns = [
    path('', CoursesView.as_view(), name="index"),
    path('<int:pk>', CoursesView.as_view(), name="detail"),
]
