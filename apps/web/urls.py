from django.urls import path, include

from apps.web.views import (LoginView,
                            LogoutView,
                            DashboardView)


app_name = "web"

urlpatterns = [
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('dashboard', DashboardView.as_view(), name="dashboard"),

    path('courses/', include('apps.web.courses.urls')),
    path('users/', include('apps.web.users.urls')),
    path('usercourse/', include('apps.web.usercourse.urls')),
]
