# get_terms.py
import asyncio
from aiohttp import ClientSession
from canvas_api import canvas_get


##################################################### 
# 
# Get relevant terms IDs
#
##################################################### 

async def get_terms(base_url,account_id,terms_SIS_ids):

    semaphore = asyncio.Semaphore(1)

    async with ClientSession() as client:

        url = f'{base_url}/api/v1/accounts/{account_id}/terms'
        params = [
            ('workflow_state[]', 'active'),
            ('per_page', '100')
        ]
        all_terms = await canvas_get(semaphore,url,client,resp_data=[],params=params)

        terms_ids = []
        for terms_pg in all_terms:
            for term in terms_pg:
                for SIS_id in terms_SIS_ids:
                    if term['sis_term_id'] == SIS_id:
                        terms_ids.append({ 'name': term['name'], 'id': term['id'] })
        
        return terms_ids 