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
        return UserCourse.objects.values('id_user', 'id_course')


class RolesRepository:
    @staticmethod
    def get_roles():
        return Roles.objects.all()
