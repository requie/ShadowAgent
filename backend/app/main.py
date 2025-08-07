from fastapi import FastAPI

app = FastAPI(title="ShadowAgent API")

@app.get("/health")
async def health():
    return {"status": "ok"}
