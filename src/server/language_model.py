from fastapi import FastAPI
import uvicorn

app = FastAPI(title="MODEL")


@app.get("/")
async def root():
    return {"message": "model"}

@app.get("/run_query")
async def run_query(query:str = ""):    
    return {
        "query":query,
        "promt":"sd fsjdfh ksajdfksajdhf sadfsadkf sdkjfsakdjf daksdjfa0",
        "time":54913
    }

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=6060)