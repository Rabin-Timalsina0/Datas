from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import pickle
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory='templates')

with open('features.pickle','rb') as f:
    feature_names = pickle.load(f)

with open('model.pickle','rb') as f:
    model = pickle.load(f)

with open('unique_loc.pickle','rb') as f:
    locations = pickle.load(f)

def predict_price(model, area, bed, bath, location):
    features = pd.DataFrame([{cols : 0 for cols in feature_names}])
    features['total_sqft'] = area
    features['bath'] = bath
    features['bhk'] = bed

    locations_df = pd.get_dummies(pd.Series([location]), dtype=int).iloc[0]
    for col in locations_df.index:
        if col in features.columns:
            features[col] = locations_df[col]
    
    predicted = model.predict(features)
    return str(predicted[0]) + 'lakhs'

@app.get('/')
async def landing_page(request: Request):
    return templates.TemplateResponse('index.html',{'request':request, 'locations':locations})

@app.post('/predict')
async def prediction_page(request: Request, location: str = Form(...), total_sqft: float = Form(...), bhk: int = Form(...), bath: int = Form(...)):
    predicted_price = predict_price(model, total_sqft, bhk, bath, location)
    return templates.TemplateResponse('index.html',{'request':request, 'predicted_price':predicted_price, 'locations': locations})