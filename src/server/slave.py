import os
import pandas as pd
import numpy as np
import gensim
from nltk.tokenize import word_tokenize
from sklearn.linear_model import LinearRegression
from fastapi import FastAPI
import bisect
import datetime
import random as rn
import uvicorn
import sys
import pickle

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
            "query": self.query,
            "weight": self.weight.item(),
            "added_at": self.added_at,
            "id": self.id
        }

def insert_query(array, q):
    bisect.insort(array, q)
    return array

def get_weight(query: Query) -> float:
    return query.weight

def train_models():
    data = pd.read_csv('data/test_queries_2.csv')
    tokenized_sentences = [word_tokenize(sentence.lower()) for sentence in data['Sentence']]
    word2vec_model = gensim.models.Word2Vec(tokenized_sentences, vector_size=6, window=2, min_count=1, epochs=10)
    sentence_vectors = np.array([sentence_to_vector(sentence, word2vec_model) for sentence in tokenized_sentences])
    model = LinearRegression()
    model.fit(sentence_vectors, data['Query Execution Time (ms)'])
    return word2vec_model, model

def sentence_to_vector(sentence, word2vec_model):
    vector = np.zeros(word2vec_model.vector_size)
    for word in sentence:
        if word in word2vec_model.wv:
            vector += word2vec_model.wv[word]
    return vector / len(sentence)

def compute_time(query: str):
    if not (os.path.exists("word2vec_model.pkl") and os.path.exists("linear_regression_model.pkl")):
        print("Did not find saved models, training new ones.")
        word2vec_model, model = train_models()
        with open("word2vec_model.pkl", "wb") as f:
            pickle.dump(word2vec_model, f)
        with open("linear_regression_model.pkl", "wb") as f:
            pickle.dump(model, f)
    else:
        print("Loading models from disk.")
        with open("word2vec_model.pkl", "rb") as f:
            word2vec_model = pickle.load(f)
        with open("linear_regression_model.pkl", "rb") as f:
            model = pickle.load(f)
    predicted_time = predict_execution_time(query, word2vec_model, model)
    print("Predicted Query Execution Time:", predicted_time)
    return predicted_time

def predict_execution_time(input_sentence, word2vec_model, linear_regression_model):
    tokenized_sentence = word_tokenize(input_sentence.lower())
    sentence_vector = sentence_to_vector(tokenized_sentence, word2vec_model)
    sentence_vector = sentence_vector.reshape(1, -1)
    predicted_time = linear_regression_model.predict(sentence_vector)
    return predicted_time[0]

@app.get("/")
async def root():
    return {"message": "Hello slave"}

@app.post("/put_query")
async def put_query(query: str = "", id: str = ""):
    query_object = Query(id=id, query=query, weight=compute_time(query=query))
    app.queries = insert_query(app.queries, query_object)
    return query_object.to_dict()

<<<<<<< HEAD
@app.get("/pop_query")
async def pop_query():
=======

@app.post("/pop_query")
async def pop_query(id: str = ""):
>>>>>>> 650693fdd4c97c6384e5df6dd2b3dd25dc44ce24
    if len(app.queries) == 0:
        return None
    deleted = None
    for i in app.queries:
        deleted = i
        app.queries.remove(i)
        break
    return deleted.to_dict()

@app.get("/get_top_query")
async def get_top_query():
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
