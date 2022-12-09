# get_courses.py
import asyncio
from aiohttp import ClientSession
from canvas_api import canvas_get


##################################################### 
# 
# Get courses
#
##################################################### 

async def get_courses(base_url,account_id,terms_ids,courses_exclusion_list):

    semaphore = asyncio.Semaphore(20)

    async with ClientSession() as client:
        url = f'{base_url}/api/v1/accounts/{account_id}/courses'

        data = []
        for term in terms_ids:
            params = [
                ('state[]', 'available'),
                ('per_page', '100'),
                ('enrollment_term_id', term['id'])
            ]
            term_courses = await canvas_get(semaphore,url,client,resp_data=[],params=params)
            if len(term_courses) > 0:
                data.append(term_courses)
        
        courses = []
        for term in data:
            for course in term:
                if int(course['id']) not in courses_exclusion_list:
                    courses.append({'name': course['name'], 'id': course['id']})

        return courses