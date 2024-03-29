import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CS4096.settings")
django.setup()

from SchedulePlanner.models import Course, Department
from requests import get
from bs4 import BeautifulSoup
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CS4096.settings")

test_catalog = "Comp Sci"

#all major undergrade degrees not including minors
degreeAbbreviation = ['Aero Eng', 'Arch Eng', 'Art', 'Bio Sci', 'Bus', 'Cer Eng', 'Chem Eng', 'Chem', 'Civ Eng', 'Comp Eng', 'Comp Sci', 'Econ', 'Educ', 'Elec Eng', 'Eng Mgt', 'English', 'Erp', 'Env Eng', 'Etym', 'Exp Eng', 'Finance', 'French', 'Fr Eng', 'Geo Eng', 'Geology', 'GeoPhys', 'German', 'History', 'IS&T', 'Mkt', 'MS&E', 'Math', 'Mech Eng', 'Met Eng', 'Mil Air', 'Mil Army', 'Min Eng', 'Music', 'Nuc Eng', 'Pet Eng', 'Philos', 'Phys Ed', 'Physics', 'Pol Sci', 'Premed', 'Psych', 'Russian', 'Spanish', 'Sp&m S', 'Stat', 'Sys Eng', 'Tch Com', 'Theatre']
differentWebpages = ['aero-eng', 'arch-eng', 'art', 'bio-sci', 'bus', 'cer-eng', 'chem-eng', 'chem', 'civ-eng', 'comp-eng', 'comp-sci', 'econ', 'educ', 'elec-eng', 'eng-mgt', 'english', 'erp', 'env-eng', 'etym', 'exp-eng', 'finance', 'french', 'fr-eng', 'geo-eng', 'geology', 'geophys', 'german', 'history', 'is-t', 'mkt', 'ms-e', 'math', 'mech-eng', 'met-eng', 'mil-air', 'mil-army', 'min-eng', 'music', 'nuc-eng', 'pet-eng', 'philos', 'phys-ed', 'physics', 'pol-sci', 'premed', 'psych', 'russian', 'spanish', 'sp-m-s', 'stat', 'sys-eng', 'tch-com', 'theatre']
degreeNames = ["Aerospace Engineering", "Architectural Engineering", "Art", "Biological Sciences", "Business", "Ceramic Engineering", "Chemical Engineering", "Chemistry", "Civil Engineering", "Computer Engineering", "Computer Science", "Economics", "Education", "Electrical Engineering", "Engineering Management", "English", "Enterprise Resource Planning", "Environmental Engineering", "Etymology", "Explosives Engineering", "Finance", "French", "Freshman Engineering", "Geological Engineering", "Geology", "Geophysics", "German", "History", "Info Science & Technology", "Marketing", "Materials Science & Eng", "Mathematics", "Mechanical Engineering", "Metallurgical Engineering", "Military Science - Air Force", "Military Science - Army", "Mining Engineering", "Music", "Nuclear Engineering", "Petroleum Engineering", "Philosophy", "Physical Education", "Physics", "Political Science", "Pre-Medicine", "Psychology", "Russian", "Spanish", "Speech & Media Studies", "Statistics", "Systems Engineering", "Technical Communications", "Theatre"]

def find_all_substring(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)

def add_requirements(text):
    stringLang = '('
    indexes = []
    indexDict = {}
    for name in degreeAbbreviation:
        indexForMajor = list(find_all_substring(text.lower(), name.lower()))
        for i in indexForMajor:
            indexDict[i] = name
        indexes += indexForMajor
    indexes.sort()
    for index in indexes:
        if 'or' in text[index-3:index]:
            stringLang += ' or '+str(text[index:index + len(indexDict[index]) + 5])
        elif ',' in text[index-3:index]:
            stringLang += ' and '+str(text[index:index + len(indexDict[index]) + 5])
        else:
            for word in [';', 'and']:
                if word in text[index-4:index]:
                    stringLang += ') and ('+str(text[index:index + len(indexDict[index]) + 5])
                    break
            else:
                if '.' not in text[index-3:index]:
                    stringLang += str(text[index:index + len(indexDict[index]) + 5])
    if stringLang[-1] == '(':
        stringLang = stringLang[0:len(stringLang)-1]+')'
    elif stringLang[-1] != ')':
        stringLang += ')'
    if stringLang == ')':
        return ''
    else:
        return stringLang


