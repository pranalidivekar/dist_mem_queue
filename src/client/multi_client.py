
import requests
import time
import csv
import sys
from distributed import Client


def client_call(query):    
    start = time.time()
    URL_master = "http://localhost:8000/"
    query_return = requests.get(f"{URL_master}get_query", params={"query":query[0]}).json()
    promt = query_return["promt"]
    end = time.time()    
    return [(promt, end-start)]

def get_queries(in_path):
    with open(in_path) as csvfile:
        reader = csv.reader(csvfile)        
        return list(reader)


def main():
    path_queries = sys.argv[1]    
    num_workers = int(sys.argv[2])
    queries = [i[0] for i in get_queries(path_queries)]
    print("Number of queries: ", len(queries))
    print("Number of workers: ", num_workers)
    print()
    #SERIAL
    # time_acum = 0    

    # for q in queries:
    #     A = client(q)
    #     time_acum += A[0][1]        
    # average_response_time = time_acum/len(queries)             

    #dask
    client = Client(processes=False, threads_per_worker=num_workers)
    
    futures = client.map(client_call, queries)
    # wait(futures)
    data = client.gather(futures)
    average_response_time = sum(d[0][1] for d in data)/len(data)    
    print("average_response_time", average_response_time)
    print("-----------------------------")

if __name__ == "__main__":
    main()
