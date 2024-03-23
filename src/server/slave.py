from fastapi import FastAPI
import bisect
import datetime
import random as rn
import uvicorn
import sys

app = FastAPI(title="SLAVE")

app.queries = []

class Query():
    def __init__(self, query: str, weight: float, id: str) -> None:
        self.added_at = datetime.datetime.now()
        self.query = query
        self.weight = weight
        self.id = id

    def __lt__(self, other):
        return self.weight < other.weight
    
    def to_dict(self):
        return {
            "query":self.query,
            "weight":self.weight,
            "added_at":self.added_at,
            "id":self.id
        }

def get_weight(query:Query) -> float:
    return query.weight

def insert_query(array, q):    
    bisect.insort(array, q)  
    return array

def compute_time(query: str):
    return rn.randint(0,100)

@app.get("/")
async def root():
    return {"message": "Hello slave"}

@app.post("/put_query")
async def put_query(query:str = "", id: str = ""):    
    query_object = Query(id=id, query=query, weight=compute_time(query=query))
    app.queries = insert_query(app.queries, query_object)    
    return query_object.to_dict()

@app.get("/pop_query")
async def pop_query():
    if len(app.queries) == 0:
        return None
    return app.queries.pop().to_dict()

@app.get("/get_top_query")
async def pop_query():
    if len(app.queries) == 0:
        return None
    return app.queries[0].to_dict()

@app.get("/get_all_queries")
async def get_all_queries():
    return app.queries

@app.get("/get_num_queries")
async def get_num_queries():    
    return len(app.queries)

if __name__ == '__main__':

    uvicorn.run(app, host="0.0.0.0", port=int(sys.argv[1]))