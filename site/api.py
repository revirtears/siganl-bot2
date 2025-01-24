from fastapi import FastAPI, Request
import uvicorn

from signature import BotSettings


app = FastAPI()
bot_settings = BotSettings()


@app.get("/postback")
async def handle_postback(request: Request):
    sub1 = request.query_params.get("sub1") 

    if sub1:
        print(f"sub1: {sub1}")
        await bot_settings.db.add_user_ref(uid=sub1)

    return {"message": "Query parameters received", "sub1": sub1}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
