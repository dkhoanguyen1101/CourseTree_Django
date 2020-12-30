from django.db import models
import hashlib
import pyodbc
from django.db.models.signals import post_save


conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                    'Server=DESKTOP-H322HOI;'
                    'Database=UofC_Tree_Apps;'
                    'Trusted_Connection=yes;')

cursor = conn.cursor()

ALL_COURSES = list()
NUM_CHOICES = list()
NUM_CHOICES.append((201,201))

result = cursor.execute("SELECT * FROM courses")
rows = result.fetchall()
for row in rows:
    ALL_COURSES.append((row[0].replace("PPLAN", "PLAN").replace("TTRAN", "TRAN"), " ".join([row[0].replace("PPLAN", "PLAN").replace("TTRAN", "TRAN"), row[1].replace("PPLAN", "PLAN").replace("TTRAN", "TRAN")])))

class Person(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=32)

    def __str__(self):
        return self.username




class Course(models.Model):
    MainCourse   =  models.ForeignKey(
        'NODE',
        on_delete=models.CASCADE,
        default=0,
    )

    Owner  =  models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
        default=0,
    )

    note    = models.CharField(max_length=200, default = "",blank=True)

    def __str__(self):
        return (self.MainCourse.aCourse + " "+ str(self.MainCourse.num) + "(note : " + self.note +")")
        

class Node(models.Model):
    #Course Name
    aCourse  = models.CharField(max_length=20, choices=ALL_COURSES)
    #Course Number
    num  = models.IntegerField(choices=NUM_CHOICES)

    

    #Child_ID
    child   =  models.ForeignKey(
        'NODE',                    
        on_delete=models.CASCADE,
        default=0,
        null=True,
        blank=True,
    )

    #TYPE
    TYPE_CHOICE = [('NODE', 'One Course'),
                    ('AND', 'And'),
                    ('OR' ,  'OR'),
                    ('OF' ,  'n OF a,b,c'),
    ]
    NodeType    = models.CharField(choices = TYPE_CHOICE, default='NODE', max_length=20)

    #Course the node belongs to 
    MainCourse  = models.ForeignKey(
        'Course',                    
        on_delete=models.CASCADE,
        default=0,
        null=True,
        blank = True,
    )
    def __str__(self):
        return (self.aCourse +" "+ str(self.num))

