import aiohttp
import asyncio
import json


async def api_service(service_id, link, quantity):
    payload = {
        'key': 'd0ddd4d40381b435019bd81919226f70', 
        'action': 'add', 
        'service': f'{service_id}',
        'link': f'{link}',
        'quantity': f'{quantity}'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('https://justanotherpanel.com/api/v2', 
                data=payload) as resp:

            response = await resp.text()
            try:
                order = json.loads(response)["order"]
                return order
            except KeyError:
                return response


async def api_status(order_id):
    payload = {
        'key': 'd0ddd4d40381b435019bd81919226f70', 
        'action': 'status',
        'order': f'{order_id}'
    }   

    async with aiohttp.ClientSession() as session:
        async with session.post('https://justanotherpanel.com/api/v2', 
                data=payload) as resp:
        
            response = await resp.text()
            try:
                status = json.loads(response)["status"]
                return status
            except KeyError:
                return response



async def api_balance():
    payload = {
        'key': 'd0ddd4d40381b435019bd81919226f70', 
        'action': 'balance'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('https://justanotherpanel.com/api/v2', 
                data=payload) as resp:
        
            response = await resp.text()
            print(json.loads(response)["balance"] + json.loads(response)["currency"])
