from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Person,Course,Node
from django.http import Http404


# Create your views here.

def index(request):
    template = loader.get_template('courses/index.html')
    context = {

    }
    return HttpResponse(template.render(context, request))

def profile (request, Person_id):
    try:
        person = Person.objects.get(pk=Person_id)
    except Person.DoesNotExist:
        raise Http404("Question does not exist")
    template = loader.get_template('courses/profile.html')
    long_list = Course.objects.order_by('id')
    short_list = list()
    for course in long_list:
        if (course.Owner_id == Person_id):
            short_list.append(course)
    username = Person.objects.get(pk=Person_id)
    context = {
        'course_list' : short_list,
        'username' : username
    }
    return HttpResponse(template.render(context, request))

def viewCourse (request, Course_id):
    try:
        course = Course.objects.get(pk=Course_id)
    except Course.DoesNotExist:
        raise Http404("Question does not exist")
    return HttpResponse('UR looking at %s' %  Course.objects.get(pk=Course_id))