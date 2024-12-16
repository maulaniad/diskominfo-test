from django.urls import path

from .views import UserView


urlpatterns = [
    path('', UserView.as_view(), name="index"),
    path('<int:pk>', UserView.as_view(), name="detail"),
]
