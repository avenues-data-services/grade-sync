# get_sections.py
import asyncio
from aiohttp import ClientSession
from canvas_api import canvas_get


##################################################### 
# 
# Get sections
#
##################################################### 

async def get_sections(base_url,courses):

    semaphore = asyncio.Semaphore(20)

    async with ClientSession() as client:
        url = base_url + '/api/v1/courses/%s/sections'
        params = [
            ('include[]', 'students'),
            ('per_page', '100'),
        ]

        resp = await asyncio.gather(*[
            asyncio.create_task(canvas_get(semaphore, url % course['id'], client, resp_data=[], params=params))
            for course in courses
        ])

        sections = []
        for course in resp:
            for section in course:
                new_section = {
                    'name': section['name'],
                    'course': section['course_id'], 
                    'students': [],
                }
                if section['students'] != 'null' and section['students'] != None:
                    for student in section['students']:
                       new_section['students'].append(student['id'])
                if len(new_section['students']) > 0:
                    sections.append(new_section)      

        return sections