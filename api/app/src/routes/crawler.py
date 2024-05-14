from fastapi import APIRouter, Request,BackgroundTasks
from typing import List
from bs4 import BeautifulSoup
import requests
from transformers import pipeline
from pydantic import BaseModel
import json
from .helper import Item,scrape_summarize,scrape_summarize_test,BulkItem,store_request_res,get_result

router = APIRouter()

@router.post("/scrape")
async def scrape_page(item: Item):
    title, summary, links = scrape_summarize(item.url)
    results = {"title": title, "summary": summary, "links": links}
    store_request_res(item.url,results)
    return {"title": title, "summary": summary, "links": links}

@router.post("/bulk-scrape")
async def bulk_scrape(background_tasks: BackgroundTasks,item:BulkItem):
    # for url in item.urls:
    background_tasks.add_task(scrape_summarize_test, item)
    return {"message": "Bulk scraping started","status": "In progress"}

@router.get("/result")
async def result_api():
    data = get_result()
    if data is None:
        return {"status":"Bulk API not triggered"}
    else:
        return get_result()

@router.get("/req_links")
def get_resquest_responses():
    filename = 'requests_responses.json'
    contents = {}
    req=[]
    try:
        with open(filename, 'r') as f:
            contents = json.load(f)
    except Exception as e:
        print(e)
    if 'log_list' in contents:
        urls = set()
        for item in contents['log_list']:
            if 'request' in item:
                request_value = item['request']
                if isinstance(request_value, str):
                    urls.add(request_value)
                elif isinstance(request_value, list):
                    for request_item in request_value:
                            urls.add(request_item)

        unique_urls = list(urls)
        return unique_urls
    else:
        urls = set()
        return list(urls)
