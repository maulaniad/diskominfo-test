from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from database.repositories import ChartQueriesRepository


class LoginView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.session.get('logged_in', None):
            if request.session.get('is_admin', None):
                return redirect("web:dashboard")
            else:
                return redirect("web:courses:index")

        return render(request, "pages/login.html")

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        username = request.POST.get('username', None)
        password = request.POST.get("password", None)

        if not username or not password:
            messages.error(request, "Harap masukkan username dan password")
            return redirect(to="web:login")

        valid_auth = authenticate(request, username=username, password=password)
        if not valid_auth:
            messages.error(request, "Username atau password salah")
            return redirect(to="web:login")

        if not valid_auth.id_role:
            role = None
        else:
            role = valid_auth.id_role.id

        request.session['logged_in'] = True
        request.session['is_admin'] = role == 1
        request.session['user_id'] = valid_auth.id
        return redirect(to="web:dashboard")


class LogoutView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        request.session.flush()
        storage = messages.get_messages(request)
        storage.used = True
        return redirect(to="web:login")


class DashboardView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.session.get('logged_in', None):
            messages.error(request, "Harap login terlebih dahulu")
            return redirect(to="web:login")

        if not request.session.get('is_admin', None):
            messages.error(request, "Harap login sebagai admin terlebih dahulu")
            return redirect(to="web:login")

        participants_data = ChartQueriesRepository.get_total_participants()

        aggregated_participants = {}
        for item in participants_data:
            course = item["course"]
            participants = item["participants"]
            aggregated_participants[course] = aggregated_participants.get(course, 0) + participants

        participants_label = list(aggregated_participants.keys())
        participants_values = list(aggregated_participants.values())

        fees_data = ChartQueriesRepository.get_total_fees()
        aggregated_fees = {}
        for item in fees_data:
            mentor = item["mentor"]
            fees = item["total_fee"]
            aggregated_fees[mentor] = aggregated_fees.get(mentor, 0) + fees

        fees_label = list(aggregated_fees.keys())
        fees_values = list(aggregated_fees.values())

        return render(
            request,
            "pages/dashboard.html",
            {
                'p_labels': participants_label,
                'p_values': participants_values,
                'f_labels': fees_label,
                'f_values': fees_values
            }
        )
