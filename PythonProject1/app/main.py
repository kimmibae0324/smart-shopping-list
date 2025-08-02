import os
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from Railway!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway가 할당해주는 포트 받기
    uvicorn.run("main:app", host="0.0.0.0", port=port)

