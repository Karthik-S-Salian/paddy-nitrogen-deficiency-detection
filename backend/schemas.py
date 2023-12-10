from pydantic import BaseModel
from fastapi import  UploadFile

class PredictResponse(BaseModel):
    cls:str

class PredictRequest(BaseModel):
    image:UploadFile
