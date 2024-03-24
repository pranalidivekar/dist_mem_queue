
import requests
import multiprocessing as mp
import mr4mp 
import time
import csv
import sys

def combine_lists ( l1, l2 ):
    return l1 + l2

def map_reduce( map_fn, reduce_fn, in_list, stages=None, progress=None, cpu_count=None ):    
    if cpu_count is None:
        p = mr4mp.pool( processes=mp.cpu_count() )
    else:
        p = mr4mp.pool( processes=cpu_count )
    if stages is not None:
        print(f"\n*MapReduce in {stages} stages*")    
    r = p.mapreduce( map_fn, reduce_fn, in_list, stages=stages, progress=progress )
    p.close() 

    return r

def client(query):    
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
    workers = int(sys.argv[2])
    queries = get_queries(path_queries)    
    print("Number of queries: ", len(queries))
    #SERIAL
    # time_acum = 0    

    # for q in queries:
    #     A = client(q)
    #     time_acum += A[0][1]        
    # average_response_time = time_acum/len(queries)
         

    # PARALLEL
    data = map_reduce(client,combine_lists,queries, cpu_count=workers)
          
    average_response_time = sum(d[1] for d in data)/len(data)
    print("time", data)
    print("average_response_time", average_response_time)

if __name__ == "__main__":
    main()
