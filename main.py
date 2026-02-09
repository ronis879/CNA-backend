from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "CNA Phase 1 is running"}
