from django.db import models
import hashlib
import pyodbc
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
#                     'Server=DESKTOP-H322HOI;'
#                     'Database=UofC_Tree_Apps;'
#                     'Trusted_Connection=yes;')

# cursor = conn.cursor()


# ALL_COURSES = list()

# result = cursor.execute("SELECT * FROM courses")
# rows = result.fetchall()
# for row in rows:
#     ALL_COURSES.append((row[0], " ".join([row[0].replace("PPLAN", "PLAN").replace("TTRAN", "TRAN"), row[1].replace("PPLAN", "PLAN").replace("TTRAN", "TRAN")])))
# conn.close()
class Person(models.Model):
    # username = models.CharField(max_length=30)
    # password = models.CharField(max_length=30)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    MainCourse = models.ForeignKey(
        'Node',
        on_delete=models.CASCADE,
        default=0,
    )

    Owner = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
        default=0,
        related_name='Course'
    )

    note = models.CharField(max_length=200, default="", blank=True)

    def __str__(self):
        if self.note:
            return (self.MainCourse.__str__() + " (" + self.note + ")")
        return self.MainCourse.__str__()


class Node(models.Model):
    # Course Name

    base = models.ForeignKey(
        'baseCourse',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # Child_ID
    child = models.ManyToManyField('Node', null=True, blank=True)

    # TYPE
    TYPE_CHOICE = [('NODE', 'One Course'),
                   ('AND', 'And'),
                   ('OR',  'OR'),
                   ('OF',  'n OF a,b,c'),
                   ]
    NodeType = models.CharField(
        choices=TYPE_CHOICE, default='NODE', max_length=20)

    # Course the node belongs to
    MainCourse = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.base:
            return (self.base.course_code)
        return self.NodeType


class baseCourseCode(models.Model):
    code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=200, blank=True, null=True)


class baseCourse(models.Model):
    code = models.ForeignKey('baseCourseCode', on_delete=models.CASCADE)
    num = models.IntegerField()
    name = models.CharField(max_length=1024)
    course_code = models.CharField(max_length=20)
    pre = models.CharField(max_length=1024)
    anti = models.CharField(max_length=1024)
    con = models.CharField(max_length=1024)

    def __str__(self):
        return (self.course_code)