def find_course_prereqs(block):
    prereqs = {'prerequisites': '', 'co-listed': '', 'accompanied': ''}

    desc = block.find('p', class_="courseblockdesc").text
    pre_text = desc[desc.find("Prerequisite"):desc.find("Co-listed")]
    pre_text = pre_text[:pre_text.find('accompanied')]
    co_text = desc[desc.find("Co-listed"):]
    co_text = co_text[:desc.find('accompanied')]
    accompanied_text = desc[desc.find('accompanied'):]
    
    desc = desc.lower()
    prereqs['prerequisites'] = add_requirements(pre_text)
    if "sophomore" in desc:
        if prereqs['prerequisites'] == '':
            prereqs['prerequisites'] = "30 credit hours"
        else:
            prereqs['prerequisites'] += " and 30 credit hours"
    elif "junior" in desc:
        if prereqs['prerequisites'] == '':
            prereqs['prerequisites'] = "60 credit hours"
        else:
            prereqs['prerequisites'] += " and 60 credit hours"
    elif "senior or graduate standing" in desc:
        if prereqs['prerequisites'] == '':
            prereqs['prerequisites'] = "90 credit hours"
        else:
            prereqs['prerequisites'] += " and 90 credit hours"
    elif "senior" in desc:
        if prereqs['prerequisites'] == '':
            prereqs['prerequisites'] = "90 credit hours"
        else:
            prereqs['prerequisites'] += " and 90 credit hours"
    elif "graduate" in desc:
        if prereqs['prerequisites'] == '':
            prereqs['prerequisites'] = "Graduate standing"
        else:
            prereqs['prerequisites'] += " and Graduate standing"
    if "literature" in desc:
        if prereqs['prerequisites'] == '':
            prereqs['prerequisites'] = "a semester of college literature"
        else:
            prereqs['prerequisites'] += " and a semester of college literature"
    if "consent" in desc:
        if prereqs['prerequisites'] == '':
            prereqs['prerequisites'] = "consent of instructor"
        else:
            prereqs['prerequisites'] += " and consent of instructor"
    prereqs['co-listed'] = add_requirements(co_text)
    prereqs['accompanied'] = add_requirements(accompanied_text)
    print(prereqs)
    return prereqs

if not os.path.exists('courses.json'):
    # Web Scrape
    data = {}
    for i in range(len(differentWebpages)):
        URL = 'https://catalog.mst.edu/explorecourses/' + differentWebpages[i] + '/#courseinventory'
        page = get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        courses = soup.find(id="courseinventorycontainer")
        course_blocks = courses.find_all("div", class_="courseblock")

        # JSON Creation
        test_catalog = degreeAbbreviation[i]

        #array of all names in json goes here
        data[differentWebpages[i]] = []

        for count, course_block in enumerate(course_blocks):
            prereq_list = find_course_prereqs(course_block)
            data[differentWebpages[i]].append({
                'course_number': test_catalog + " " + course_block.find("p", class_="courseblocktitle").find("em").text[len(test_catalog)+1:len(test_catalog)+5],
                'name': course_block.find("p", class_="courseblocktitle").find("em").text[len(test_catalog)+7:],
                'description': course_block.find('p', class_="courseblockdesc").text,
                'requirements': prereq_list,
                'credits': course_block.find("p", class_="courseblocktitle").text[course_block.find("p", class_="courseblocktitle").text.find("(")+5:-3] if len(course_block.find("p", class_="courseblocktitle").text[course_block.find("p", class_="courseblocktitle").text.find("("):]) == 9 else "99",
                'full_text': course_block.text,
                'department_slug': differentWebpages[i],
                'department_abbr': degreeAbbreviation[i]
            })

    with open('courses.json', 'w') as outfile:
        json.dump(data, outfile)


# Database Creation
if os.path.exists('courses.json'):
    print("Pre-DataBase")

    with open('courses.json') as json_file:
        data = json.load(json_file)
        for idx, var in enumerate(differentWebpages):
            dept = Department(
                abbreviation=degreeAbbreviation[idx],
                slug=var,
                name=degreeNames[idx]
            )
            dept.save()
            for course_block in data[var]:
                course = Course(
                    course_number=course_block['course_number'],
                    name=course_block['name'],
                    description=course_block['description'],
                    requirements=course_block['requirements'],
                    credits=course_block['credits'],
                    full_text=course_block['full_text'],
                    department=dept
                )
                course.save()
            print(var)
    print("Post-Database")

