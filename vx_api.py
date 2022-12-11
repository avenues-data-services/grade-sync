# main.py
from google.cloud import secretmanager
from google.oauth2 import service_account
import asyncio
import aiohttp
from aiohttp import ClientSession
from datetime import datetime

##################################################### 
# 
# VX API Functions
#
##################################################### 

async def get_vx_api_token(client,campus:str,token=None):
    if token:
        now = datetime.timestamp(datetime.now())
        token_date = token['created_at']
        elapsed_seconds = now - token_date

        if elapsed_seconds > (token['expires_in']-600): # check token expiration date
            return await vx_api_request_new_token(client,campus) # create new token
        else:
            return token # use the same token
    else:
        return await vx_api_request_new_token(client,campus) #create new token


async def vx_api_request_new_token(client:ClientSession, campus:str):
    url = f'https://accounts.veracross.com/avenues_{campus}/oauth/token'
    scopes = [
        'academics.qualitative_grades:read',
        'academics.qualitative_grades:update',
        'academics.qualitative_grades:list',
        'academics.config.grading_periods:list',
        'classes:list',
    ]

    payload = {
        'grant_type': 'client_credentials',
        'client_id': '36eaac1f7118419bab716e756ac70796',
        'client_secret': 'd8fa75f1baad2dbfc44aa1bf5531d9ec37594338a36fe1ef97423ddf34d64bba',
        'scope': ' '.join(scopes)
    }   
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
 
    async with client.post(url=url, data=payload) as resp:
        return await resp.json(content_type='application/json; charset=utf-8') 

async def vx_api_get(client,semaphore,endpoint:str,campus:str,params=None,token=None):
    async with semaphore:
        updated_token = await get_vx_api_token(client,campus,token)

        url = f'https://api.veracross.com/avenues_{campus}/v3/{endpoint}' 

        data = []
        page_num = 1
        next_page = True
        while next_page:
            headers = {
                "Authorization": "Bearer %s" % updated_token['access_token'],
                "X-Page-Size": "1000",
                "X-Page-Number": "%s" % str(page_num),
                "X-API-Value-Lists": "include"
            }
            async with client.get(url=url, headers=headers, params=params, ssl=True) as resp:
                resp_data = await resp.json()

                if len(resp_data['data']) > 0:
                    data = data + resp_data['data']
                    page_num += 1
                else:
                    next_page = False
        return {'token': updated_token, 'data': data}