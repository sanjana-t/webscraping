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
        li = [item.get('request') for item in contents['log_list']]
        req.append(li)
    return req

# urls = ['https://example.com/page1', 'https://example.com/page2', 'https://example.com/page3']
# cosine_distance_matrix = get_cosine_distance_matrix(urls)
# print(cosine_distance_matrix)