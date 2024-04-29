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


def get_weight(query: Query) -> float:
    return query.weight


def insert_query(array, q):
    bisect.insort(array, q)
    return array


def sentence_to_vector(sentence, model):
    vectors = []
    for word in sentence:
        try:
            word_vector = model.wv[word]
            vectors.append(word_vector)
        except KeyError:
            pass
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros(model.vector_size)


def predict_execution_time(input_sentence, word2vec_model, linear_regression_model):
    tokenized_sentence = word_tokenize(input_sentence.lower())
    sentence_vector = sentence_to_vector(tokenized_sentence, word2vec_model)
    sentence_vector = sentence_vector.reshape(1, -1)
    predicted_time = linear_regression_model.predict(sentence_vector)
    return predicted_time[0]


def compute_time(query: str):
    # input_sentence = "Example input sentence"
    data = pd.read_csv('data/query_execution_time.csv')
    # Tokenize sentences
    tokenized_sentences = [word_tokenize(sentence.lower()) for sentence in data['Sentence']]
    word2vec_model = gensim.models.Word2Vec(tokenized_sentences, vector_size=6, window=2, min_count=1, epochs=10)
    # Convert sentences to dense vector arrays
    sentence_vectors = np.array([sentence_to_vector(sentence, word2vec_model) for sentence in tokenized_sentences])
    model = LinearRegression()
    model.fit(sentence_vectors, data['Query Execution Time (ms)'])
    predicted_time = predict_execution_time(query, word2vec_model, model)
    print("Predicted Query Execution Time:", predicted_time)
    return predicted_time


@app.get("/")
async def root():
    return {"message": "Hello slave"}


@app.post("/put_query")
async def put_query(query: str = "", id: str = ""):
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