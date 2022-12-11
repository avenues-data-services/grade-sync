# get_students.py
import asyncio
from aiohttp import ClientSession
from canvas_api import canvas_get

async def get_all_students(campus:str):

    semaphore = asyncio.Semaphore(20)

    users_url = f'https://avenues{campus}.instructure.com/api/v1/accounts/1/users/'
    users_params = [
        ('per_page', '100'),
        ('enrollment_type', 'student')
    ]

    resp = None

    async with ClientSession() as client:
        try:
            resp = await canvas_get(semaphore, users_url, client, params=users_params)
        except:
            pass

    students = []

    if resp:
        for s in resp:
            try:
                sisID = int(s['sis_user_id'])
            except:
                sisID = s['sis_user_id']
            students.append({
                'id': int(s['id']),
                'name': s['name'],
                'sortable_name': s['sortable_name'],
                'email': s['login_id'],
                'sisID': sisID
            })

    return students