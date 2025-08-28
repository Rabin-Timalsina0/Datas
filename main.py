from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('pickle_files/books.pkl','rb') as f:
    books = pickle.load(f)

with open('pickle_files/popular.pkl','rb') as f:
    popularity = pickle.load(f)

with open('pickle_files/pt.pkl', 'rb') as f:
    pt = pickle.load(f)

with open('pickle_files/similarity.pkl','rb') as f:
    similarity = pickle.load(f)

class response(BaseModel):
    name: str

def recommend_book(book_name):
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity[index])),key=lambda x:x[1],reverse=True)[1:6]
    final = []
    for i in similar_items:
        final.append({'name':pt.index[i[0]],
                      'poster_url':books.loc[books['Book-Title'] == pt.index[i[0]], 'Image-URL-M'].values[0]})
    return final

@app.get('/')
def landing():
    return 'Welcome'

@app.post('/getBooks')
def similar_books(response: response):
    bName = response.name
    recommendations = recommend_book(bName)
    return {'recommendations': recommendations}
