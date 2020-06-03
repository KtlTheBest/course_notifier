import re
import requests
import json
import smtplib
import sys

from config import *

server_url = "smtp.gmail.com"
server_port = 465

login = EMAIL_LOGIN
password = EMAIL_PASSWORD

rlogin = REGISTRAR_LOGIN
rpassword = REGISTRAR_PASSWORD

subject = "Available courses found!"
message = "Subject: {}\n\nThese courses seem available, make sure to register them quickly!\n\n".format(subject)

registrar_url = "https://registrar.nu.edu.kz"
get_courses_url = "https://registrar.nu.edu.kz/my-registrar/course-registration/json?method=getCourseList&_dc=1590483127586&schoolID=&instructorID=&subjectID=&titleText=&openClassesOnly=true&page=1&start=0&limit=10000"
#get_course_detail = "https://registrar.nu.edu.kz/my-registrar/course-registration/json?_dc=1590483221890&method=getCourseDetails&instanceid={}"

headersPost = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "https://registrar.nu.edu.kz/user/login",
    "Content-Type": "application/x-www-form-urlencoded",
    "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"
}

headersGet = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'https://registrar.nu.edu.kz/my-registrar/course-registration',
    'DNT': '1',
    'Connection': 'close',
    'Upgrade-Insecure-Requests': '1'
}

wanted_courses = WANTED_COURSES


def login2registrar(username, password):
    url = registrar_url
    r = requests.Session()
    html = r.get(url + "/my-registrar").text
    csrfTokenReg = re.compile(r'name="csrf_token" value="(.+?)"')
    csrfMatch = csrfTokenReg.finditer(html)
    csrfToken = ""

    for match in csrfMatch:
        csrfToken = match.group(1)

    formIdReg = re.compile(r'name="form_build_id" value="(.+?)"')
    formMatch = formIdReg.finditer(html)

    for match in formMatch:
        formBuildId = match.group(1)


    data = {
        "csrf_token": csrfToken,
        "name": username,
        "pass": password,
        "form_build_id": formBuildId,
        "form_id": "user_login",
        "op": "Log in"
    }

    r.post(url + '/index.php?q=user/login', headers=headersPost, data=data)
    r.post(url + '/index.php?q=user/login', headers=headersPost, data=data)

    return r


def get_empty_courses():
    s = login2registrar(rlogin, rpassword)
    courses = json.loads(s.get(get_courses_url, headers=headersGet).text)
    return s, courses


def check_course(s, course):
    global message
    print(course)
    text = s.get(get_course_detail.format(course['INSTANCEID']), headers=headersGet).text
    print(text)


def get_server():
    server = smtplib.SMTP_SSL(server_url, server_port)
    server.login(login, password)

    return server


def send_mail(message):
    server = get_server()
    server.sendmail(login, login, message)
    server.quit()


def get_wanted_courses():
    global wanted_courses
    args = sys.argv

    if len(args) > 1:
        for course in args[1:]:
            if course not in wanted_courses:
                wanted_courses.append(course)


def main():
    global message

    get_wanted_courses()
    s, empty_courses = get_empty_courses()

    if len(empty_courses) > 0:
        payload = ""
        for course in empty_courses:
            if course['COURSECODE'] in wanted_courses:
                payload += "    {}\n".format(course['COURSECODE'])

        if payload != "":
            message += payload
            message += "\nBest wishes,\nDanel"
            send_mail(message)


if __name__ == "__main__":
    main()
