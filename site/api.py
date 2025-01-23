from fastapi import FastAPI, HTTPException, Query, Request
import uvicorn


app = FastAPI()


@app.get("/postback")
async def handle_postback(request: Request):
    print(request)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
