
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import joblib
import os
import pandas as pd
from loguru import logger
 
# Creating FastAPI instance
app = FastAPI()
 
# Creating class to define the request body
# and the type hints of each attribute
class HouseInfo(BaseModel):
    MSSubClass : int = 60
    MSZoning : str = "RL"
    LotArea : int = 7844
    LotConfig : str = "Inside"
    BldgType : str = "1Fam"
    OverallCond : int = 7
    YearBuilt : int = 1978
    YearRemodAdd : int = 1978
    Exterior1st : str = "HdBoard"
    BsmtFinSF2 : float = 0.0
    TotalBsmtSF : float = 672.0


# Loading model with default path models/model.pkl
clf = joblib.load(
    os.environ.get('MODEL_PATH', "models/model.pkl")
)

# Creating an endpoint to receive the data
# to make prediction on.
@app.post('/predict')
def predict(data : HouseInfo):    
    # Predicting the class
    logger.info("Make predictions...")
    # Convert data to pandas DataFrame and make predictions
    price = clf.predict(
        pd.DataFrame(
            jsonable_encoder(data),
            index=[0]
        )
    )[0]
     
    # Return the result
    return { 'price' : price}