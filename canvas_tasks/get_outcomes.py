# get_students.py
import asyncio
from aiohttp import ClientSession
from canvas_api import canvas_get

async def get_outcomes(campus:str,outcomes):

    semaphore = asyncio.Semaphore(20)

    url = f'https://avenues{campus}.instructure.com/api/v1/outcomes/'

    resp = None

    async with ClientSession() as client:
        resp = await asyncio.gather(*[
            asyncio.create_task(canvas_get(semaphore, url + str(id), client, resp_data=[], params=None))
            for id in outcomes
        ])

        outcomes = []
        for r in resp:
            outcomes.append({
                'outcomeID': r[0],
                'outcomeTitle': r[5],
                'outcomeDescription': r[9],
            })

    return outcomes