from django.db import connection

from database.models import Courses, Users, UserCourse, Roles


class CoursesRepository:
    @staticmethod
    def get_courses():
        return Courses.objects.filter()

    @staticmethod
    def get_course(course_id):
        return Courses.objects.filter(id=course_id).first()

    @staticmethod
    def get_my_courses(user_id):
        user_course_ids = UserCourse.objects.filter(
            id_user=user_id
        ).values_list('id_course', flat=True)
        return Courses.objects.filter(id__in=user_course_ids)

    @staticmethod
    def create_course(data):
        return Courses.objects.create(**data)

    @staticmethod
    def update_course(course_id, data):
        course = Courses.objects.filter(id=course_id).first()
        if not course:
            return None
        course.course = data.get('course', course.course)
        course.mentor = data.get('mentor', course.mentor)
        course.title = data.get('title', course.title)
        course.save()
        return True

    @staticmethod
    def delete_course(course_id):
        return Courses.objects.filter(id=course_id).delete()


class UsersRepository:
    @staticmethod
    def get_users():
        return Users.objects.filter()

    @staticmethod
    def get_user(user_id):
        return Users.objects.filter(id=user_id).first()

    @staticmethod
    def create_user(data):
        return Users.objects.create(**data)

    @staticmethod
    def update_user(user_id, data):
        user = Users.objects.filter(id=user_id).first()
        if not user:
            return None
        user.email = data.get('email', user.email)
        user.username = data.get('username', user.username)
        user.password = data.get("password", user.password)

        role = Roles.objects.filter(id=data.get('id_role_id', 2)).first()
        user.id_role = role
        user.save()
        return True

    @staticmethod
    def delete_user(user_id):
        return Users.objects.filter(id=user_id).delete()


class UserCourseRepository:
    @staticmethod
    def get_user_course():
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT u.id, u.username, c.id, c.course
                FROM usercourse uc
                JOIN users u ON uc.id_user = u.id
                JOIN courses c ON uc.id_course = c.id
                """
            )
            data = cursor.fetchall()

        formatted_list = []
        for course in data:
            formatted_list.append(
                {
                    'id_user': course[0],
                    'username': course[1],
                    'id_course': course[2],
                    'course': course[3]
                }
            )
        return formatted_list

    @staticmethod
    def create_usercourse(data):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO usercourse (id_user, id_course) VALUES (%s, %s)",
                (data.get('id_user_id'), data.get('id_course_id'))
            )
        return True

    @staticmethod
    def delete_usercourse(user_id, course_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM usercourse
                WHERE id_user = %s AND id_course = %s
                """,
                (user_id, course_id)
            )
        return True

class RolesRepository:
    @staticmethod
    def get_roles():
        return Roles.objects.all()


class ChartQueriesRepository:
    @staticmethod
    def get_total_participants():
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select c.course, c.mentor, c.title, count(u.id) as "jumlah_peserta" from usercourse uc
                join courses c on c.id = uc.id_course 
                join users u on u.id = uc.id_user
                group by c.course, c.mentor, c.title
                order by c.mentor;
                """
            )
            data = cursor.fetchall()

        formatted_list: list[dict] = []
        for e in data:
            formatted_list.append({
                'course': e[0],
                'mentor': e[1],
                'title': e[2],
                'participants': e[3]
            })
        return formatted_list

    @staticmethod
    def get_total_fees():
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select c.mentor, count(u.id) as "jumlah_peserta", count(u.id) * 2000000 as "total_fee"
                from usercourse uc
                join courses c on c.id = uc.id_course 
                join users u on u.id = uc.id_user
                group by c.mentor
                order by "total_fee" desc, c.mentor;
                """
            )
            data = cursor.fetchall()

        formatted_list: list[dict] = []
        for e in data:
            formatted_list.append({
                'mentor': e[0],
                'participants': e[1],
                'total_fee': e[2]
            })
        return formatted_list
