# coding: utf8
from django.http import HttpResponse
from django.shortcuts import render
from django.http import QueryDict
import time
from pprint import pprint
import json

from . import planning


def home(request):
    # prev = time.time()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        week = int(request.POST['week'])
        print(username)
        dom = planning.planning(username, password, week)
    else:
        dom = planning.planning(month=6)
    # {pprint(dom[0])
    pprint(dom)
    s = "<br><br><br><br>"
    r = ""
    """
    text2 = ''
    diff = round(time.time()-prev,3)
    text2 = '<h4>'+str(diff)+'</h4>'
    for e in dom:
        text2 += '<h3>'+e['title']+'</h3><p>Type: '+e['type']+'<br>Enseignants: '+e['teachers']+'<br/>Salle: '+e['room']+'<br/>Etudiants: '+e['students']+'<br>Jour: '+e['day']+ '<br>Début: '+e['start']+'<br>Fin: '+e['end'] +'</p>'
    """

    # data = json.dumps(dom, ensure_ascii=False).encode('utf-8')
    return HttpResponse(dom)
