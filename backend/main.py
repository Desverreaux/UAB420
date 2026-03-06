from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow Vue dev server to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows all origins, you can specify your frontend URL here
    allow_methods=["*"], # allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # allows all headers, you can specify which headers are allowed if needed
)

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI!"}