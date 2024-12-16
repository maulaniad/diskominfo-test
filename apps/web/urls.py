from django.urls import path

from apps.web.views import (LoginView,
                            LogoutView,
                            DashboardView,
                            CoursesView,
                            CoursesFormView,
                            CoursesDeleteView,
                            UsersView,
                            UsersFormView,
                            UsersDeleteView,
                            UserCourseView)


app_name = "web"

urlpatterns = [
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('dashboard', DashboardView.as_view(), name="dashboard"),

    path('courses', CoursesView.as_view(), name="courses"),
    path('courses/create', CoursesFormView.as_view(), name="courses-form"),
    path('courses/<int:id>', CoursesFormView.as_view(), name="courses-form-detail"),
    path('courses/<int:id>/delete', CoursesDeleteView.as_view(), name="courses-delete"),

    path('users', UsersView.as_view(), name="users"),
    path('users/create', UsersFormView.as_view(), name="users-form"),
    path('users/<int:id>', UsersFormView.as_view(), name="users-form-detail"),
    path('users/<int:id>/delete', UsersDeleteView.as_view(), name="users-delete"),

    path('usercourse', UserCourseView.as_view(), name="usercourse"),
]
