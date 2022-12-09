# get_assignments.py
import asyncio
from aiohttp import ClientSession
from canvas_api import canvas_get


##################################################### 
# 
# Get CPA assignments
#
##################################################### 

async def get_assignments(base_url,courses,cpa_title,assignments_exclusion_list,outcomes_exclusion_list,outcomes_list=None):

    semaphore = asyncio.Semaphore(20)

    async with ClientSession() as client:
        url = base_url + '/api/v1/courses/%s/assignments'
        params = [
            ('per_page', '100'),
        ]
        if cpa_title != None:
            params.append(('search_term', cpa_title))

        resp = await asyncio.gather(*[
            asyncio.create_task(canvas_get(semaphore, url % course['id'], client, resp_data=[], params=params))
            for course in courses
        ])

        assignments = []

        for course in resp:
            for assignment in course:
                a = {
                    'id': assignment['id'],
                    'date': assignment['due_at'],
                    'course': { 
                        'id': assignment['course_id'],
                        'name': ''
                    }
                }
                if outcomes_list:
                    a['course']['outcomes'] = []
                    if 'rubric' in assignment:
                        for outcome in assignment['rubric']:
                            if 'outcome_id'in outcome and { str(assignment['id']): str(outcome['outcome_id']) } not in outcomes_exclusion_list:
                                a['course']['outcomes'].append({
                                    'outcome': outcome['description'],
                                    'description': outcome['long_description']
                                })

                if int(a['id']) not in assignments_exclusion_list:
                    assignments.append(a)

        for assignment in assignments:
            for course in courses:
                if assignment['course']['id'] == course['id']:
                    assignment['course']['name'] = course['name']

        return assignments