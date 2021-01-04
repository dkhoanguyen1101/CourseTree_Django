from django import forms
from django.utils.safestring import mark_safe
from .models import baseCourseCode, baseCourse
# import pyodbc

# conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
#                     'Server=DESKTOP-H322HOI;'
#                     'Database=UofC_Tree_Apps;'
#                     'Trusted_Connection=yes;')

# cursor = conn.cursor()


# for  i in baseCourseCode.objects.all():

#     result = cursor.execute(f"SELECT * FROM dbo.{i.code}")
#     for j in result:
#         x = baseCourse.objects.create(num = int(j[0]),name = j[1], course_code = j[2], pre = j[3], anti = j[4], con = j[5], code=i)
# conn.commit()
# conn.close()

#

# result = cursor.execute("SELECT * FROM courses")
# rows = result.fetchall()
# for row in rows:
#     ALL_COURSES.append((row[0], " ".join([row[0].replace("PPLAN", "PLAN").replace("TTRAN", "TRAN"), row[1].replace("PPLAN", "PLAN").replace("TTRAN", "TRAN")])))
# conn.close()

ALL_COURSES = list()
allcoursecode = baseCourseCode.objects.all()
for coursecode in allcoursecode:
    ALL_COURSES.append((coursecode.id, " ".join(
        (coursecode.code, coursecode.course_name))))

NUM_CHOICE = list()
allcourse = baseCourse.objects.filter(code_id=1)
for course in allcourse:
    NUM_CHOICE.append((course.id, str(course.num) + " " + course.name))


class createCourseForm(forms.Form):
    courseName = forms.ChoiceField(label=mark_safe(
        'Course name'), choices=ALL_COURSES, required=False,)
    courseNum = forms.ChoiceField(label=mark_safe(
        'Course num'), choices=NUM_CHOICE, required=True)
    note = forms.CharField(label=mark_safe('Add note'))
