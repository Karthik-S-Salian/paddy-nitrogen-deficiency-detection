from pydantic import BaseModel
from fastapi import  UploadFile

class PredictResponse(BaseModel):
    message:str

class PredictRequest(BaseModel):
    image:UploadFile
