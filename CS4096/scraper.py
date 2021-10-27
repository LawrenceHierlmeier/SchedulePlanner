import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CS4096.settings")
django.setup()

from SchedulePlanner.models import Course
from requests import get
from bs4 import BeautifulSoup
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CS4096.settings")

test_catalog = "Comp Sci"

#all major undergrade degrees not including minors
degreeAbbreviation = ['Aero Eng',             'Mil Air',           'Arch Eng',                 'Art', 'Alp',                        'Bio Sci',            'Bus',                          'Cer Eng',            'Chem Eng',                          'Chem',      'Civ Eng',          'Comp Eng',            'Comp Sci',        'Econ',      'Educ',      'Elec Eng',              'Eng Mgt',               'English',                          'Erp',                        'Env Eng',                  'Etyn',      'Exp Eng',               'Finance', 'Fr Eng',                                     'French', 'Geo Eng',               'Geology',              'German', 'History', 'IS&T',                            'Mkt',       'MS&E',                           'Math',        'Mech Eng',              'Met Eng',                  'Mil Army',        'Min Eng',           'Music', 'Nuc Eng',            'Pet Eng',              'Philos',     'Phys Ed',                        'Physics', 'Pol Sci',          'Premed',               'Psych',      'Russian', 'Spanish', 'Sp&m S',                'Stat',       'Sys Eng',            'Theatre']
degrees =            ['aerospaceengineering', 'aerospace-studies', 'architecturalengineering', 'art', 'artslanguagesandphilosophy', 'biologicalsciences', 'businessandmanagementsystems', 'ceramicengineering', 'chemicalandbiochemicalengineering', 'chemistry', 'civilengineering', 'computerengineering', 'computerscience', 'economics', 'education', 'electricalengineering', 'engineeringmanagement', 'englishandtechnicalcommunication', 'enterpriseresourceplanning', 'environmentalengineering', 'etymology', 'explosivesengineering', 'finance', 'foundationalengineeringandcomputingprogram', 'french', 'geologicalengineering', 'geologyandgeophysics', 'german', 'history', 'informationscienceandtechnology', 'marketing', 'materialsscienceandengineering', 'mathematics', 'mechanicalengineering', 'metallurgicalengineering', 'militaryscience', 'miningengineering', 'music', 'nuclearengineering', 'petroleumengineering', 'philosophy', 'physicaleducationandrecreation', 'physics', 'politicalscience', 'prehealthprofessions', 'psychology', 'russian', 'spanish', 'speechandmediastudies', 'statistics', 'systemsengineering', 'theatre']


def find_all_substring(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)


def find_course_prereqs(block):
    desc = block.find('p', class_="courseblockdesc").text
    prereq_text = desc[desc.find("Prerequisite"):desc.find("Co-listed")]
    prereq_text = prereq_text[prereq_text.find('"C"'):]
    prereq_text = prereq_text[:prereq_text.find('accompanied')]
    # print(block.find("p", class_="courseblocktitle").find("em").text[15:])
    for name in degreeAbbreviation:
        indexes = list(find_all_substring(prereq_text, name))
        # print(indexes)
        for index in indexes:
            # print(prereq_text[index:index + len(name)])
            # print(prereq_text[index + len(name) + 1:index + len(name) + 5])
            yield prereq_text[index:index + len(name)], prereq_text[index + len(name) + 1:index + len(name) + 5]


if not os.path.exists('courses.json'):
    # Web Scrape
    data = {}
    for i in range(len(degrees)):
        URL = 'https://catalog.mst.edu/undergraduate/degreeprogramsandcourses/' + degrees[i] + '/#courseinventory'
        page = get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        courses = soup.find(id="courseinventorycontainer")
        course_blocks = courses.find_all("div", class_="courseblock")

        # JSON Creation
        test_catalog = degreeAbbreviation[i]

            #array of all names in json goes here
        data[degrees[i]] = []

        for count, course_block in enumerate(course_blocks):
            prereq_list = list(find_course_prereqs(course_block))
            data[degrees[i]].append({
                'course_number': test_catalog + " " + course_block.find("p", class_="courseblocktitle").find("em").text[9:13],
                'name': course_block.find("p", class_="courseblocktitle").find("em").text[15:],
                'description': course_block.find('p', class_="courseblockdesc").text,
                'requirements': prereq_list,
                'credits': course_block.find("p", class_="courseblocktitle").text[course_block.find("p", class_="courseblocktitle").text.find("(")+5:-3] if len(course_block.find("p", class_="courseblocktitle").text[course_block.find("p", class_="courseblocktitle").text.find("("):]) == 9 else "99",
                'full_text': course_block.text
            })

    with open('courses.json', 'w') as outfile:
        json.dump(data, outfile)


# Database Creation
if os.path.exists('courses.json'):
    print("Pre-DataBase")

    with open('courses.json') as json_file:
        data = json.load(json_file)
        for var in degrees:
            for course_block in data[var]:
                course = Course(
                    course_number=course_block['course_number'],
                    name=course_block['name'],
                    description=course_block['description'],
                    requirements=course_block['requirements'],
                    credits=course_block['credits'],
                    full_text=course_block['full_text']
                )

                course.save()
            print(var)
    print("Post-Database")

