from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from routes import crawler

app = FastAPI()

origins = ["*"]  # specify orgins to handle CORS issue

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_v1 = FastAPI()

api_v1.include_router(crawler.router)

app.mount(f"/api/v1", api_v1)

