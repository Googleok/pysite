from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook


def guestbooklist(request):
    guestbooklist = Guestbook.objects.all().order_by('-id')
    data = {'guestbooklist': guestbooklist}

    return render(request, 'guestbook/list.html', data)


def insert(request):
    guestbook = Guestbook()
    guestbook.name = request.POST['name']
    guestbook.password = request.POST['password']
    guestbook.contents = request.POST['contents']

    guestbook.save()

    return HttpResponseRedirect('/guestbook')


def deleteform(requst, id=0):
    data = {'id': id}
    return render(requst, 'guestbook/deleteform.html', data)


def delete(requst, id=0):
    guestbook = Guestbook.objects.filter(id=id).filter(password=requst.POST['password'])
    guestbook.delete()
    return HttpResponseRedirect('/guestbook')
