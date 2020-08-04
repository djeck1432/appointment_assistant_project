import os
import json
import base64
import asks
from dotenv import load_dotenv
from async_timeout import timeout
from anyio import create_task_group,run
import asyncio
from time import monotonic


async def create_task_id(api_key, base64_image):
    url = 'https://api.anti-captcha.com/createTask'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = json.dumps({'clientKey': api_key,
                       'task':
                           {
                               'type': "ImageToTextTask",
                               'body': base64_image,
                           },
                       })
    response = await asks.request('POST',url,headers=headers,data=data)
    response.raise_for_status()
    task_id = response.json()['taskId']
    return task_id

async def get_captcha_text(api_key, task_id):
    url = 'https://api.anti-captcha.com/getTaskResult'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = json.dumps({
        'clientKey': api_key,
        'taskId': task_id
    })
    response = await asks.request('POST',url, headers=headers, data=data)
    response.raise_for_status()
    result = response.json()
    captcha_solution = result.get('solution')
    if captcha_solution:
        captcha_text = captcha_solution['text']
        return captcha_text


async def solve_captcha(api_key,captcha_queue,base64_image,max_time=20,response_timeout=15):
    try:
        async with timeout(max_time) as cm:
            task_id = await create_task_id(api_key, base64_image)
            #description, why here is sleep(5-10sec) read in the doc https://anticaptcha.atlassian.net/wiki/spaces/API/pages/196633
            await asyncio.sleep(response_timeout)

            result_text = await get_captcha_text(api_key, task_id)
            while not result_text:
                await asyncio.sleep(1)
                result_text = await get_captcha_text(api_key, task_id)
            captcha_queue.put_nowait(result_text)
            # return result_text

    except asyncio.TimeoutError:
        print('finish procces')

async def get_result_capthca(captcha_queue,base64_message):
    load_dotenv()
    api_key = os.getenv('CAPTCHA_KEY')

    async with create_task_group() as captcha:
           await captcha.spawn(solve_captcha,api_key,captcha_queue,base64_message)
