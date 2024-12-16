from django.urls import include, path


app_name = "api"

urlpatterns = [
    path('users/', include("apps.api.users.urls")),
    path('courses/', include("apps.api.courses.urls")),
]
