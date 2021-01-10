from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Person, Course, Node, baseCourseCode, baseCourse
from django.http import Http404
from django.shortcuts import redirect
from .forms import createCourseForm, nodeForm, nodeForm1, nodeForm2
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

import json

count = int()


# Create your views here.


def logout_view(request):
    logout(request)
    return redirect("")


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            newPerson = Person.objects.create(user=user)
            newPerson.save()
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, 'courses/signup.html', {'form': form})


def index(request):
    id = request.user.id
    if (id == None):
        template = loader.get_template('courses/index.html')
        context = {
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect("/profile/")


def profile(request):
    id = request.user.id
    if id != None:
        return redirect('/viewProfile/' + str(id) + '/')
    return HttpResponse('you are not logged in </br><a href="/accounts/login/">login</a>')


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
            form = createCourseForm()
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
    count = [1]
    graph = makeGraph(course.MainCourse, count)
    count = count[0]
    # print(count)
    graph = json.dumps(graph)
    anodeForm = nodeForm()
    return HttpResponse(template.render({'course': Course.objects.get(pk=Course_id), 'count': count, "graph": graph, "nodeForm": anodeForm, "nodeForm1": nodeForm1(), "nodeForm2": nodeForm2()}, request))


def makeGraph(aNode, count):

    pre = "none"
    con = "none"
    anti = "none"

    if aNode == None:
        return {}

    if aNode.NodeType == 'NODE':
        name = aNode.base.name
        pre = aNode.base.pre
        anti = aNode.base.anti
        con = aNode.base.con
    else:
        alist = list()
        for node in aNode.child.all():
            if node.NodeType == 'NODE':
                alist.append(node.__str__())
            else:
                alist.append(node.__str__() + " NODE")
        name = (" " + aNode.__str__().lower() + " ").join(alist)
    toReturn = {'name':   aNode.__str__(), 'children': [],
                "type": aNode.NodeType, "courseName": name, "pre": pre, "anti": anti, "con": con, "id": aNode.id}
    if len(aNode.child.all()) != 0:
        for node in aNode.child.all():
            toReturn['children'].append(makeGraph(node, count))
        count[0] += 1
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


def changeCourse(request, node_id):
    courseNum = request.GET.get('courseNum')
    print(courseNum)
    toChange = Node.objects.get(id=node_id)
    print(toChange.base)
    print(baseCourse.objects.get(id=courseNum))
    toChange.base = baseCourse.objects.get(id=courseNum)
    toChange.save()
    print(toChange.base)

    return redirect("/")


def addChild(request, node_id):
    courseNum = request.GET.get('courseNum')
    choice = request.GET.get('choice')
    mainCourse = request.GET.get('mainCourse')
    toChange = Node.objects.get(id=node_id)
    if (choice == 'NODE'):
        n = Node.objects.create(MainCourse=Course.objects.get(id=mainCourse), NodeType='NODE',
                                base=baseCourse.objects.get(id=courseNum))
    else:
        n = Node.objects.create(MainCourse=Course.objects.get(id=mainCourse), NodeType=choice,
                                base=None)
    n.save()
    toChange.child.add(n)
    toChange.save()

    return viewCourse(request, mainCourse)


def deleteNode(request, node_id):
    toChange = Node.objects.get(id=node_id)
    toChange.delete()

    return redirect(request.META['HTTP_REFERER'])
