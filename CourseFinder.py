import requests
from bs4 import BeautifulSoup

def setup():
    year = input("Enter year(2018, 2019, ...)or q to quit: ")
    code = input("Enter 3 or 4 letter subject code or q to quit: ")
    season = input("Spring(S) or Fall(F) or q to quit: ")
    course = input("Enter course number or q to quit: ")

    code = code.upper()
    season = season.upper()

    if (len(course) == 2):
        course = '0' + course
        print(course)

    if (season == 'S'):
        season = str(10)
    else:
        season = str(30)

    term = year + season
    print(term)
    print(type(term))

    if (year == 'Q' or code == 'Q' or season == 'Q' or course == 'Q'):
        exit()

    check(code, term, course)

def check(code, term, course):
    url = 'https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.p_ViewSchedule'
    PAYLOAD = {'openclasses':'N', 'subjcode':code, 'validterm':term}
    class_page = requests.post(url, data=PAYLOAD, headers={'host':'mystudentrecord.ucmerced.edu'})

    if class_page.status_code != requests.codes.ok:
        quit('Error: (' + str(class_page.status_code) + ')')

    parsed = BeautifulSoup(class_page.text, 'html.parser')
    link2 = parsed

    for link in parsed.find_all('tr'):	
        if (link.find('a', href=True, text='15001') != None):
            link2 = link
	
    for course in link2.find_all('small')[12]:
        if (course == 'Closed'):
            print(course)
        else:
            print(course, " seats available")

setup()
