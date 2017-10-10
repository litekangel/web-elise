# coding: utf8
import time
import re
import lxml.html as lh
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import timedelta, datetime

"""
Travail à faire:
s'occuper du formattage de la date en fonction du mois (un mois c'est surement moins de 31jours
Solution
query la date de début et la date de fin d'une semaine et en déduire le jour qu'on est
"""


def init_driver():
    driver = webdriver.Chrome('D:\dev\chromedriver.exe')
    # driver.wait = WebDriverWait(driver, 1)
    driver.implicitly_wait(10)
    return driver


def connect(driver, username, password):
    # driver.get("https://lise.ensam.eu/faces/Login.xhtml")
    # driver.get("https://lise.ensam.eu/faces/Login.xhtml")
    driver.get("https://apps.etre.ensam.eu/cas/login?service=https%3A%2F%2Flise.ensam.eu%2Fj_spring_cas_security_check")
    try:
        j_username = driver.find_element_by_name("username")
        j_password = driver.find_element_by_name("password")

        j_username.send_keys(username)
        j_password.send_keys(password)
        j_username.submit()
    except TimeoutException:
        print("Champ introuvable")


def access_to_planning(driver, month=0):
    # driver.get("https://lise.ensam.eu/faces/Planning.xhtml")
    driver.execute_script(
        "PF('modalePatientez').show();PrimeFaces.addSubmitParam('form',{'form:entree_46994':'form:entree_46994'}).submit('form');return false;")
    # planning = driver.find_element_by_partial_link_text("planning")
    # time.sleep(3)
    time.sleep(3)
    # planning.click()
    mnth = driver.find_element_by_css_selector(
        'div.fc-toolbar > div.fc-right > button.fc-month-button.ui-button.ui-state-default.ui-corner-left.ui-corner-right')
    mnth.click()

    start_date = driver.find_element_by_css_selector(".fc-toolbar > .fc-center")

    sd = start_date.text
    print(sd.split(' ')[3])

    # un mois a quatre semaines non ?
    # crenal = []

    """
    if week != 0:
        last_date = driver.find_element_by_name("form:calendarFinInputDate")
        sd, month, year = sd.split('/')
        monday = datetime(int("20" + year), int(month), int(sd))
        delta = timedelta(days=week * 7)
        wished_monday = monday + delta
        sd = wished_monday.strftime("%d/%m/%y")
        print(sd)
        last_day = wished_monday + timedelta(days=5)
        ld = last_day.strftime("%d/%m/%y")
        print(ld)
        try:
            start_date.clear()
            last_date.clear()
            start_date.send_keys(sd)
            last_date.send_keys(ld)
            ok = driver.find_element_by_id('form:btnOk')
            ok.click()

            time.sleep(2)
        except TimeoutException:
            print("Champ introuvable")
    # time.sleep(1)
    
    current_week = 0
    if week >=0:
        while (current_week < week):
            next = driver.find_element_by_name('form:j_idt117')
            next.click()
            time.sleep(2)
            current_week+=1
    else:
        while (current_week > week):
            try:
                prev = driver.find_element_by_name('form:j_idt114')
            except TimeoutException:
                time.sleep(2)
                prev = driver.find_element_by_name('form:j_idt114')
            prev.click()
            time.sleep(2)
            current_week-=1
    #lessons = driver.find_elements_by_class_name("evenement")
    
    doc = lh.fromstring(driver.page_source)
    # time.sleep(5)
    # prev = driver.find_element_by_name('form:j_idt127')
    # prev.click()
    # time.sleep(5)
    """
    time.sleep(5)
    return [driver.page_source, sd]


def formatter(dom, lesson, weekday, d, m, y):
    types = ['ED_TD', 'TPS', 'CM', 'TPF', 'OH', 'TEST', 'EXAMEN', 'PROJET']
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    lesson = lesson[6:]
    for type in types:
        typec = ' - ' + type + ' - '
        if typec in lesson:
            print("ceci est lesson :")
            print(lesson)
            h = re.findall("[0-9]{2}:[0-9]{2}", lesson)
            title = lesson.split(typec)[0]
            rem = lesson.split(typec)[1]
            teachers = rem.split(' - ')[0]  # On peut encore le découper en utilisant '/'
            room = rem.split(' - ')[1]
            students = rem.split(' - ')[-1]
            dom.append(
                {'type': type, 'weekday': weekday, 'd': d, 'm': str(m).zfill(2), 'y': y,
                 'day': jours[weekday] + ' ' + str(d) + '/' + str(m) + '/' + str(y), 'start': h[0], 'end': h[1],
                 'title': title, 'teachers': teachers, 'room': room, 'students': students})
    return dom


def planning(username="2016-0687", password="Katyamila159", month=0):
    driver = init_driver()
    connect(driver, username, password)
    lessons, date = access_to_planning(driver, month)
    # return [lessons, date]
    # start_d, m, y = date.split('/')
    # time.sleep(5)
    driver.quit()
    print('***************************************************************')
    days1 = [21, 100, 179, 258, 337, 416]  # orientation 1 (ceci sont les top)
    days2 = [51, 229, 407, 585, 763, 941]  # orientation 2 (ceci sont les lefts)

    mois = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre',
            'Décembre']
    # les indices sont les jour de Lundi à Samedi
    # les 4 semaines sont les 3e, 5e, 7e, 9e tableaux de la page_source
    dom = []
    soup = BeautifulSoup(lessons, 'lxml')

    tag = soup.find_all('table')
    tags = []
    for ta in tag:
        tags.append(ta.prettify())

    # return tags

    tables_id = [3, 5, 7, 9]
    weeks = []

    for i in tables_id:
        week = tag[i]
        rows = week.find_all('tr')
        days = [[] for k in range(6)]
        for row in rows:
            tds = row.find_all('td')
            for i, td in enumerate(tds):

                lesson = td.get_text()
                days[i].append(lesson)
                if len(days[i]) != 0:
                    print('pornographix')
                    dom = formatter(dom, lesson, i, days[i][0], mois.index(date.split(' ')[3]) + 1, date.split(' ')[-1])
        weeks.append(days)

    print("ooooooooooooooooooooooooooooooo")
    print(dom)

    return dom
