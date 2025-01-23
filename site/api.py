from fastapi import FastAPI, HTTPException, Query, Request
import uvicorn


app = FastAPI()


@app.get("/postback")
async def handle_postback(request: Request):
    query_params = request.query_params
    print(query_params)
    query_dict = dict(query_params)
    return {"message": "Query parameters received", "data": query_dict}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
