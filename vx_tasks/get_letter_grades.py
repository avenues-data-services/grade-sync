# get_qualitative_grades.py
import asyncio
from aiohttp import ClientSession
from vx_api import vx_api_get

async def get_letter_grades(classes,endpoint:str,campus:str,token=None):
    semaphore = asyncio.Semaphore(20)

    async with ClientSession() as client:
        resp = await asyncio.gather(*[
            asyncio.create_task(vx_api_get(client,semaphore,endpoint,campus,[('class_id', str(c))],token))
            for c in classes
        ])

        data = []
        token = resp[0]['token']
        for r in resp:
            data = data + r['data']
        
        return {'token': token, 'data': data}