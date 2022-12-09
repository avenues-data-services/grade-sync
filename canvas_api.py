# main.py
from google.cloud import secretmanager
from google.oauth2 import service_account
import asyncio
import aiohttp
from aiohttp import ClientSession

##################################################### 
# 
# Get Canvas API Key
#
##################################################### 

project_id = 'cp-gradebook'
secret_name = "canvas-key"
#secret_name = "canvas-key-sv"
#secret_name = "canvas-key-ny"

credentials = service_account.Credentials.from_service_account_file('cp-gradebook-e8acace97515.json')
secret_client = secretmanager.SecretManagerServiceClient(credentials=credentials)

name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
response = secret_client.access_secret_version(name=name)
canvas_api_key = response.payload.data.decode("UTF-8")


##################################################### 
# 
# Canvas API Functions
#
##################################################### 

async def api_request(semaphore, url: str, client: ClientSession, params=None):
    async with semaphore:
        headers = {"Authorization": "Bearer %s" % canvas_api_key}
        print(url)
        async with client.get(url=url, headers=headers, params=params, ssl=True) as resp:
            json = await resp.json()
            links = resp.links

            return {'links': links, 'json': json}


async def canvas_get(semaphore, url: str, client: ClientSession, resp_data=[], params=None, key=None, one_page=False):
    # Perform a GET request to the Canvas API.
    resp = await api_request(semaphore, url, client, params=params)
    new_resp_data = resp['json']

    # Handle type of response.
    resp_data = append_response(resp_data, new_resp_data)      
    
    # Handle pagination
    if not one_page and 'next' in resp['links'].keys():
        # If this is the first page
        if resp['links']['current']['url'] == resp['links']['first']['url']:
            if 'last' in resp['links']:
                last_page_url = str(resp['links']['last']['url'])

                num_pages = int(last_page_url[
                    last_page_url.find("page=") + len("page="):last_page_url.rfind("&per_page")
                ])

                urls = []
                for page in range(num_pages-1):
                    url = last_page_url
                    if '?page=' in url:
                        url = url.replace("?page=" + str(num_pages), "?page=" + str(page+2))
                    else:
                        url = url.replace("&page=" + str(num_pages), "&page=" + str(page+2))
                    urls.append(url)
                pgs_data = await asyncio.gather(*[
                    asyncio.create_task(canvas_get(semaphore, page_url, client, resp_data=resp_data, params=params, key=key, one_page=True)) for page_url in urls
                ])
                for new_resp_data in pgs_data:
                    resp_data = append_response(resp_data, new_resp_data)
                return resp_data
            else:
                return await canvas_get(semaphore, resp['links']['next']['url'], client, resp_data=resp_data, params=params, key=key)
        else:
            return await canvas_get(semaphore, resp['links']['next']['url'], client, resp_data=resp_data, params=params, key=key)
    # There are no more pages
    else:
        if key:
            return (key, resp_data)
        else:
            return resp_data

def append_response(resp_data, new_resp_data):
    # Returns combination of prior pages' data and the current page's data.
    if type(new_resp_data) == list:
        if len(resp_data) > 0:
            resp_data = resp_data + new_resp_data
        else:
           resp_data = new_resp_data
    elif type(new_resp_data) == dict:
        for item in new_resp_data:
            resp_data.append(new_resp_data[item])
    
    return resp_data

