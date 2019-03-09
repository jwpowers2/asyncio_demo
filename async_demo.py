#!/usr/bin/python3.6
import csv,datetime,random
import asyncio
from aiohttp import ClientSession

'''
This demo makes successive async requests to an API.  It returns how long it took,
    how many requests, and a list of the stock symbols requested.

most credit to the following pages for help with this demo
    https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
    https://aiohttp.readthedocs.io/en/stable/
    https://hackernoon.com/asynchronous-python-45df84b82434

IEX has a super-fast async endpoint with lots of data so they're great for this demo
'''

# asyncronous GET request 
async def fetch(url,session):
    async with session.get(url) as response:
        return await response.text()

async def run(stocks):

    url = "https://api.iextrading.com/1.0/stock/{}/chart/1d"
    tasks = []
    stock_list = []
    top = random.randint(1,99)

    async with ClientSession() as session:
        start = datetime.datetime.now()
        for i in range(0,top):
            stock_list.append(stocks[i][0])
            task = asyncio.ensure_future(fetch(url.format(stocks[i][0]), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        finish = datetime.datetime.now()
        time = finish - start
        print("{} requests in {} seconds:\n {}".format(len(responses),time, stock_list))

# fire up the event loop
with open('nasdaq.csv', 'r') as f:
    stocks_list = list(csv.reader(f))
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(stocks_list))
    loop.run_until_complete(future)
