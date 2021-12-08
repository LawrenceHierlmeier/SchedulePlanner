from django import template

register = template.Library()


@register.simple_tag
def meet_requirements(taken_courses, requirements, current_course):
    requirements_split = requirements.split(',')
    requirements_split = requirements_split[0]
    requirements_split = requirements_split.split(':')
    requirements_split = requirements_split[1]
    requirements_split = requirements_split[3:-2]
    exclusive_requirements = requirements_split.split('and')

    taken_courses = taken_courses + ""
    current_course = current_course + ""

    if current_course in taken_courses:
        return "Already In Degree Plan"
    elif taken_courses.find(requirements_split):
        return "Add to Degree Plan"
    else:
        return "Cannot Add To Degree Plan"
