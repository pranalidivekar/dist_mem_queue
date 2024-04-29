from fastapi import FastAPI
import requests
import random as rn
from contextlib import asynccontextmanager
import asyncio
import uvicorn


urls = [
    "http://localhost:6001/",
    "http://localhost:6002/",
    "http://localhost:6003/"
]

LM_url = "http://localhost:6060/"



def get_executable():    
    fastest = 9999999
    return_url = ""
    query_return = None
    for url in app.slaves_urls:    
        json_query = requests.get(f"{url}get_top_query").json()
        if json_query is not None and json_query["weight"]<fastest:
           fastest = json_query["weight"]
           query_return = json_query
           return_url = url
    if query_return:
        requests.get(f"{return_url}pop_query")
    return query_return

async def run_query(s):     
    while True:                
        query = get_executable()        
        if query:
            resp = requests.get(f"{LM_url}run_query",params={"query":query})    
            id = query["id"] 
            app.results_set[id] = resp.json()["promt"]        
        await asyncio.sleep(s)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # Load the ML model
    asyncio.create_task(run_query(1))
    yield
    # Run on shutdown (if required)
    print('Shutting down...')
    
    

app = FastAPI(title="MASTER",lifespan=lifespan)
app.results_set = {}

app.slaves_urls = urls
# app.completed_queries = {}



def get_url_candidate():    
    smallest_size = int(requests.get(f"{app.slaves_urls[0]}get_num_queries").text)
    return_url = app.slaves_urls[0]

    for url in app.slaves_urls[1:]:
        resp = requests.get(f"{url}get_num_queries")
        value = int(resp.text)        
        if value<smallest_size:            
            smallest_size = value
            return_url = url    
    return return_url


@app.get("/")
async def root():
    return {"message": "Hello master"}

@app.get("/get_query")
async def get_query(query:str = ""):
    id_query = str(rn.randint(0,100000))
    url = get_url_candidate()
    resp = requests.post(f"{url}put_query",params={"query":query,"id":id_query})    
    response_dict = resp.json()
    while not id_query in app.results_set:        
        await asyncio.sleep(1)        
    response_dict["url_slave"] = url
    response_dict["promt"] = app.results_set[id_query]
    return response_dict

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)