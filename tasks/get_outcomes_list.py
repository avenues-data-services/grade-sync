# get_outcomes_list.py
import asyncio
from utiliy import grade_level
from aiohttp import ClientSession
from canvas_api import canvas_get
from datetime import datetime


##################################################### 
# 
# Get the outcome list for all courses/CPAs
#
##################################################### 

async def get_outcomes_list(base_url,assignments,graduation_years,period,subjects_codes):

    semaphore = asyncio.Semaphore(20)

    async with ClientSession() as client:

        # get the list of courses with CPA assignments
        courses = []

        period_start = datetime.strptime(period['start'], '%Y-%m-%dT%H:%M:%SZ')
        period_end = datetime.strptime(period['end'], '%Y-%m-%dT%H:%M:%SZ')

        for a in assignments:
            # if a['course'] not in courses and len(a['course']['outcomes']) > 0:   # after 1st semester the script will check for due date
            #     if a['date'] != None:
            #         a_date = datetime.strptime(a['date'], '%Y-%m-%dT%H:%M:%SZ')
            #         if a_date >= period_start and a_date <= period_end:
            #             courses.append(a['course'])
            if a['course'] not in courses and len(a['course']['outcomes']) > 0:
                courses.append(a['course'])
        

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
                print(grades)
                for grade in grades:
                    new_course = {
                        'name': '',
                        'id': course[0]['enrollments'][0]['course_id'],
                        'grade': grade,
                        'outcomes': []
                    }
                    if new_course not in updated_courses:
                        updated_courses.append(new_course)

        # combine information about each course
        for course in updated_courses:
            for c in courses:
                if course['id'] == c['id']:
                    course['name'] = c['name']
                    for outcome in c['outcomes']:
                        if outcome not in course['outcomes']:
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
                            outcome['outcome'],
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
                        if len(outcome['outcome']) > 0: 
                            code = outcome['outcome'][-3:].replace('.','').replace(')','')
                            code = ''.join([i for i in code if not i.isdigit()])
                            if code in subjects_codes:
                                line[0] = subjects_codes[code]

                        outcomes_list.append(line)

        return outcomes_list