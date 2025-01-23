from fastapi import FastAPI, HTTPException, Query, Request
import uvicorn

from signature import BotSettings


app = FastAPI()
bot_settings = BotSettings()


@app.get("/postback")
async def handle_postback(request: Request):
    user_id = request.query_params.get("user_id")

    if user_id:
        try:
            print(f"User ID: {user_id}")
            return {"message": "Postback успешно получен", "user_id": user_id}, 200
        except ValueError:
            print(f"Некорректный user_id: {user_id}")
            raise HTTPException(status_code=400, detail="Некорректный user_id")
    else:
        print("Параметр user_id отсутствует")
        raise HTTPException(status_code=400, detail="Параметр user_id отсутствует")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
