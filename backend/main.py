from fastapi import FastAPI, UploadFile,status,HTTPException,File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from schemas import PredictResponse
from detect import predict_class

app = FastAPI()

origins = [
    "*",
    "http://localhost:37914",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/predict",response_model=PredictResponse)
async def predict(image:UploadFile = File(...)):
    message = predict_class(await image.read())
    return {
        'message': message
    }

if __name__ == "__main__":
    import socket
    hostname = socket.getfqdn()
    ip = socket.gethostbyname_ex(hostname)[2][0]
    uvicorn.run(app, host=ip, port=8000)