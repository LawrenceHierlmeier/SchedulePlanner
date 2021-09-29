import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CS4096.settings")
django.setup()

from SchedulePlanner.models import Course
from requests import get
from bs4 import BeautifulSoup
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CS4096.settings")



#Web Scrape
URL = "https://catalog.mst.edu/undergraduate/degreeprogramsandcourses/computerscience/"
page = get(URL)

soup = BeautifulSoup(page.content, "html.parser")

courses = soup.find(id="courseinventorycontainer")
course_blocks = courses.find_all("div", class_="courseblock")

#Database Creation

test_catalog = "Comp Sci"
degreeAbbreviation = ['Comp Sci', 'Math', 'Comp Eng', 'Philos', 'Stat']

def find_course_prereqs(block):
    desc = block.find('p', class_="courseblockdesc").text
    print(desc)

print("Pre-DataBase")

'''
for count, course_block in enumerate(course_blocks):
    find_course_prereqs(course_block)
'''

for count, course_block in enumerate(course_blocks):
    if (course_block.find("p", class_="courseblocktitle").find("em").text[15:] != "Special Problems") and (course_block.find("p", class_="courseblocktitle").find("em").text[15:] != "Special Topics"):
        course = Course(
            course_number=test_catalog + " " + course_block.find("p", class_="courseblocktitle").find("em").text[9:13],
            name=course_block.find("p", class_="courseblocktitle").find("em").text[15:],
            description=course_block.find('p', class_="courseblockdesc").text,
            requirements="",
            credits=course_block.find("p", class_="courseblocktitle").text[course_block.find("p", class_="courseblocktitle").text.find("(")+5:-3] if len(course_block.find("p", class_="courseblocktitle").text[course_block.find("p", class_="courseblocktitle").text.find("("):]) == 9 else "99",
            full_text=""
        )

        course.save()

print("Post-Database")
