# get_outcomes.py
import asyncio
from aiohttp import ClientSession
from canvas_api import canvas_get


##################################################### 
# 
# Get outcomes
#
##################################################### 

async def get_outcomes(base_url,courses):

    semaphore = asyncio.Semaphore(20)

    async with ClientSession() as client:
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
                        'title': outcome['title'][2:].strip()
                    }
                    if new_outcome not in outcomes:
                        outcomes.append(new_outcome)

        return outcomes