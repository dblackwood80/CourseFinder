import requests
import datetime
from bs4 import BeautifulSoup

def setup():
	#Deal with season
    season = input("Spring(Sp), Summer(Su), or Fall(Fa): ")
    season = season.upper()
	
    if (season == 'SP'):
        season = str(10)
    elif (season == 'SU'):
	    season = str(20)
    elif (season == 'FA'):
	    season = str(30)
    else:
        print('Invalid season. Exiting.')
        exit()
		
	#Deal with year
    year = input("Enter a valid year(2018, 2019, ...): ")
    now = datetime.datetime.now()
	
    if (int(year) < now.year or (season == 'SU' and int(year) < now.year) or (season == 'SU' and int(year) >= now.year)):
	    print('Invalid year. Exiting.')
	    exit()
	
	#Deal with course code
    code = input("Enter 3 or 4 letter subject code: ")
    code = code.upper()
	
	#Deal with course number
    course = input("Enter course number or q to quit: ")
    if (course == 'Q' or course == 'q'):
        exit()
	
    if (len(course) == 1):
        course = '00' + course

    if (len(course) == 2):
        course = '0' + course
		
	#Put it all together
    term = year + season
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
        if (link.find('small', text=code + '-' + course + '-01') != None):
            link2 = link
	
    for tempCourse in link2.find_all('small')[12]:
        if (tempCourse == 'Closed'):
            print(code + '-' + course + '-01')
            print(tempCourse)
        else:
            print(code + '-' + course + '-01')
            print(tempCourse, "seats available")

setup()
