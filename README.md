# webscraping

Run below command to test -

uvicorn main:app --host 0.0.0.0 --port 80

-- Demo

https://github.com/sanjana-t/webscraping/assets/73529434/cef5640c-31b7-464d-bde4-d5c053a49415


![image](https://github.com/sanjana-t/webscraping/assets/73529434/e9be1754-ff71-491f-b2b7-f243e1cd4ec6)


Response -
[
    {
        "0": "https://realpython.com/django-social-post-3/",
        "1": "https://stackoverflow.com/questions/8507723/how-to-start-working-with-gtest-and-cmake",
        "similarity": 0.4873273364043804,
        "distance": 0.5126726635956196
    },
    {
        "0": "https://realpython.com/django-social-post-3/",
        "2": "https://www.w3schools.com/",
        "similarity": 0.20060322949574505,
        "distance": 0.799396770504255
    },
    {
        "1": "https://stackoverflow.com/questions/8507723/how-to-start-working-with-gtest-and-cmake",
        "2": "https://www.w3schools.com/",
        "similarity": 0.1450718815560894,
        "distance": 0.8549281184439106
    }
]


--- Main libraries
 - beautifulsoup4 (web scraping)
 - transfomers (text summarization)

   
---features
   - web scrape api
   - web urls crawl async with 30% text
   - all requests till date api with pagination and no duplicate
   - cosine similarity/distance matrix integrated as separate api itself
