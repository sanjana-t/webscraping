from fastapi import FastAPI
from typing import List
from bs4 import BeautifulSoup
import requests
from transformers import pipeline
from pydantic import BaseModel
import json
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Item(BaseModel):
    url: str

class BulkItem(BaseModel):
    urls: List[str]

def scrape_summarize(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1').get_text() if soup.find('h1') else None
    links = [link.get('href') for link in soup.find_all('a') if link.get('href')]
    text = ' '.join([p.get_text() for p in soup.find_all('p')])

    summarizer = pipeline("summarization", model="t5-small")
    summary = summarizer(text, do_sample=False)[0]['summary_text']
    return title, summary, links



def scrape_summarize_test(item):
    global scraped_results
    scraped_results = []
    results =[]
    for url in item.urls:
        data={}
        data['title']=""
        data['summary']=""
        data['links']=[]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1').get_text() if soup.find('h1') else None
        links = [link.get('href') for link in soup.find_all('a') if link.get('href')]
        text = ' '.join([p.get_text() for p in soup.find_all('p')])

        summarizer = pipeline("summarization", model="t5-small")
        # summary = summarizer(text, do_sample=False)[0]['summary_text']
        summary = summarizer(text, max_length=int(len(content)*0.3), min_length=int(len(content)*0.2), do_sample=False)[0]['summary_text']
        data['title']=title
        data['summary']=summary
        data['links']=links
        matrix = get_cosine_distance_matrix(url)
        data['matrix']= matrix.tolist()
        results.append(data)
    scraped_results.append(results)
    with open("log.txt", mode="w") as email_file:
        my_string = ",".join(str(element) for element in results)
        email_file.write(my_string)
    store_request_res(item.urls,results)
    return title, summary, links

def create_empty_json_file(filename):
    with open(filename, 'w') as file:
        json.dump({}, file)

create_empty_json_file('requests_responses.json')

def store_request_res(request,response):
    with open('requests_responses.json', 'r+') as file:
        data = json.load(file)
        if 'log_list' not in data:
            data['log_list'] = []
        data['log_list'].append({'request': request, 'response': response})
        file.seek(0)
        json.dump(data, file)
        file.truncate()

def get_result():
    if 'scraped_results' in globals():
        if len(scraped_results)>0:
            return {"message": "Crawling complete", "results": scraped_results,"status": "Completed"}
        else:
            return {"status": "In progress"}
# for each url

def cosine_matrix(item):
    documents = [extract_text_from_url(url) for url in item.urls]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    cosine_dist_matrix = 1 - cosine_sim_matrix
    similarities = []
    for i in range(len(item.urls)):
        for j in range(i + 1, len(item.urls)):
            similarities.append({
                i: item.urls[i],
                j: item.urls[j],
                "similarity": cosine_sim_matrix[i, j],
                "distance": cosine_dist_matrix[i, j]
            })

    return similarities

# Function to extract text from a URL
def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    return text

# Function to compute vector embeddings using spaCy
def compute_embeddings(text):
    nlp = spacy.load("en_core_web_md")
    doc = nlp(text)
    return doc.vector.reshape(1, -1) 

# Function to compute cosine distance matrix for a list of embeddings
def compute_cosine_distance_matrix(embeddings):
    return cosine_similarity(embeddings, embeddings)

# Function to process url and return cosine distance matrix
def get_cosine_distance_matrix(url):
    text = extract_text_from_url(url)
    embedding = compute_embeddings(text)
    cosine_distance_matrix = compute_cosine_distance_matrix(embedding)
    if cosine_distance_matrix.ndim == 1:
        return  cosine_distance_matrix.reshape(1, -1)
    elif cosine_distance_matrix.ndim == 2 and cosine_distance_matrix.shape[0] == 1:
       return  cosine_distance_matrix.reshape(-1, 1)

