from django.urls import path

from apps.web.users.views import UsersView, UsersFormView, UsersDeleteView


app_name = "users"

urlpatterns = [
    path('', UsersView.as_view(), name="index"),
    path('create', UsersFormView.as_view(), name="form-create"),
    path('<int:id>', UsersFormView.as_view(), name="form-detail"),
    path('<int:id>/delete', UsersDeleteView.as_view(), name="delete"),
]
