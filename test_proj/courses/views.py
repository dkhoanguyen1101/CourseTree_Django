from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Person, Course, Node, baseCourseCode, baseCourse
from django.http import Http404
from django.shortcuts import redirect
from .forms import createCourseForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
import json


# Create your views here.

def index(request):
    template = loader.get_template('courses/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def profile(request):
    id = request.user.id
    if id != None:
        return redirect('/viewProfile/' + str(id) + '/')
    return HttpResponse('you are not logged in')


def viewProfile(request, User_id):
    if (request.user.id == User_id):

        if request.method == 'POST':
            form = createCourseForm(request.POST)
            # message = str(form.data['courseNum'])
            n = Node.objects.create(MainCourse=None, NodeType='NODE',
                                    base=baseCourse.objects.get(pk=int(form.data['courseNum'])))
            c = Course.objects.create(
                note=form.data['note'], MainCourse=n, Owner=Person.objects.get(pk=User_id))
            c.save()
            n.MainCourse = c
            n.save()
            form = form = createCourseForm()
            return HttpResponseRedirect("/profile/")

        else:
            form = createCourseForm()

        person = Person.objects.get(pk=User_id)
        template = loader.get_template('courses/profile.html')
        course_list = person.Course.all()
        context = {
            'course_list': course_list,
            'username': person.user.username,
            'form': form,
        }
        return HttpResponse(template.render(context, request))
    return HttpResponse('you are not allowed')


def viewCourse(request, Course_id):
    try:
        course = Course.objects.get(pk=Course_id)
    except Course.DoesNotExist:
        raise Http404("Question does not exist")
    template = loader.get_template('courses/viewCourse.html')
    graph = makeGraph(course.MainCourse)
    graph = json.dumps(graph)
    return HttpResponse(template.render({'course': Course.objects.get(pk=Course_id), "graph": graph}, request))


def makeGraph(aNode):
    if aNode == None:
        return {}
    toReturn = {'name':   aNode.__str__(), 'children': []}
    if len(aNode.child.all()) != 0:
        for node in aNode.child.all():
            toReturn['children'].append(makeGraph(node))
        return toReturn
    else:
        return toReturn


def largeToString(node):
    if node.NodeType == 'NODE' and Node.objects.get() != None:
        return (node.course + '->' + self.largeToString(node.child))
    elif node.type == 'NODE' and node.child == None:
        return node.course
    elif (node.type in ['AND', 'OR', 'OF']):
        count = 0
        stringList = []
        while (count < len(node.courses)):
            stringList.append(self.largeToString(node.courses[count]))
            count += 1

        if (node.type == 'AND'):
            return ('(' + ".".join(stringList) + ')')
        elif (node.type == 'OR'):
            return ('(' + "+".join(stringList) + ')')
        elif (node.type == 'OF'):
            return ('(' + "+".join(stringList) + ')')


# def createGraph(request):
#     print(1)
#     return (render(request, 'courses/node.html', {'node': Node.objects.get(id=int(request.GET.get('node')))}))


def load_num(request):
    code_id = request.GET.get('course')
    # print(code_id)
    courses = baseCourse.objects.filter(code_id=code_id)
    return render(request, 'courses/course_dropdown_list_options.html', {'courses': courses})


def delete_course(request, Course_id):
    course = get_object_or_404(Course, pk=Course_id)
    if (request.method == 'POST'):
        course.delete()
    return redirect('/profile/')
