from django.db import models


class Courses(models.Model):
    course = models.CharField(max_length=50, blank=True, null=True)
    mentor = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courses'


class UserCourse(models.Model):
    id_user = models.ForeignKey('Users', models.CASCADE, db_column='id_user', blank=True, null=True)
    id_course = models.ForeignKey(Courses, models.CASCADE, db_column='id_course', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usercourse'


class Users(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    id_role = models.ForeignKey("Roles", models.CASCADE, db_column='id_role', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Roles(models.Model):
    role = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'
