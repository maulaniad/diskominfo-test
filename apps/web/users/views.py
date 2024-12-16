from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from database.repositories import UsersRepository, RolesRepository


class UsersView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.session.get('is_admin', None):
            data = UsersRepository.get_users()
        else:
            data = UsersRepository.get_user(request.session.get('user_id'))
        return render(request, "pages/users/index.html", {'data': data})


class UsersFormView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user_id = kwargs.get('id', None)
        user_data = UsersRepository.get_user(user_id)
        roles = RolesRepository.get_roles()

        if not user_data:
            return render(
                request,
                "pages/users/form.html",
                {
                    'action': "create",
                    'roles': roles
                }
            )

        return render(
            request,
            "pages/users/form.html",
            {
                'roles': roles,
                'action': "update",
                'id': user_id,
                'username': user_data.username,
                'email': user_data.email,
                'password': user_data.password,
                'role': user_data.id_role.id if user_data.id_role else None,
            }
        )
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user_id = kwargs.get('id', None)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        role = request.POST.get('role', None)

        if not user_id:
            valid_data = UsersRepository.create_user({
                'username': username,
                'email': email,
                'password': password,
                'id_role_id': role
            })
        else:
            valid_data = UsersRepository.update_user(user_id, {
                'username': username,
                'email': email,
                'password': password,
                'id_role_id': role
            })
        if not valid_data:
            messages.error(request, ("User gagal disimpan"))
            return redirect(to="web:users:index")

        messages.success(request, ("User berhasil disimpan"))
        return redirect(to="web:users:index")


class UsersDeleteView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user_id = kwargs.get('id')
        UsersRepository.delete_user(user_id)
        return redirect(to="web:users:index")
