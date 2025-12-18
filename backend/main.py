from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_engine import RAGSystem
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo purposes, allow all. Change this for production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
rag = RAGSystem()

class QueryRequest(BaseModel):
    query: str

@app.on_event("startup")
async def startup_event():
    if os.path.exists("manual.txt"):
        print("Found manual.txt, ingesting...")
        rag.ingest("manual.txt")
    else:
        print("No manual.txt found. Please upload one.")

@app.post("/chat")
async def chat(request: QueryRequest):
    response = rag.query(request.query)
    return {"response": response}

@app.post("/upload")
async def upload_manual(file: UploadFile = File(...)):
    content = await file.read()
    # Save to disk
    file_path = "manual.txt"
    with open(file_path, "wb") as f:
        f.write(content)
    
    rag.ingest(file_path)
    return {"message": "Manual uploaded and processed successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
