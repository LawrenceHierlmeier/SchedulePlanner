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
degreeAbbreviation = ['Comp Sci', 'Math', 'Comp Eng', 'Philos', 'Stat']


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
    URL = "https://catalog.mst.edu/undergraduate/degreeprogramsandcourses/computerscience/#courseinventory"
    page = get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    courses = soup.find(id="courseinventorycontainer")
    course_blocks = courses.find_all("div", class_="courseblock")

    # JSON Creation
    test_catalog = "Comp Sci"


    data = {"Courses": []}
    for count, course_block in enumerate(course_blocks):
        prereq_list = list(find_course_prereqs(course_block))
        data["Courses"].append({
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
        for course_block in data["Courses"]:
            course = Course(
                course_number=course_block['course_number'],
                name=course_block['name'],
                description=course_block['description'],
                requirements=course_block['requirements'],
                credits=course_block['credits'],
                full_text=course_block['full_text']
            )

            course.save()

    print("Post-Database")

