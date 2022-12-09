# get_outcomes.py
import asyncio
from aiohttp import ClientSession
from canvas_api import canvas_get
from utiliy import grade_level

##################################################### 
# 
# Get outcomes
#
##################################################### 

async def get_courses_outcomes_list(base_url,courses,graduation_years,subjects_codes):

    semaphore = asyncio.Semaphore(20)

    async with ClientSession() as client:
       # get the students enrolled in each of the courses
        url = base_url + '/api/v1/courses/%s/users'
        params = [
            ('enrollment_type', 'student'),
            ('include[]', 'enrollments'),
            ('per_page', '100'),
        ]

        resp = await asyncio.gather(*[
            asyncio.create_task(canvas_get(semaphore, url % course['id'], client, resp_data=[], params=params))
            for course in courses
        ])

        # define the grade level of the courses based on the list of students
        updated_courses = []
        for course in resp:
            grades = []
            for user in course:
                g = grade_level(user,graduation_years)
                if g not in grades and g != '':
                    grades.append(g)
            if len(grades) > 0:
                for grade in grades:
                    new_course = {
                        'name': '',
                        'id': course[0]['enrollments'][0]['course_id'],
                        'grade': grade,
                        'outcomes': []
                    }
                    if new_course not in updated_courses:
                        updated_courses.append(new_course)

        # add name to each course
        for course in updated_courses:
            for c in courses:
                if course['id'] == c['id']:
                    course['name'] = c['name']

        # get each course outcomes
        url = base_url + '/api/v1/courses/%s/outcome_rollups'
        params = [
            ('aggregate', 'course'),
            ('include[]', 'outcomes'),
            ('per_page', '100'),
        ]

        resp = await asyncio.gather(*[
            asyncio.create_task(canvas_get(semaphore, url % course['id'], client, resp_data=[], params=params))
            for course in courses
        ])

        outcomes = []
        for course in resp:
            if 'outcomes' in course[1]:
                for outcome in course[1]['outcomes']:
                    new_outcome = {
                        'id': str(outcome['id']),
                        'title': outcome['title'],
                        'description': outcome['description'],
                        'course_id': course[0][0]['links']['course'],
                    }
                    if new_outcome not in outcomes:
                        outcomes.append(new_outcome)

        # add outcomes to each course
        for course in updated_courses:
            for outcome in outcomes:
                if int(course['id']) == int(outcome['course_id']) and outcome not in course['outcomes']:
                    course['outcomes'].append(outcome)

        # generate the outcomes list
        outcomes_list = []
        for course in updated_courses:
            if len(course['outcomes']) > 0:
                for outcome in course['outcomes']:
                    if "Description of criterion" not in outcome:
                        line = [
                            course['name'],
                            course['grade'],
                            outcome['title'],
                            outcome['description'],
                        ]
                        # adjust outcome format
                        if line[3] != None:
                            if '">' in line[3]:
                                start = '">'
                                end = '</span>'
                                s = line[3]
                                line[3] = s[s.find(start)+len(start):s.rfind(end)]
                            line[3] = line[3].replace('<span>','')
                            line[3] = line[3].replace('</span>','')
                            line[3] = line[3].replace('<p>','')
                            line[3] = line[3].replace('</p>','')
                        # replace course by subject
                        if len(outcome['title']) > 0: 
                            code = outcome['title'][-3:].replace('.','').replace(')','')
                            code = ''.join([i for i in code if not i.isdigit()])
                            if code in subjects_codes:
                                line[0] = subjects_codes[code]

                        outcomes_list.append(line)

        return outcomes_list